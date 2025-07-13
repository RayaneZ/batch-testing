import pytest
from shtest_compiler.parser.parser import Parser

def test_parse_minimal():
    parser = Parser()
    description = """
Step: Préparation
Action: Créer le dossier ./demo
Résultat: le dossier est cree.
"""
    shtest = parser.parse(description)
    assert shtest.steps
    assert shtest.steps[0].name == "Préparation"
    assert shtest.steps[0].actions[0].command.startswith("Créer le dossier")
    assert "cree" in shtest.steps[0].actions[0].result_expr 