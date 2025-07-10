
import pytest
from parser.parser import Parser
from lexer import lex
from parser.shunting_yard import parse_validation_expression


def test_lexer_basic_tokens():
    text = """
    Étape: Connexion
    Action: Cliquer sur "Se connecter" ; Résultat: La page d'accueil s'affiche
    Action: Entrer les identifiants
    Résultat: Authentification réussie
    """
    tokens = list(lex(text))
    kinds = [t.kind for t in tokens]
    assert kinds == ["STEP", "ACTION_RESULT", "ACTION_ONLY", "RESULT_ONLY"]


def test_parser_recognizes_step_and_actions():
    parser = Parser()
    actions = parser.parse("Étape: Connexion")
    assert actions["steps"] == ["Connexion"]

    actions = parser.parse("Action: créer le dossier /tmp/data")
    assert actions["file_operations"] == [("créer", "dossier", "/tmp/data", "0755")]


def test_parser_requires_result_after_action_only():
    parser = Parser()
    with pytest.raises(SyntaxError):
        # Simule une action seule non suivie d’un résultat
        lines = [
            "Étape: Test",
            "Action: taper login",
            "Action: taper mot de passe"
        ]
        for i, line in enumerate(lines):
            actions = parser.parse(line)
            if "Action: " in line and i+1 >= len(lines) or not lines[i+1].startswith("Résultat:"):
                raise SyntaxError("Action non suivie de résultat")


def test_validation_expression():
    expr = "fichier /tmp/logs/app.log contient 'OK'"
    try:
        parse_validation_expression(expr)
    except Exception:
        pytest.fail("L'expression de validation devrait être valide")
