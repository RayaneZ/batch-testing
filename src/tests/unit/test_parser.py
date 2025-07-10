
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from parser.parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_step_parsing(self):
        result = self.parser.parse("Étape: Chargement")
        self.assertIn("Chargement", result["steps"])

    def test_argument_parsing(self):
        result = self.parser.parse("argument fichier=test.txt")
        self.assertEqual(result["arguments"].get("fichier"), "test.txt")

    def test_action_result_parsing(self):
        text = "Action: exécuter init.sql ; Résultat: le script retourne un code 0"
        result = self.parser.parse(text)
        self.assertIn("init.sql", result["sql_scripts"])
        self.assertIn("retour 0", result["validation"])

    def test_ignore_comment(self):
        text = "# ceci est un commentaire\nAction: echo test"
        result = self.parser.parse(text)
        self.assertEqual(result["execution"], [])

    def test_batch_path_detection(self):
        result = self.parser.parse("exécuter mon_script.sh")
        self.assertEqual(result["batch_path"], "mon_script.sh")

    def test_file_operations(self):
        result = self.parser.parse("créer le fichier = /tmp/test.txt")
        self.assertIn(("créer", "fichier", "/tmp/test.txt", "0644"), result["file_operations"])

    def test_copy_operation(self):
        result = self.parser.parse("copier fichier /tmp/a.txt vers /tmp/b.txt")
        self.assertIn(("copier", "fichier", "/tmp/a.txt", "/tmp/b.txt"), result["copy_operations"])

    def test_validation_alias(self):
        result = self.parser.parse("Résultat: le contenu est affiché")
        self.assertIn("contenu affiché", result["validation"])

    def test_variable_assignment(self):
        result = self.parser.parse("Définir la variable SQL_CONN = sqlplus -S user/password@db")
        self.assertEqual(result["arguments"].get("SQL_CONN"), "sqlplus -S user/password@db")

    def test_multiple_sql_scripts(self):
        text = "Action: Exécuter le script SQL JDD_Commun.sql puis JDD_Extra.sql ;"
        result = self.parser.parse(text)
        self.assertIn("JDD_Commun.sql", result["sql_scripts"])
        self.assertIn("JDD_Extra.sql", result["sql_scripts"])

    def test_identifiants_alias(self):
        result = self.parser.parse("Résultat: Les identifiants sont configurés")
        self.assertIn("identifiants configurés", result["validation"])

    def test_dossier_cree_alias(self):
        result = self.parser.parse("Résultat: Le dossier est créé")
        self.assertIn("dossier créé", result["validation"])

    def test_fichier_cree_alias(self):
        result = self.parser.parse("Résultat: le fichier est créé")
        self.assertIn("fichier cree", result["validation"])

if __name__ == "__main__":
    unittest.main()
