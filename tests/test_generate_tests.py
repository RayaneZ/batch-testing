import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from generate_tests import parse_test_file, generate_shell_script


class TestGenerateShellScript(unittest.TestCase):
    def test_variable_export(self):
        content = (
            "Action: Définir la variable SQL_CONN = sqlplus -S user/password@db ; "
            "Résultat: identifiants configurés."
        )
        actions = parse_test_file(content)
        script = generate_shell_script(actions)
        self.assertIn(
            "export SQL_CONN=sqlplus -S user/password@db",
            script.splitlines(),
        )

    def test_skip_none_execution(self):
        content = (
            "Action: Exécuter le script SQL init_bdd.sql ; Résultat: base prête."
        )
        actions = parse_test_file(content)
        script = generate_shell_script(actions)
        self.assertNotIn('run_cmd "None"', script)


if __name__ == "__main__":
    unittest.main()
