import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

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
            'export SQL_CONN="sqlplus -S user/password@db"',
            script.splitlines(),
        )
        self.assertIn(
            'if [ -n "$SQL_CONN" ]; then actual="identifiants configurés"; else actual="non configuré"; fi',
            script,
        )

    def test_skip_none_execution(self):
        content = (
            "Action: Exécuter le script SQL init_bdd.sql ; Résultat: base prête."
        )
        actions = parse_test_file(content)
        script = generate_shell_script(actions)
        self.assertIn(
            "sqlplus -S ${SQL_CONN:-user/password@db} <<'EOF'",
            script,
        )

    def test_step_and_sql_validation(self):
        content = (
            "\u00c9tape: Pr\u00e9paration\n"
            "Action: Ex\u00e9cuter le script SQL init.sql ; R\u00e9sultat: base pr\u00eate."
        )
        actions = parse_test_file(content)
        script = generate_shell_script(actions)
        lines = script.splitlines()
        self.assertIn("# ---- Pr\u00e9paration ----", lines)
        self.assertTrue(any("init.sql" in line for line in lines))
        self.assertTrue(any("log_diff" in line for line in lines))

    def test_unique_condition_numbers(self):
        content = (
            "Action: Définir la variable X = 1 ; Résultat: identifiants configurés.\n"
            "Action: Exécuter /bin/true ; Résultat: retour 0."
        )
        actions = parse_test_file(content)
        script = generate_shell_script(actions)
        self.assertIn('cond1', script)
        self.assertIn('cond2', script)


if __name__ == "__main__":
    unittest.main()
