import argparse
import os
import configparser
from typing import List

from parser.parser import Parser
from parser.shunting_yard import parse_validation_expression

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
    errors: List[str] = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            text = line.strip()
            if not text or text.startswith("#"):
                continue
            actions = parser.parse(text)
            if _is_actions_empty(actions):
                errors.append(f"{path}:{lineno}: ligne non reconnue -> {text}")
                continue
            for expr in actions.get("validation", []):
                try:
                    parse_validation_expression(expr)
                except Exception as exc:  # pragma: no cover - unexpected failures
                    errors.append(
                        f"{path}:{lineno}: expression invalide -> {expr} ({exc})"
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
