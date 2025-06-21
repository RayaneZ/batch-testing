from parser import Parser
from string import Template
import argparse
import os
from glob import glob
import re


def parse_test_in_natural_language(test_description: str):
    """Analyse la description du test en utilisant le parseur modulaire."""
    parser = Parser()
    return parser.parse(test_description)


def parse_test_file(contents: str):
    """Parse line by line and preserve ordering of actions/results."""
    parser = Parser()
    parsed_lines = []
    for line in contents.splitlines():
        parsed_lines.append(parser.parse(line))
    return parsed_lines


TEMPLATES = {
    "process_batch": Template("${path} ${args}"),
    "grep_log": Template("grep 'ERROR' ${path}"),
    "execute_sql": Template("sqlplus -S user/password@db @${script}"),
    "create_dir": Template("mkdir -p ${path} && chmod ${mode} ${path}"),
    "create_file": Template("touch ${path} && chmod ${mode} ${path}"),
    "update_file": Template("touch ${path}"),
    "touch_ts": Template("touch -t ${ts} ${path}"),
    "cat_file": Template("cat ${file}"),
    "copy_file": Template("cp ${src} ${dest}"),
    "copy_dir": Template("cp -r ${src} ${dest}"),
}


def generate_shell_script(actions_list, batch_path: str):
    """Génère un script shell à partir de la liste ordonnée d'actions."""
    lines = [
        "#!/bin/bash",
        "",
        "run_cmd() {",
        "  local _stdout=$(mktemp)",
        "  local _stderr=$(mktemp)",
        "  bash -c \"$1\" >\"$_stdout\" 2>\"$_stderr\"",
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
                lines.append(f"run_cmd \"echo '{action}'\"  # TODO")

        if actions["execution"]:
            arg_str = ' '.join([f'{k}={v}' for k, v in actions["arguments"].items()])
            actual_path = actions.get("batch_path") or batch_path
            for action in actions["execution"]:
                lines.append(f"run_cmd \"{TEMPLATES['process_batch'].substitute(path=actual_path, args=arg_str)}\"")

        if actions["sql_scripts"]:
            for script in actions["sql_scripts"]:
                lines.append(f"run_cmd \"{TEMPLATES['execute_sql'].substitute(script=script)}\"")

        if actions["file_operations"]:
            for operation, ftype, path, mode in actions["file_operations"]:
                if ftype.lower() == "dossier":
                    cmd = TEMPLATES["create_dir"].substitute(path=path, mode=mode)
                else:
                    cmd = TEMPLATES["create_file"].substitute(path=path, mode=mode)
                lines.append(f"run_cmd \"{cmd}\"")
                lines.append(f"run_cmd \"{TEMPLATES['update_file'].substitute(path=path)}\"")

        if actions.get("copy_operations"):
            for ftype, src, dest in actions["copy_operations"]:
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
                lines.append(f"# Attendu : {expected}")
                m = re.search(r"le fichier (\S+) existe", expected, re.IGNORECASE)
                if m:
                    last_file = m.group(1)
                    lines.append(f"if [ -e {last_file} ]; then actual=\"le fichier {last_file} existe\"; else actual=\"le fichier {last_file} absent\"; fi")
                elif re.search(r"(?:le\s+)?fichier\s+est\s+présent", expected, re.IGNORECASE) and last_file:
                    lines.append(f"if [ -e {last_file} ]; then actual=\"Le fichier est présent\"; else actual=\"fichier absent\"; fi")
                elif re.search(r"le\s+(fichier|dossier)\s+est\s+copié", expected, re.IGNORECASE):
                    lines.append(f"if [ $last_ret -eq 0 ]; then actual=\"{expected}\"; else actual=\"échec copie\"; fi")
                else:
                    ret_match = re.search(r"retour\s*(\d+)", expected)
                    if ret_match:
                        lines.append("actual=\"$last_ret\"")
                        lines.append(f"expected=\"{ret_match.group(1)}\"")
                        lines.append("log_diff \"$expected\" \"$actual\"")
                        continue
                    stdout_match = re.search(r"stdout\s*=\s*(.*)", expected)
                    if stdout_match:
                        lines.append("actual=\"$last_stdout\"")
                        lines.append(f"expected=\"{stdout_match.group(1)}\"")
                        lines.append("log_diff \"$expected\" \"$actual\"")
                        continue
                    stdout_grep = re.search(r"stdout\s+contient\s+(.*)", expected)
                    if stdout_grep:
                        pattern = stdout_grep.group(1)
                        lines.append(f"if echo \"$last_stdout\" | grep -q {pattern!r}; then actual={pattern!r}; else actual=\"\"; fi")
                        lines.append(f"expected={pattern!r}")
                        lines.append("log_diff \"$expected\" \"$actual\"")
                        continue
                    stderr_match = re.search(r"stderr\s*=\s*(.*)", expected)
                    if stderr_match:
                        lines.append("actual=\"$last_stderr\"")
                        lines.append(f"expected=\"{stderr_match.group(1)}\"")
                        lines.append("log_diff \"$expected\" \"$actual\"")
                        continue
                    stderr_grep = re.search(r"stderr\s+contient\s+(.*)", expected)
                    if stderr_grep:
                        pattern = stderr_grep.group(1)
                        lines.append(f"if echo \"$last_stderr\" | grep -q {pattern!r}; then actual={pattern!r}; else actual=\"\"; fi")
                        lines.append(f"expected={pattern!r}")
                        lines.append("log_diff \"$expected\" \"$actual\"")
                        continue
                    lines.append("actual=\"non vérifié\"")
                lines.append(f"expected=\"{expected}\"")
                lines.append("log_diff \"$expected\" \"$actual\"")


    return "\n".join(lines)


INPUT_DIR = "src/tests"
OUTPUT_DIR = "output"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-path", default="./process_batch.sh", help="Chemin vers le script batch")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for txt_file in glob(os.path.join(INPUT_DIR, "*.shtest")):
        with open(txt_file, encoding="utf-8") as f:
            test_description = f.read()
        actions = parse_test_file(test_description)
        script = generate_shell_script(actions, batch_path=args.batch_path)
        out_name = os.path.splitext(os.path.basename(txt_file))[0] + ".sh"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(script)
        print(f"Generated {out_path}")


if __name__ == '__main__':
    main()
