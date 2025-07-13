import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from generate_tests import parse_shtest_file, generate_shell_script


class TestGenerateShellScript(unittest.TestCase):
    def test_variable_export(self):
        content = (
            "Action: Définir la variable SQL_CONN = sqlplus -S user/password@db ; "
            "Résultat: identifiants configurés."
        )
        actions = parse_shtest_file(content)
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
        actions = parse_shtest_file(content)
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
        actions = parse_shtest_file(content)
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
        actions = parse_shtest_file(content)
        script = generate_shell_script(actions)
        self.assertIn('cond1', script)
        self.assertIn('cond2', script)

    def test_sql_driver_override(self):
        content = (
            "Action: Définir la variable SQL_DRIVER = mysql ;\n"
            "Action: Exécuter le script SQL init.sql ;"
        )
        actions = parse_shtest_file(content)
        script = generate_shell_script(actions)
        self.assertIn(
            "mysql ${SQL_CONN:-user/password@db} < init.sql",
            script,
        )

    def test_sql_driver_mysql(self):
        import os
        os.environ["SQL_DRIVER"] = "mysql"
        content = (
            "Action: Définir la variable SQL_CONN = root/test@db ;\n"
            "Action: Exécuter le script SQL test.sql ;"
        )
        actions = parse_shtest_file(content)
        script = generate_shell_script(actions)
        self.assertIn(
            "mysql ${SQL_CONN:-user/password@db} < test.sql",
            script,
        )
        del os.environ["SQL_DRIVER"]

    def test_sql_driver_postgres(self):
        import os
        os.environ["SQL_DRIVER"] = "postgres"
        content = (
            "Action: Définir la variable SQL_CONN = root/test@db ;\n"
            "Action: Exécuter le script SQL test.sql ;"
        )
        actions = parse_shtest_file(content)
        script = generate_shell_script(actions)
        self.assertIn(
            "psql \"$SQL_URL\" -f test.sql",
            script,
        )
        del os.environ["SQL_DRIVER"]

    def test_sql_driver_oracle_default(self):
        import os
        if "SQL_DRIVER" in os.environ:
            del os.environ["SQL_DRIVER"]
        content = (
            "Action: Définir la variable SQL_CONN = root/test@db ;\n"
            "Action: Exécuter le script SQL test.sql ;"
        )
        actions = parse_shtest_file(content)
        script = generate_shell_script(actions)
        self.assertIn(
            "sqlplus -s ${SQL_CONN:-user/password@db} @test.sql",
            script,
        )

    def test_sql_driver_redis(self):
        import os
        os.environ["SQL_DRIVER"] = "redis"
        content = (
            "Action: Définir la variable SQL_CONN = -h myhost -p 6380 -a mypass ;\n"
            "Action: Exécuter le script SQL mon_script.redis ;"
        )
        actions = parse_shtest_file(content)
        script = generate_shell_script(actions)
        self.assertIn(
            "redis-cli -h myhost -p 6380 -a mypass < mon_script.redis",
            script,
        )
        del os.environ["SQL_DRIVER"]


if __name__ == "__main__":
    unittest.main()
