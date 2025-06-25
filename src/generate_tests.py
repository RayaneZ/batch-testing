"""Utilities to transform ``.shtest`` files into executable shell scripts."""

from parser import Parser
from templates import TEMPLATES
from validation_compiler import _compile_validation
import argparse
import os
from glob import glob
import re
import configparser


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.ini")
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

INPUT_DIR = config.get("application", "input_dir", fallback="src/tests")
OUTPUT_DIR = config.get("application", "output_dir", fallback="output")


def parse_test_file(contents: str):
    """Parse line by line and preserve ordering of actions/results."""

    parser = Parser()
    parsed_lines = []
    for line in contents.splitlines():
        # ``Parser.parse`` only deals with a single line. We keep the list
        # of results in order so that the generated script mirrors the
        # original description.
        parsed_lines.append(parser.parse(line))
    return parsed_lines




def generate_shell_script(actions_list):
    """Génère un script shell à partir de la liste ordonnée d'actions.

    Each item in *actions_list* corresponds to a line of the original
    ``.shtest`` file as produced by :func:`parse_test_file`.
    """
    lines = [
        "#!/bin/sh",
        "",
        "run_cmd() {",
        "  local _stdout=$(mktemp)",
        "  local _stderr=$(mktemp)",
        "  /bin/sh -c \"$1\" >\"$_stdout\" 2>\"$_stderr\"",
        "  last_ret=$?",
        "  last_stdout=$(cat \"$_stdout\")",
        "  last_stderr=$(cat \"$_stderr\")",
        "  rm -f \"$_stdout\" \"$_stderr\"",
        "}",
        "",
        "log_diff() {",
        "  expected=\"$1\"",
        "  actual=\"$2\"",
        "  if [ \"$expected\" != \"$actual\" ]; then",
        "    echo 'Différence détectée :'",
        "    echo \"- Attendu : $expected\"",
        "    echo \"- Obtenu : $actual\"",
        "  fi",
        "}",
        "",
    ]

    last_file = None
    for actions in actions_list:
        if actions["steps"]:
            lines.append(f"# ---- {actions['steps'][0]} ----")
            continue

        if actions["initialization"]:
            lines.append("# Initialisation")
            for action in actions["initialization"]:
                scripts = re.findall(r"\S+\.sql", action, re.IGNORECASE)
                if scripts:
                    for script in scripts:
                        cmd = TEMPLATES['execute_sql'].substitute(
                            script=script,
                            conn='${SQL_CONN:-user/password@db}'
                        )
                        lines.append(f"run_cmd \"{cmd}\"")
                else:
                    lines.append(f"run_cmd \"echo '{action}'\"")

        if actions["execution"]:
            arg_str = ' '.join([f'{k}={v}' for k, v in actions["arguments"].items()])
            actual_path = actions.get("batch_path")
            for action in actions["execution"]:
                cmd = actual_path if not arg_str else f"{actual_path} {arg_str}"
                lines.append(f"run_cmd \"{cmd}\"")

        if actions["sql_scripts"]:
            for script in actions["sql_scripts"]:
                cmd = TEMPLATES['execute_sql'].substitute(
                    script=script,
                    conn='${SQL_CONN:-user/password@db}'
                )
                lines.append(f"run_cmd \"{cmd}\"")

        if actions["file_operations"]:
            for operation, ftype, path, mode in actions["file_operations"]:
                if ftype.lower() == "dossier":
                    cmd = TEMPLATES["create_dir"].substitute(path=path, mode=mode)
                else:
                    cmd = TEMPLATES["create_file"].substitute(path=path, mode=mode)
                lines.append(f"run_cmd \"{cmd}\"")
                lines.append(f"run_cmd \"{TEMPLATES['update_file'].substitute(path=path)}\"")

        if actions.get("copy_operations"):
            for op, ftype, src, dest in actions["copy_operations"]:
                if op.lower().startswith("d\xe9placer"):
                    cmd = TEMPLATES["move"].substitute(src=src, dest=dest)
                else:
                    if ftype.lower() == "dossier":
                        cmd = TEMPLATES["copy_dir"].substitute(src=src, dest=dest)
                    else:
                        cmd = TEMPLATES["copy_file"].substitute(src=src, dest=dest)
                lines.append(f"run_cmd \"{cmd}\"")

        if actions.get("touch_files"):
            for entry in actions["touch_files"]:
                path, ts = entry if isinstance(entry, tuple) else (entry, None)
                if ts:
                    cmd = TEMPLATES["touch_ts"].substitute(path=path, ts=ts)
                else:
                    cmd = TEMPLATES["update_file"].substitute(path=path)
                lines.append(f"run_cmd \"{cmd}\"")

        if actions["cat_files"]:
            for file in actions["cat_files"]:
                lines.append(f"run_cmd \"{TEMPLATES['cat_file'].substitute(file=file)}\"")

        if actions["logs_check"]:
            for path in actions["log_paths"]:
                lines.append(f"run_cmd \"{TEMPLATES['grep_log'].substitute(path=path)}\"")

        if actions["validation"]:
            lines.append("# Validation des résultats")
            for expected in actions["validation"]:
                lines.extend(_compile_validation(expected))


    return "\n".join(lines)




def main():
    # Command-line interface for the generator
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for txt_file in glob(os.path.join(INPUT_DIR, "*.shtest")):
        with open(txt_file, encoding="utf-8") as f:
            test_description = f.read()
        actions = parse_test_file(test_description)
        script = generate_shell_script(actions)
        out_name = os.path.splitext(os.path.basename(txt_file))[0] + ".sh"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(script)
        # Inform the user about the newly created script
        print(f"Generated {out_path}")


if __name__ == '__main__':
    main()
