import argparse
import os
import configparser
from typing import List

from parser.parser import Parser
from parser.shunting_yard import parse_validation_expression
from lexer import lex_file

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.ini")
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

DEFAULT_INPUT_DIR = config.get("application", "input_dir", fallback="src/tests")


def _is_actions_empty(actions: dict) -> bool:
    for key, value in actions.items():
        if key == "batch_path":
            if value:
                return False
        elif value:
            return False
    return True


def check_file(path: str, parser: Parser) -> List[str]:
    """Return a list of syntax errors found in *path*."""
    errors: List[str] = []
    current_step_lineno: int | None = None
    current_step_name: str = ""
    step_has_action = False

    for token in lex_file(path):
        if token.kind == "STEP":
            # Report an empty step before starting a new one
            if current_step_lineno is not None and not step_has_action:
                errors.append(
                    f"{path}:{current_step_lineno}: \u00e9tape sans action -> {current_step_name}"
                )
            current_step_lineno = token.lineno
            current_step_name = token.value
            step_has_action = False
            line = f"\u00c9tape: {token.value}"
            actions = parser.parse(line)
            if _is_actions_empty(actions):
                errors.append(f"{path}:{token.lineno}: ligne non reconnue -> {line}")
            continue

        if token.kind in ("ACTION_RESULT", "ACTION_ONLY"):
            if current_step_lineno is None:
                errors.append(
                    f"{path}:{token.lineno}: action sans \u00e9tape -> {token.original or token.value}"
                )
            line = (
                f"Action: {token.value} ; R\u00e9sultat: {token.result}"
                if token.kind == "ACTION_RESULT"
                else f"Action: {token.value}"
            )
            actions = parser.parse(line)
            if _is_actions_empty(actions):
                errors.append(f"{path}:{token.lineno}: ligne non reconnue -> {line}")
            for expr in actions.get("validation", []):
                try:
                    parse_validation_expression(expr)
                except Exception as exc:  # pragma: no cover - unexpected failures
                    errors.append(
                        f"{path}:{token.lineno}: expression invalide -> {expr} ({exc})"
                    )
            step_has_action = True
            continue

        # Any other token is unrecognised text
        errors.append(f"{path}:{token.lineno}: ligne non reconnue -> {token.value}")

    if current_step_lineno is not None and not step_has_action:
        errors.append(
            f"{path}:{current_step_lineno}: \u00e9tape sans action -> {current_step_name}"
        )

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        default=[DEFAULT_INPUT_DIR],
        help="Files or directories to check",
    )
    args = parser.parse_args()

    p = Parser()
    all_errors: List[str] = []

    for path in args.paths:
        if os.path.isdir(path):
            for name in os.listdir(path):
                if name.endswith(".shtest"):
                    full = os.path.join(path, name)
                    all_errors.extend(check_file(full, p))
        else:
            all_errors.extend(check_file(path, p))

    if all_errors:
        print("\n".join(all_errors))
        raise SystemExit(1)

    print("Syntax OK")


if __name__ == "__main__":
    main()
