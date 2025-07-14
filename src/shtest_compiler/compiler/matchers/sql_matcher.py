from shtest_compiler.compiler.matcher_registry import register_matcher
from ..utils import shell_condition, strip_accents


@register_matcher("sql_checks")
def match(expected, _):
    """
    Analyse une chaîne 'expected' et retourne une condition shell pour les validations SQL.
    Gère les vérifications de base de données, scripts SQL, et identifiants.
    """

    # ------------------------------------------------------------
    # Étape 1 : Normalisation de l'entrée
    # ------------------------------------------------------------
    normalized = strip_accents(expected.lower())

    # ------------------------------------------------------------
    # Étape 2 : Mappage des validations SQL
    # ------------------------------------------------------------
    sql_mapping = {
        # Validations de base de données
        "la base est prete pour le test": ("Base prête pour le test", "Base non prête"),
        "la base de test est prete": ("Base de test prête", "Base de test non prête"),
        "base prete": ("Base prête", "Base non prête"),
        # Validations de scripts SQL
        "le script s'execute avec succes": (
            "Script exécuté avec succès",
            "Échec d'exécution du script",
        ),
        "le script s'execute avec succès": (
            "Script exécuté avec succès",
            "Échec d'exécution du script",
        ),
        "script execute avec succes": (
            "Script exécuté avec succès",
            "Échec d'exécution du script",
        ),
        # Validations d'identifiants
        "les identifiants sont configures": (
            "Identifiants configurés",
            "Identifiants non configurés",
        ),
        "identifiants configures": (
            "Identifiants configurés",
            "Identifiants non configurés",
        ),
        "identifiants configurés": (
            "Identifiants configurés",
            "Identifiants non configurés",
        ),
        # Validations de connexion
        "connexion etablie": ("Connexion établie", "Échec de connexion"),
        "connexion reussie": ("Connexion réussie", "Échec de connexion"),
        "base accessible": ("Base accessible", "Base inaccessible"),
    }

    # Si le texte correspond à une des clés du mapping, on retourne la condition shell associée
    if normalized in sql_mapping:
        success_msg, fail_msg = sql_mapping[normalized]
        return shell_condition(success_msg, fail_msg)

    # ------------------------------------------------------------
    # Étape 3 : Vérifications de variables d'environnement SQL
    # ------------------------------------------------------------
    if normalized == "variable sql_conn vaut":
        # Cette validation nécessite une valeur spécifique, on laisse le compilateur la gérer
        return None

    # ------------------------------------------------------------
    # Étape 4 : Vérifications de code de retour SQL
    # ------------------------------------------------------------
    if normalized.startswith("sql retour ") or normalized.startswith("retour sql "):
        parts = normalized.split()
        if len(parts) > 2 and parts[-1].isdigit():
            return [
                f'if [ $? -eq {parts[-1]} ]; then actual="Retour SQL {parts[-1]}"; else actual="Retour SQL différent"; fi',
                f'expected="Retour SQL {parts[-1]}"',
            ]

    # ------------------------------------------------------------
    # Étape 5 : Aucun motif SQL reconnu
    # ------------------------------------------------------------
    return None
