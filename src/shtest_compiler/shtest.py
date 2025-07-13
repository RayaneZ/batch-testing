import argparse
from shtest_compiler.compile_expr import compile_validation
from shtest_compiler.compile_file import compile_file
from shtest_compiler.verify_syntax import main as verify_main
from shtest_compiler.export_to_excel import export_patterns_to_excel
from shtest_compiler.config.debug_config import set_debug, debug_print
import sys


def main():
    parser = argparse.ArgumentParser(prog="shtest", description="Outils CLI pour les fichiers .shtest")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode for detailed logging (can be used anywhere)")
    
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommande compile_expr
    parser_expr = subparsers.add_parser("compile_expr", help="Compiler une expression de validation")
    parser_expr.add_argument("expression", help="Expression à compiler")
    parser_expr.add_argument("--verbose", action="store_true", help="Afficher les étapes de compilation")
    parser_expr.add_argument("--debug", action="store_true", help="Enable debug mode for detailed logging")

    # Subcommande compile_file
    parser_file = subparsers.add_parser("compile_file", help="Compiler un fichier .shtest")
    parser_file.add_argument("file", help="Chemin vers le fichier .shtest")
    parser_file.add_argument("--verbose", action="store_true", help="Afficher les étapes de compilation")
    parser_file.add_argument("--output", help="Fichier de sortie pour le script généré")
    parser_file.add_argument("--debug", action="store_true", help="Enable debug mode for detailed logging")

    # Subcommande verify_syntax
    parser_verify = subparsers.add_parser("verify", help="Vérifier uniquement la syntaxe d'un fichier .shtest")
    parser_verify.add_argument("file", help="Fichier .shtest à vérifier")
    parser_verify.add_argument("--verbose", action="store_true", help="Afficher les détails du parsing")
    parser_verify.add_argument("--debug", action="store_true", help="Enable debug mode for detailed logging")

    # Subcommande to_excel
    parser_excel = subparsers.add_parser("to_excel", help="Exporter les patterns (actions/validations) vers un fichier Excel")
    parser_excel.add_argument("actions_yml", help="Chemin vers le YAML des actions")
    parser_excel.add_argument("validations_yml", help="Chemin vers le YAML des validations")
    parser_excel.add_argument("output_xlsx", help="Fichier Excel de sortie")
    parser_excel.add_argument("--verbose", action="store_true", help="Afficher les détails de l'export")
    parser_excel.add_argument("--debug", action="store_true", help="Enable debug mode for detailed logging")

    # Use parse_known_args to allow --debug anywhere
    args, unknown = parser.parse_known_args()

    # If --debug is present anywhere, enable debug globally
    debug_flag = getattr(args, 'debug', False) or '--debug' in unknown
    set_debug(debug_flag)
    debug_print("ENTRYPOINT DEBUG ACTIVE: src/shtest_compiler/shtest.py loaded")

    # Re-parse with all args for subcommand
    if unknown:
        # Merge unknowns into sys.argv for subparser
        sub_args = sys.argv[1:]
        args = parser.parse_args(sub_args)

    if args.command == "compile_expr":
        lines = compile_validation(args.expression, verbose=args.verbose or getattr(args, 'debug', False))
        print("\n".join(lines))

    elif args.command == "compile_file":
        output_path = compile_file(args.file, debug=args.verbose or getattr(args, 'debug', False), output_path=args.output)
        if not args.output:
            print(f"Compiled file: {output_path}")

    elif args.command == "verify":
        # Pass the file argument to verify_syntax
        import sys
        # Temporarily modify sys.argv to pass the file argument
        original_argv = sys.argv.copy()
        sys.argv = [sys.argv[0], args.file]
        if args.verbose:
            sys.argv.append("--verbose")
        if getattr(args, 'debug', False):
            sys.argv.append("--debug")
        
        try:
            verify_main()
        finally:
            # Restore original sys.argv
            sys.argv = original_argv

    elif args.command == "to_excel":
        if args.verbose or getattr(args, 'debug', False):
            print(f"Export des patterns vers {args.output_xlsx}...")
        export_patterns_to_excel(args.actions_yml, args.validations_yml, args.output_xlsx)

if __name__ == "__main__":
    main()
