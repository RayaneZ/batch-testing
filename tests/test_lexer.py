import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer import lex

class TestLexerNested(unittest.TestCase):
    def test_nested_action_result(self):
        text = "Action: Exécuter script.sh ; Résultat: base prête."
        tokens = list(lex(text, nested=True))
        self.assertEqual(tokens[0].kind, "ACTION_RESULT")
        self.assertEqual(tokens[0].value, "Exécuter script.sh ;")
        self.assertEqual(tokens[0].result, "base prête.")
        kinds = [t.kind for t in tokens]
        self.assertIn("ACTION_EXPR", kinds)
        self.assertIn("RESULT_EXPR", kinds)

    def test_nested_action_only(self):
        text = "Action: echo hello"
        tokens = list(lex(text, nested=True))
        self.assertEqual(tokens[0].kind, "ACTION_ONLY")
        self.assertEqual(tokens[0].value, "echo hello")
        kinds = [t.kind for t in tokens]
        self.assertIn("ACTION_EXPR", kinds)

if __name__ == '__main__':
    unittest.main()
