import argparse
import sys

from shtest_compiler.compile_expr import compile_validation
from shtest_compiler.compile_file import compile_file
from shtest_compiler.export_to_excel import export_patterns_to_excel
from shtest_compiler.verify_syntax import main as verify_main
from shtest_compiler.utils.logger import debug_log, set_debug, log_pipeline_error


def main():
    parser = argparse.ArgumentParser(
        prog="shtest", description="Outils CLI pour les fichiers .shtest"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode for detailed logging (can be used anywhere)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommande compile_expr
    parser_expr = subparsers.add_parser(
        "compile_expr", help="Compiler une expression de validation"
    )
    parser_expr.add_argument("expression", help="Expression à compiler")
    parser_expr.add_argument(
        "--verbose", action="store_true", help="Afficher les étapes de compilation"
    )
    parser_expr.add_argument(
        "--debug", action="store_true", help="Enable debug mode for detailed logging"
    )

    # Subcommande compile_file
    parser_file = subparsers.add_parser(
        "compile_file", help="Compiler un fichier .shtest"
    )
    parser_file.add_argument("file", help="Chemin vers le fichier .shtest")
    parser_file.add_argument(
        "--verbose", action="store_true", help="Afficher les étapes de compilation"
    )
    parser_file.add_argument("--output", help="Fichier de sortie pour le script généré")
    parser_file.add_argument(
        "--debug", action="store_true", help="Enable debug mode for detailed logging"
    )

    # Subcommande verify_syntax
    parser_verify = subparsers.add_parser(
        "verify", help="Vérifier uniquement la syntaxe d'un fichier .shtest"
    )
    parser_verify.add_argument("file", help="Fichier .shtest à vérifier")
    parser_verify.add_argument(
        "--verbose", action="store_true", help="Afficher les détails du parsing"
    )
    parser_verify.add_argument(
        "--debug", action="store_true", help="Enable debug mode for detailed logging"
    )

    # Subcommande to_excel
    parser_excel = subparsers.add_parser(
        "to_excel",
        help="Exporter les patterns (actions/validations) vers un fichier Excel",
    )
    parser_excel.add_argument("actions_yml", help="Chemin vers le YAML des actions")
    parser_excel.add_argument(
        "validations_yml", help="Chemin vers le YAML des validations"
    )
    parser_excel.add_argument("output_xlsx", help="Fichier Excel de sortie")
    parser_excel.add_argument(
        "--verbose", action="store_true", help="Afficher les détails de l'export"
    )
    parser_excel.add_argument(
        "--debug", action="store_true", help="Enable debug mode for detailed logging"
    )

    # Use parse_known_args to allow --debug anywhere
    args, unknown = parser.parse_known_args()

    # If --debug is present anywhere, enable debug globally
    debug_flag = getattr(args, "debug", False) or "--debug" in unknown
    set_debug(debug_flag)
    debug_log("ENTRYPOINT DEBUG ACTIVE: src/shtest_compiler/shtest.py loaded")

    # Re-parse with all args for subcommand
    if unknown:
        # Merge unknowns into sys.argv for subparser
        sub_args = sys.argv[1:]
        args = parser.parse_args(sub_args)

    if args.command == "compile_expr":
        lines = compile_validation(
            args.expression, verbose=args.verbose or getattr(args, "debug", False)
        )
        print("\n".join(lines))

    elif args.command == "compile_file":
        try:
            output_path = compile_file(
                input_path=args.file,
                output_path=args.output,
                grammar=getattr(args, "grammar", "default"),
                ast_builder=getattr(args, "ast_builder", "default"),
                debug=debug_flag,
                debug_output_path=getattr(args, "debug_output_path", None),
            )
        except Exception as e:
            import traceback
            from shtest_compiler.parser.core import ParseError
            if isinstance(e, ParseError) and "no actions" in str(e).lower():
                log_pipeline_error(
                    f"[USER ERROR] The test file appears empty or has a step with no actions.\n"
                    f"Please add at least one action to each step.\n"
                    f"Example: Créer le fichier test.txt\n\n"
                    f"Original error: {e}"
                )
            else:
                log_pipeline_error(f"[ERROR] {type(e).__name__}: {e}\n{traceback.format_exc()}")
            raise
        if not args.output:
            print(f"Compiled file: {output_path}")

    elif args.command == "verify":
        # Pass the file argument to verify_syntax

        # Temporarily modify sys.argv to pass the file argument
        original_argv = sys.argv.copy()
        sys.argv = [sys.argv[0], args.file]
        if args.verbose:
            sys.argv.append("--verbose")
        if getattr(args, "debug", False):
            sys.argv.append("--debug")

        try:
            verify_main()
        finally:
            # Restore original sys.argv
            sys.argv = original_argv

    elif args.command == "to_excel":
        if args.verbose or getattr(args, "debug", False):
            print(f"Export des patterns vers {args.output_xlsx}...")
        export_patterns_to_excel(
            args.actions_yml, args.validations_yml, args.output_xlsx
        )


if __name__ == "__main__":
    import sys
    from shtest_compiler.utils.logger import log_pipeline_error
    def _log_excepthook(exc_type, exc_value, exc_traceback):
        import traceback
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        log_pipeline_error(f"[UNCAUGHT EXCEPTION] {exc_type.__name__}: {exc_value}\n{''.join(traceback.format_tb(exc_traceback))}")
    sys.excepthook = _log_excepthook
    try:
        main()
    except Exception as e:
        import traceback
        log_pipeline_error(f"[FATAL ERROR] {type(e).__name__}: {e}\n{traceback.format_exc()}")
        raise
