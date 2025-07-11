import argparse
from shtest_compiler.compile_expr import compile_validation
from shtest_compiler.compile_file import compile_file
from shtest_compiler.verify_syntax import main as verify_main


def main():
    parser = argparse.ArgumentParser(prog="shtest", description="Outils CLI pour les fichiers .shtest")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommande compile_expr
    parser_expr = subparsers.add_parser("compile_expr", help="Compiler une expression de validation")
    parser_expr.add_argument("expression", help="Expression à compiler")
    parser_expr.add_argument("--verbose", action="store_true", help="Afficher les étapes de compilation")

    # Subcommande compile_file
    parser_file = subparsers.add_parser("compile_file", help="Compiler un fichier .shtest")
    parser_file.add_argument("file", help="Chemin vers le fichier .shtest")
    parser_file.add_argument("--verbose", action="store_true", help="Afficher les étapes de compilation")
    parser_file.add_argument("--output", help="Fichier de sortie pour le script généré")

    # Subcommande verify_syntax
    parser_verify = subparsers.add_parser("verify", help="Vérifier uniquement la syntaxe d'un fichier .shtest")
    parser_verify.add_argument("file", help="Fichier .shtest à vérifier")
    parser_verify.add_argument("--verbose", action="store_true", help="Afficher les détails du parsing")

    args = parser.parse_args()

    if args.command == "compile_expr":
        lines = compile_validation(args.expression, verbose=args.verbose)
        print("\n".join(lines))

    elif args.command == "compile_file":
        lines = compile_file(args.file, debug=args.verbose, output_path=args.output)
        if not args.output:
            print("\n".join(lines))

    elif args.command == "verify":
        verify_main()


if __name__ == "__main__":
    main()
