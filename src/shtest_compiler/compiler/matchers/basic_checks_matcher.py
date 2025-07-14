import yaml
import os
import re
from shtest_compiler.compiler.matcher_registry import register_matcher
from ..utils import shell_condition, retcode_condition, strip_accents

def load_patterns():
    """Load validation patterns from patterns_validations.yml."""
    patterns_path = os.path.join(os.path.dirname(__file__), "../../config/patterns_validations.yml")
    if not os.path.exists(patterns_path):
        return {}
    
    with open(patterns_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    patterns = {}
    for validation in data.get("validations", []):
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
    
    return patterns

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
    # Étape 2 : Chargement des patterns depuis YAML
    # ------------------------------------------------------------
    patterns = load_patterns()

    # ------------------------------------------------------------
    # Étape 3 : Recherche par alias et regex
    # ------------------------------------------------------------
    for phrase, pattern_info in patterns.items():
        handler_name = pattern_info.get("handler", "")
        aliases = pattern_info.get("aliases", [])
        opposite = pattern_info.get("opposite", {})
        
        # Check exact alias match (normalized)
        if normalized in [strip_accents(alias.lower()) for alias in aliases]:
            return _handle_pattern_match(handler_name, pattern_info, last_file_var, scope)
        
        # Check regex pattern matches
        for alias in aliases:
            if alias.startswith("^") and alias.endswith("$"):
                # This is a regex pattern
                regex_pattern = alias[1:-1]  # Remove ^ and $
                if re.match(regex_pattern, expected, re.IGNORECASE):
                    return _handle_pattern_match(handler_name, pattern_info, last_file_var, scope, expected)

    # ------------------------------------------------------------
    # Étape 4 : Vérification du code de retour (fallback)
    # ------------------------------------------------------------
    # Exemple attendu : "retour 0", "retour 1", etc.
    if normalized.startswith("retour "):
        parts = normalized.split()
        if len(parts) > 1 and parts[1].isdigit():
            return retcode_condition(int(parts[1]), scope)

    # ------------------------------------------------------------
    # Étape 5 : Aucun motif reconnu
    # ------------------------------------------------------------
    return None

def _handle_pattern_match(handler_name, pattern_info, last_file_var, scope, original_text=None):
    """Handle a pattern match by loading and calling the appropriate plugin."""
    try:
        # Import and use the actual plugin
        plugin_module = __import__(f"shtest_compiler.plugins.{handler_name}", fromlist=[handler_name])
        if hasattr(plugin_module, handler_name):
            plugin_class = getattr(plugin_module, handler_name)
            plugin_instance = plugin_class()
            if hasattr(plugin_instance, 'to_shell'):
                # Call the plugin with proper parameters
                return plugin_instance.to_shell(varname="result", last_file_var=last_file_var)
    except Exception as e:
        # Fallback to shell condition if plugin fails
        opposite = pattern_info.get("opposite", {})
        success_msg = pattern_info.get("phrase", "succès")
        fail_msg = opposite.get("phrase", "échec") if opposite else "échec"
        pattern_scope = pattern_info.get("scope", "global")
        
        return shell_condition(success_msg, fail_msg, pattern_scope)
    
    return None