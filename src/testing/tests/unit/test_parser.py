import pytest

from shtest_compiler.parser.configurable_parser import ConfigurableParser


def test_parse_minimal():
    parser = ConfigurableParser(debug=False)
    description = """
Step: Preparation
Action: Creer le dossier ./demo
Resultat: le dossier est cree.
"""
    shtest = parser.parse(description)
    assert shtest.steps
    assert shtest.steps[0].name == "Preparation"
    assert shtest.steps[0].actions[0].command.startswith("Creer le dossier")
    # Check result_expr if it exists
    if shtest.steps[0].actions[0].result_expr:
        assert "cree" in shtest.steps[0].actions[0].result_expr
