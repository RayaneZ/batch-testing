import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import verify_syntax
from parser.parser import Parser


class TestVerifySyntax(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def _write_temp(self, content: str) -> str:
        tmp = tempfile.NamedTemporaryFile('w', delete=False, suffix='.shtest')
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_invalid_line_number(self):
        path = self._write_temp("Étape: S\nAction: Définir la variable X = 1\nblabla\n")
        try:
            errors = verify_syntax.check_file(path, self.parser)
        finally:
            os.unlink(path)
        self.assertEqual(len(errors), 1)
        self.assertIn(':3:', errors[0])

    def test_empty_step_error(self):
        path = self._write_temp("Étape: A\nÉtape: B\nAction: echo\n")
        try:
            errors = verify_syntax.check_file(path, self.parser)
        finally:
            os.unlink(path)
        self.assertTrue(any(':1:' in e and 'étape sans action' in e for e in errors))

    def test_action_without_step(self):
        path = self._write_temp("Action: echo 1\n")
        try:
            errors = verify_syntax.check_file(path, self.parser)
        finally:
            os.unlink(path)
        self.assertTrue(any('action sans étape' in e for e in errors))

    def test_result_without_step(self):
        path = self._write_temp("Résultat: retour 0\n")
        try:
            errors = verify_syntax.check_file(path, self.parser)
        finally:
            os.unlink(path)
        self.assertTrue(any('résultat sans étape' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
