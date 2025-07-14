import argparse
from shtest_compiler.parser.configurable_parser import ConfigurableParser


def check_file(file_path: str, debug: bool = False) -> bool:
    """Check the syntax of a single .shtest file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        parser = ConfigurableParser(debug=debug)
        parser.parse(content, path=file_path)
        return True

    except Exception as e:
        if debug:
            print(f"[ERROR] Erreur de syntaxe dans {file_path}: {e}")
        # Re-raise the exception so it propagates up
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Vérifie uniquement la syntaxe d'un fichier .shtest"
    )
    parser.add_argument("file", help="Fichier .shtest à vérifier")
    parser.add_argument(
        "--verbose", action="store_true", help="Afficher les détails du parsing"
    )

    args = parser.parse_args()

    try:
        if check_file(args.file, debug=args.verbose):
            print("[✔] Syntaxe valide.")
        else:
            print("[ERROR] Erreur de syntaxe.")
            exit(1)
    except Exception as e:
        print(f"[ERROR] Erreur de syntaxe: {e}")
        exit(1)


if __name__ == "__main__":
    main()
