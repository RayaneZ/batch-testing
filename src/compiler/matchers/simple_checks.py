from ..utils import shell_condition

def match(expected, _):
    normalized = expected.lower()
    lookup = {
        "base prête": shell_condition("base prête", "base non prête", "base prête"),
        "contenu affiché": shell_condition("contenu affiché", "contenu non affiché", "contenu affiché"),
        "dossier créé": shell_condition("dossier créé", "échec création", "dossier créé"),
        "fichier cree": shell_condition("fichier cree", "échec création", "fichier cree"),
        "date modifiée": shell_condition("date modifiée", "date inchangée", "date modifiée"),
        "contenu correct": shell_condition("contenu correct", "contenu incorrect", "contenu correct"),
        "logs accessibles": shell_condition("logs accessibles", "logs inaccessibles", "logs accessibles"),
    }
    return lookup.get(normalized)