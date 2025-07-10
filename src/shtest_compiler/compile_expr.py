
import argparse
from shtest_compiler.compiler.compiler import compile_validation

def main():
    parser = argparse.ArgumentParser(description="Compiler une expression de validation en shell.")
    parser.add_argument("expression", help="Expression à compiler, ex: 'fichier /tmp/x contient OK'")
    parser.add_argument("--verbose", action="store_true", help="Afficher les étapes de compilation")

    args = parser.parse_args()
    lines = compile_validation(args.expression, verbose=args.verbose)
    print("\n".join(lines))

if __name__ == "__main__":
    main()
