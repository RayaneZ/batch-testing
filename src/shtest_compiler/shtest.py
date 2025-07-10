
import argparse
from shtest_compiler.compile_expr import compile_expr
from shtest_compiler.compile_file import compile_file
from shtest_compiler.generate_tests import generate_tests

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

    # Subcommande generate_tests
    parser_gen = subparsers.add_parser("generate", help="Générer des scripts à partir d'un répertoire de fichiers .shtest")
    parser_gen.add_argument("input_dir", help="Répertoire contenant les fichiers .shtest")
    parser_gen.add_argument("output_dir", help="Répertoire où écrire les scripts générés")

    args = parser.parse_args()

    if args.command == "compile_expr":
        lines = compile_expr(args.expression, verbose=args.verbose)
        print("\n".join(lines))
    elif args.command == "compile_file":
        lines = compile_file(args.file, verbose=args.verbose)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            print(f"[✔] Script sauvegardé dans {args.output}")
        else:
            print("\n".join(lines))
    elif args.command == "generate":
        generate_tests(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
