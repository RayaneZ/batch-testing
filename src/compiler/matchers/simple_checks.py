from ..utils import shell_condition, retcode_condition, strip_accents

def match(expected, _):
    normalized = strip_accents(expected.lower())
    mapping = {
        "base prete": ("base prête", "base non prête"),
        "contenu affiche": ("contenu affiché", "contenu non affiché"),
        "dossier cree": ("dossier créé", "échec création"),
        "fichier cree": ("fichier cree", "échec création"),
        "date modifiee": ("date modifiée", "date inchangée"),
        "contenu correct": ("contenu correct", "contenu incorrect"),
        "logs accessibles": ("logs accessibles", "logs inaccessibles"),
        "le fichier est present": ("Le fichier est présent", "Le fichier est absent"),
        "le dossier est copie": ("le dossier est copié", "le dossier non copié"),
        "le script est affiche": ("contenu affiché", "contenu non affiché"),
        "le fichier est deplace": ("le fichier est déplacé", "fichier non déplacé"),
        "le dossier est deplace": ("le dossier est déplacé", "dossier non déplacé"),
    }

    if normalized in mapping:
        success, fail = mapping[normalized]
        return shell_condition(success, fail)

    if normalized == "identifiants configures":
        return [
            'if [ -n "$SQL_CONN" ]; then actual="identifiants configurés"; else actual="non configuré"; fi',
            'expected="identifiants configurés"',
        ]

    if normalized.startswith("retour "):
        code = normalized.split()[1]
        if code.isdigit():
            return retcode_condition(int(code))

    return None
