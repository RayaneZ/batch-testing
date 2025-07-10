import argparse
import sys
import os
import configparser

from shtest_compiler.generate_tests import generate_tests
from shtest_compiler.export_to_excel import export_tests_to_excel
from shtest_compiler.verify_syntax import check_file
from shtest_compiler.parser.parser import Parser

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.ini")

def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    input_dir = config.get("application", "input_dir", fallback="tests")
    output_dir = config.get("application", "output_dir", fallback="output")
    sql_driver = config.get("application", "sql_driver", fallback="oracle")
    return input_dir, output_dir, sql_driver

def run_syntax_check(input_dir: str):
    print("[1/3] Vérification de la syntaxe...")
    parser = Parser()
    all_errors = []

    if os.path.isdir(input_dir):
        for name in os.listdir(input_dir):
            if name.endswith(".shtest"):
                full = os.path.join(input_dir, name)
                print(f"[1/3] Vérification de {full}")
                all_errors.extend(check_file(full, parser))
                
    else:
        print(f"[1/3] Vérification de {input_dir}")
        all_errors.extend(check_file(input_dir, parser))

    if all_errors:
        print("\n".join(all_errors))
        sys.exit("❌ Erreurs détectées. Interruption.")
    print("✅ Syntaxe valide.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Répertoire d'entrée (.shtest)")
    parser.add_argument("--output", help="Répertoire de sortie des scripts")
    parser.add_argument("--excel", help="Chemin du fichier Excel à générer")
    parser.add_argument("--no-shell", action="store_true", help="Ne pas générer les scripts shell")
    parser.add_argument("--no-excel", action="store_true", help="Ne pas générer le fichier Excel")
    args = parser.parse_args()

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

    print("✅ Terminé avec succès.")

if __name__ == "__main__":
    main()
