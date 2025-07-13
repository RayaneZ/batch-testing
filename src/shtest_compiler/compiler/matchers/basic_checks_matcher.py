import yaml
import os
from shtest_compiler.compiler.matcher_registry import register_matcher
from ..utils import shell_condition, retcode_condition, strip_accents

def load_validation_mappings():
    """Load validation mappings from YAML configuration file."""
    mappings_path = os.path.join(os.path.dirname(__file__), "../../config/validation_mappings.yml")
    if not os.path.exists(mappings_path):
        return {}, {}, {}
    
    with open(mappings_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    handlers = data.get("handlers", {})
    special_cases = data.get("special_cases", {})
    
    # Create alias-to-handler mapping for quick lookup
    alias_to_handler = {}
    for handler_name, handler_data in handlers.items():
        aliases = handler_data.get("aliases", [])
        for alias in aliases:
            # Normalize alias for case-insensitive matching
            normalized_alias = strip_accents(alias.lower())
            alias_to_handler[normalized_alias] = handler_name
    
    # Load patterns if import_patterns is enabled
    patterns = {}
    if data.get("import_patterns", False):
        patterns_file = data.get("patterns_file", "patterns_validations.yml")
        patterns_path = os.path.join(os.path.dirname(__file__), f"../../config/{patterns_file}")
        if os.path.exists(patterns_path):
            with open(patterns_path, encoding="utf-8") as f:
                patterns_data = yaml.safe_load(f)
                for validation in patterns_data.get("validations", []):
                    phrase = validation.get("phrase", "")
                    handler = validation.get("handler", "")
                    scope = validation.get("scope", "global")
                    aliases = validation.get("aliases", [])
                    opposite = validation.get("opposite", {})
                    
                    patterns[phrase] = {
                        "handler": handler,
                        "scope": scope,
                        "aliases": aliases,
                        "opposite": opposite
                    }
    
    return handlers, special_cases, patterns, alias_to_handler

@register_matcher("simple_checks")
def match(expected, last_file_var=None, scope="global"):
    """
    Analyse une chaîne 'expected' et retourne une condition shell ou un test adapté
    en fonction de règles pré-définies (présence de fichiers, code de retour, etc.).
    Le scope peut être 'global' ou 'last_action'.
    """

    # ------------------------------------------------------------
    # Étape 1 : Normalisation de l'entrée
    # ------------------------------------------------------------
    # - Conversion en minuscules
    # - Suppression des accents (é → e, etc.)
    normalized = strip_accents(expected.lower())

    # ------------------------------------------------------------
    # Étape 2 : Chargement des mappings et patterns depuis YAML
    # ------------------------------------------------------------
    handlers, special_cases, patterns, alias_to_handler = load_validation_mappings()

    # ------------------------------------------------------------
    # Étape 3 : Recherche par alias vers handler
    # ------------------------------------------------------------
    # Si le texte normalisé correspond à un alias, on trouve le handler associé
    if normalized in alias_to_handler:
        handler_name = alias_to_handler[normalized]
        handler_data = handlers.get(handler_name, {})
        
        success_msg = handler_data.get("success", "succès")
        fail_msg = handler_data.get("failure", "échec")
        mapping_scope = handler_data.get("scope", "global")
        
        # Check if we have pattern information for this handler
        if handler_name in [p.get("handler") for p in patterns.values()]:
            # Use pattern-based validation instead of simple shell condition
            for phrase, pattern_info in patterns.items():
                if pattern_info.get("handler") == handler_name:
                    # Import and use the actual plugin
                    try:
                        plugin_module = __import__(f"shtest_compiler.plugins.{handler_name}", fromlist=[handler_name])
                        if hasattr(plugin_module, handler_name):
                            plugin_class = getattr(plugin_module, handler_name)
                            plugin_instance = plugin_class()
                            if hasattr(plugin_instance, 'to_shell'):
                                # Call the plugin with proper parameters
                                return plugin_instance.to_shell(varname="result", last_file_var=last_file_var)
                    except Exception as e:
                        # Fallback to shell condition if plugin fails
                        pass
        
        return shell_condition(success_msg, fail_msg, mapping_scope)

    # ------------------------------------------------------------
    # Étape 4 : Cas spéciaux avec logique personnalisée
    # ------------------------------------------------------------
    # Vérification d'une variable d'environnement SQL
    if normalized == "identifiants configures":
        special_case = special_cases.get("identifiants configures", {})
        variable = special_case.get("variable", "SQL_CONN")
        success_msg = special_case.get("success", "identifiants configurés")
        fail_msg = special_case.get("failure", "non configuré")
        handler = special_case.get("handler", "")
        
        # Try to use the handler from patterns if available
        if handler and handler in [p.get("handler") for p in patterns.values()]:
            try:
                plugin_module = __import__(f"shtest_compiler.plugins.{handler}", fromlist=[handler])
                if hasattr(plugin_module, handler):
                    plugin_class = getattr(plugin_module, handler)
                    plugin_instance = plugin_class()
                    if hasattr(plugin_instance, 'to_shell'):
                        return plugin_instance.to_shell(varname="result", last_file_var=last_file_var)
            except Exception as e:
                pass
        
        return [
            f'if [ -n "${variable}" ]; then actual="{success_msg}"; else actual="{fail_msg}"; fi',
            f'expected="{success_msg}"',
        ]

    # ------------------------------------------------------------
    # Étape 5 : Vérification du code de retour
    # ------------------------------------------------------------
    # Exemple attendu : "retour 0", "retour 1", etc.
    if normalized.startswith("retour "):
        parts = normalized.split()
        if len(parts) > 1 and parts[1].isdigit():
            return retcode_condition(int(parts[1]), scope)

    # ------------------------------------------------------------
    # Étape 6 : Aucun motif reconnu
    # ------------------------------------------------------------
    return None