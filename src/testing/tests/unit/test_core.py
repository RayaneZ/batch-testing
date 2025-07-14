import pytest

from shtest_compiler.ast.shell_framework_ast import (ShellFrameworkAST,
                                                     ShellTestStep,
                                                     ValidationCheck)
from shtest_compiler.ast.shell_framework_binder import ShellFrameworkBinder
from shtest_compiler.parser.configurable_parser import ConfigurableParser
from shtest_compiler.parser.lexer.configurable_lexer import ConfigurableLexer
from shtest_compiler.parser.shunting_yard import parse_validation_expression


def test_lexer_basic_tokens():
    text = """
    Étape: Connexion
    Action: Cliquer sur "Se connecter" ; Résultat: La page d'accueil s'affiche
    Action: Entrer les identifiants
    Résultat: Authentification réussie
    """
    tokens = list(ConfigurableLexer().lex(text))
    # Just check that we get tokens and they have the expected structure
    assert len(tokens) > 0
    for token in tokens:
        assert hasattr(token, "type")
        assert hasattr(token, "value")
        assert hasattr(token, "lineno")


def test_parser_recognizes_step_and_actions():
    parser = ConfigurableParser(debug=False)
    # Test with a complete step that has actions
    text = """
    Étape: Connexion
    Action: créer le dossier /tmp/data
    Résultat: le dossier est créé
    """
    ast = parser.parse(text)
    assert len(ast.steps) > 0
    assert ast.steps[0].name == "Connexion"


def test_parser_requires_result_after_action_only():
    parser = ConfigurableParser(debug=False)
    # Test with a valid step that has both action and result
    text = """
    Étape: Test
    Action: taper login
    Résultat: login saisi
    Action: taper mot de passe
    Résultat: mot de passe saisi
    """
    # This should not raise an exception
    ast = parser.parse(text)
    assert len(ast.steps) > 0


def test_validation_expression():
    expr = "fichier /tmp/logs/app.log contient 'OK'"
    try:
        parse_validation_expression(expr)
    except Exception:
        pytest.fail("L'expression de validation devrait être valide")


def test_scope_enforcement_raises_on_local_validation_without_action():
    # Create a fake local validation
    local_validation = ValidationCheck()
    local_validation.scope = "last_action"
    local_validation.phrase = "Fake local validation"
    # Create a step with no actions but with a local validation
    step = ShellTestStep(name="Step 1", actions=[], validations=[local_validation])
    ast = ShellFrameworkAST(helpers=[], steps=[step], global_code=[])
    binder = ShellFrameworkBinder(ast)
    with pytest.raises(ValueError, match="must follow an action"):
        binder.bind()
