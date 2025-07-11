import argparse
from shtest_compiler.parser.parser import Parser


def main():
    parser = argparse.ArgumentParser(description="Vérifie uniquement la syntaxe d'un fichier .shtest")
    parser.add_argument("file", help="Fichier .shtest à vérifier")
    parser.add_argument("--verbose", action="store_true", help="Afficher les détails du parsing")

    args = parser.parse_args()

    try:
        with open(args.file, encoding="utf-8") as f:
            content = f.read()

        parser = Parser()
        parser.parse(content, path=args.file, debug=args.verbose)

        print("[✔] Syntaxe valide.")

    except Exception as e:
        print("[❌] Erreur de syntaxe :", e)
        exit(1)


if __name__ == "__main__":
    main()
