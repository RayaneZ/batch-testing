import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from compiler.compiler import compile_validation

class TestValidationCompiler(unittest.TestCase):

    def test_base_ready(self):
        lines = compile_validation("base prête")
        self.assertTrue(any("base prête" in line for line in lines))

    def test_file_exists(self):
        lines = compile_validation("le fichier test.txt existe")
        self.assertTrue(any("test.txt" in line for line in lines))

if __name__ == "__main__":
    unittest.main()