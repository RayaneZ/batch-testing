
import argparse
from shtest_compiler.parser.lexer import lex_file
from shtest_compiler.parser.parser import Parser
from shtest_compiler.compiler.compiler import compile_validation

def compile_file(path: str, verbose: bool = False):
    parser = Parser()
    counter = [0]
    result = []
    current_step = ""
    for token in lex_file(path):
        if verbose:
            print(f"[LEX] {token.kind}: {token.value}")
        if token.kind == "STEP":
            current_step = token.value
            continue
        if token.kind in {"ACTION_RESULT", "RESULT_ONLY", "ACTION_ONLY"}:
            action_line = (
                f"Action: {token.value} ; Résultat: {token.result}"
                if token.kind == "ACTION_RESULT"
                else f"Action: {token.value}"
                if token.kind == "ACTION_ONLY"
                else f"Résultat: {token.value}"
            )
            actions = parser.parse(action_line)
            for expr in actions.get("validation", []):
                result.extend(compile_validation(expr, counter=counter, verbose=verbose))
    return result

def main():
    parser = argparse.ArgumentParser(description="Compiler un fichier .shtest en script shell.")
    parser.add_argument("file", help="Chemin vers le fichier .shtest à compiler")
    parser.add_argument("--verbose", action="store_true", help="Afficher les étapes de compilation")
    parser.add_argument("--output", help="Fichier de sortie pour le script généré")
    args = parser.parse_args()

    lines = compile_file(args.file, verbose=args.verbose)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"[✔] Script sauvegardé dans {args.output}")
    else:
        print("\n".join(lines))

if __name__ == "__main__":
    main()
