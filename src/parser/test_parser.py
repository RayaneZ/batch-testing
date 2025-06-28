
import unittest
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
        text = "Action: exécuter init.sql Résultat: le script retourne un code 0"
        result = self.parser.parse(text)
        self.assertIn("init.sql", result["sql_scripts"])
        self.assertIn("retour 0", result["validation"])

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

if __name__ == "__main__":
    unittest.main()
