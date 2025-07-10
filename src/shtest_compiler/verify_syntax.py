from shtest_compiler.common_patterns import LINE_FORMATS, VALIDATION_KEY
from typing import List
from shtest_compiler.parser.parser import Parser
from shtest_compiler.parser.shunting_yard import parse_validation_expression
from src.shtest_compiler.parser.lexer import lex_file


def _is_actions_empty(actions: dict) -> bool:
    """
    Vérifie si un dictionnaire d'actions est vide ou non significatif.
    """
    for key, value in actions.items():
        if key == "batch_path":
            if value:
                return False
        elif value:
            return False
    return True


def format_line(token) -> str:
    """
    Utilise LINE_FORMATS pour formater dynamiquement la ligne en fonction du type de token.
    """
    fmt = LINE_FORMATS.get(token.kind.lower(), "{value}")
    return fmt.format(value=token.value, result=token.result or "")


def validate_actions(path: str, token, line: str, parser: Parser, errors: List[str]) -> bool:
    """
    Tente de parser et valider une ligne. Retourne True si une action a été reconnue.
    """
    actions = parser.parse(line)
    if _is_actions_empty(actions):
        errors.append(f"{path}:{token.lineno}: ligne non reconnue -> {line}")
        return False

    for expr in actions.get(VALIDATION_KEY, []):
        try:
            parse_validation_expression(expr)
        except Exception as exc:
            errors.append(
                f"{path}:{token.lineno}: expression invalide -> {expr} ({exc})"
            )

    return True


def check_file(path: str, parser: Parser) -> List[str]:
    """
    Analyse un fichier .shtest et retourne une liste d'erreurs de syntaxe.
    Vérifie aussi que chaque 'Action:' est suivie d'un 'Résultat:'.
    """
    errors: List[str] = []
    current_step_lineno = None
    current_step_name = ""
    step_has_action = False
    previous_action_only_token = None  # Pour vérifier la règle action_only → result_only

    for token in lex_file(path):
        kind = token.kind.lower()

        # Vérifie que l'action_only précédente est suivie d'un result_only
        if previous_action_only_token:
            if kind != "result_only":
                errors.append(
                    f"{path}:{previous_action_only_token.lineno}: "
                    f"'Action' non suivie d'un 'Résultat'"
                )
            previous_action_only_token = None

        if kind == "step":
            if current_step_lineno and not step_has_action:
                errors.append(
                    f"{path}:{current_step_lineno}: étape sans action -> {current_step_name}"
                )
            current_step_lineno = token.lineno
            current_step_name = token.value
            step_has_action = False

            line = format_line(token)
            validate_actions(path, token, line, parser, errors)
            continue

        if kind in LINE_FORMATS:
            if current_step_lineno is None:
                msg = "action sans étape" if kind != "result_only" else "résultat sans étape"
                errors.append(f"{path}:{token.lineno}: {msg} -> {token.original or token.value}")

            line = format_line(token)
            if validate_actions(path, token, line, parser, errors):
                step_has_action = True

            # Mémoriser les action_only pour vérif à la prochaine ligne
            if kind == "action_only":
                previous_action_only_token = token

            continue

        # Ligne non reconnue
        errors.append(f"{path}:{token.lineno}: ligne non reconnue -> {token.value}")

    if current_step_lineno and not step_has_action:
        errors.append(
            f"{path}:{current_step_lineno}: étape sans action -> {current_step_name}"
        )

    return errors


def main() -> None:
    """Point d'entrée CLI pour la vérification de syntaxe."""
    import argparse
    import os
    import sys

    parser = argparse.ArgumentParser(
        description="Vérifie la syntaxe des fichiers .shtest"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="tests",
        help="Fichier ou dossier à analyser",
    )
    args = parser.parse_args()

    parser_obj = Parser()
    all_errors: List[str] = []

    if os.path.isdir(args.path):
        for name in os.listdir(args.path):
            if name.endswith(".shtest"):
                full = os.path.join(args.path, name)
                print(f"Vérification de {full}")
                all_errors.extend(check_file(full, parser_obj))
    else:
        print(f"Vérification de {args.path}")
        all_errors.extend(check_file(args.path, parser_obj))

    if all_errors:
        print("\n".join(all_errors))
        sys.exit("❌ Erreurs détectées")

    print("✅ Syntaxe valide")


if __name__ == "__main__":
    main()
