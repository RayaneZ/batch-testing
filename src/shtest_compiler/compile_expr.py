import argparse
from shtest_compiler.compiler.utils import compile_validation


def main():
    parser = argparse.ArgumentParser(description="Compile une expression de validation en shell")
    parser.add_argument("expression", help="Expression de test à compiler (ex: 'retour 0 et stdout contient OK')")
    parser.add_argument("--verbose", action="store_true", help="Afficher les étapes de compilation")

    args = parser.parse_args()

    lines = compile_validation(args.expression, verbose=args.verbose)
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
