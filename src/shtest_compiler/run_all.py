import argparse
import sys
import os
import configparser

from shtest_compiler.generate_tests import generate_tests
from shtest_compiler.export_to_excel import export_tests_to_excel
from shtest_compiler.verify_syntax import check_file
from shtest_compiler.parser.parser import Parser
from shtest_compiler.config.debug_config import set_debug, debug_print

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.ini")

def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    input_dir = config.get("application", "input_dir", fallback="tests")
    output_dir = config.get("application", "output_dir", fallback="output")
    sql_driver = config.get("application", "sql_driver", fallback="oracle")
    return input_dir, output_dir, sql_driver


def run_syntax_check(input_path):
    print("[1/3] Vérification de la syntaxe...")
    errors = []
    
    # Handle single file vs directory
    if os.path.isfile(input_path):
        files_to_check = [input_path]
    else:
        files_to_check = []
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if file.endswith('.shtest'):
                    files_to_check.append(os.path.join(root, file))
    
    for file_path in files_to_check:
        try:
            check_file(file_path)
        except Exception as e:
            errors.append(f"{file_path}: {e}")
    
    if errors:
        print("Erreurs de syntaxe détectées:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("Syntaxe OK")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Répertoire d'entrée (.shtest)")
    parser.add_argument("--output", help="Répertoire de sortie des scripts")
    parser.add_argument("--excel", help="Chemin du fichier Excel à générer")
    parser.add_argument("--no-shell", action="store_true", help="Ne pas générer les scripts shell")
    parser.add_argument("--no-excel", action="store_true", help="Ne pas générer le fichier Excel")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode for detailed logging")
    args = parser.parse_args()
    
    # Set global debug configuration
    set_debug(args.debug)
    if args.debug:
        os.environ["SHTEST_DEBUG"] = "1"

    config_input, config_output, config_driver = read_config()
    input_dir = args.input or config_input
    output_dir = args.output or config_output
    if "SQL_DRIVER" not in os.environ:
        os.environ["SQL_DRIVER"] = config_driver
    excel_file = args.excel or os.path.join(output_dir, "tests_summary.xlsx")

    run_syntax_check(input_dir)

    if not args.no_shell:
        print("[2/3] Génération des scripts...")
        generate_tests(input_dir=input_dir, output_dir=output_dir)

    if not args.no_excel:
        print("[3/3] Export Excel...")
        export_tests_to_excel(input_dir=input_dir, output_file=excel_file)

    print("Terminé avec succès.")

if __name__ == "__main__":
    main()
