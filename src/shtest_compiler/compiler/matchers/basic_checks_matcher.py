from shtest_compiler.compiler.matcher_registry import register_matcher
from ..utils import shell_condition, retcode_condition, strip_accents

@register_matcher("simple_checks")
def match(expected, _):
    """
    Analyse une chaîne 'expected' et retourne une condition shell ou un test adapté
    en fonction de règles pré-définies (présence de fichiers, code de retour, etc.).
    """

    # ------------------------------------------------------------
    # Étape 1 : Normalisation de l'entrée
    # ------------------------------------------------------------
    # - Conversion en minuscules
    # - Suppression des accents (é → e, etc.)
    normalized = strip_accents(expected.lower())

    # ------------------------------------------------------------
    # Étape 2 : Mappage direct vers des tests shell simples
    # ------------------------------------------------------------
    # Chaque clé correspond à une forme textuelle attendue (normalisée)
    # Elle est associée à un couple (message_si_succès, message_si_échec)
    mapping = {
        "base prete": ("base prête", "base non prête"),
        "contenu affiche": ("contenu affiché", "contenu non affiché"),
        "dossier cree": ("dossier créé", "échec création"),
        "fichier cree": ("fichier créé", "échec création"),
        "date modifiee": ("date modifiée", "date inchangée"),
        "contenu correct": ("contenu correct", "contenu incorrect"),
        "logs accessibles": ("logs accessibles", "logs inaccessibles"),
        "le fichier est present": ("Le fichier est présent", "Le fichier est absent"),
        "le dossier est copie": ("le dossier est copié", "le dossier non copié"),
        "le script est affiche": ("contenu affiché", "contenu non affiché"),
        "le fichier est deplace": ("le fichier est déplacé", "fichier non déplacé"),
        "le dossier est deplace": ("le dossier est déplacé", "dossier non déplacé"),
        # Nouveaux matchers ajoutés
        "fichier deplace": ("fichier déplacé", "fichier non déplacé"),
        "dossier deplace": ("dossier déplacé", "dossier non déplacé"),
        "fichier present": ("fichier présent", "fichier absent"),
        "dossier present": ("dossier présent", "dossier absent"),
        "fichier existe": ("fichier existe", "fichier n'existe pas"),
        "variable d'environnement definie": ("variable d'environnement définie", "variable d'environnement non définie"),
        "fichiers identiques": ("fichiers identiques", "fichiers différents"),
    }

    # Si le texte correspond à une des clés du mapping, on retourne la condition shell associée
    if normalized in mapping:
        success_msg, fail_msg = mapping[normalized]
        return shell_condition(success_msg, fail_msg)

    # ------------------------------------------------------------
    # Étape 3 : Cas particulier — vérification d'une variable d'environnement SQL
    # ------------------------------------------------------------
    if normalized == "identifiants configures":
        return [
            'if [ -n "$SQL_CONN" ]; then actual="identifiants configurés"; else actual="non configuré"; fi',
            'expected="identifiants configurés"',
        ]

    # ------------------------------------------------------------
    # Étape 4 : Cas particulier — vérification du code de retour
    # ------------------------------------------------------------
    # Exemple attendu : "retour 0", "retour 1", etc.
    if normalized.startswith("retour "):
        parts = normalized.split()
        if len(parts) > 1 and parts[1].isdigit():
            return retcode_condition(int(parts[1]))

    # ------------------------------------------------------------
    # Étape 5 : Aucun motif reconnu
    # ------------------------------------------------------------
    return None