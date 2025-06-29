from parser.parser import Parser
from lexer import lex
from templates import TEMPLATES
from compiler.matchers.drivers import get_sql_command
from compiler.compiler import compile_validation
import os
from glob import glob
import re

def parse_test_file(contents: str):
    parser = Parser()
    parsed_lines = []
    for token in lex(contents):
        if token.kind == "STEP":
            line = f"Étape: {token.value}"
        elif token.kind == "ACTION_RESULT":
            line = f"Action: {token.value} ; Résultat: {token.result}"
        elif token.kind == "ACTION_ONLY":
            line = f"Action: {token.value}"
        else:
            line = token.value
        parsed_lines.append(parser.parse(line))
    return parsed_lines

def generate_shell_script(actions_list):
    lines = [
        "#!/bin/sh",
        "set -e",
        "",
        "run_cmd() {",
        "  local _stdout=$(mktemp)",
        "  local _stderr=$(mktemp)",
        "  /bin/sh -c \"$1\" >\"$_stdout\" 2>\"_stderr\"",
        "  last_ret=$?",
        "  last_stdout=$(cat \"$_stdout\")",
        "  last_stderr=$(cat \"$_stderr\")",
        "  rm -f \"$_stdout\" \"$_stderr\"",
        "  if [ $last_ret -ne 0 ]; then",
        "    echo \"STDERR: $last_stderr\"",
        "  fi",
        "}", "", "log_diff() {",
        "  expected=\"$1\"",
        "  actual=\"$2\"",
        "  if [ \"$expected\" != \"$actual\" ]; then",
        "    echo 'Différence détectée :'",
        "    echo \"- Attendu : $expected\"",
        "    echo \"- Obtenu : $actual\"",
        "  fi", "}", ""
    ]

    counter = [0]
    current_driver = os.environ.get("SQL_DRIVER", "oracle")
    pending_ident = False
    skip_ident = False
    for actions in actions_list:
        if actions.get("steps"):
            lines.append(f"# ---- {actions['steps'][0]} ----")
            continue
        if actions.get("arguments"):
            for key, value in actions["arguments"].items():
                lines.append(f"export {key}=\"{value}\"")
                if key == "SQL_DRIVER":
                    current_driver = value
            if "SQL_CONN" in actions["arguments"] and pending_ident:
                lines.extend(compile_validation("identifiants configurés", counter))
                pending_ident = False
                skip_ident = True
        if actions.get("initialization"):
            lines.append("# Initialisation")
            for action in actions["initialization"]:
                scripts = re.findall(r"\S+\.sql", action, re.IGNORECASE)
                if scripts:
                    for script in scripts:
                        cmd = get_sql_command(script=script, conn='${SQL_CONN:-user/password@db}', driver=current_driver)
                        lines.append(f"run_cmd \"{cmd}\"")
                else:
                    lines.append(f"run_cmd \"echo '{action}'\"")
        if actions.get("execution"):
            arg_str = ' '.join([f'{k}={v}' for k, v in actions.get("arguments", {}).items()])
            actual_path = actions.get("batch_path")
            for action in actions["execution"]:
                scripts = re.findall(r"\S+\.sql", action, re.IGNORECASE)
                if scripts:
                    for script in scripts:
                        cmd = get_sql_command(script=script, conn='${SQL_CONN:-user/password@db}', driver=current_driver)
                        lines.append(f"run_cmd \"{cmd}\"")
                    continue
                if actual_path is None:
                    lines.append(f"echo '{action}'")
                    continue
                cmd = actual_path if not arg_str else f"{actual_path} {arg_str}"
                lines.append(f"run_cmd \"{cmd}\"")
        if actions.get("file_operations"):
            for op, typ, path, mode in actions["file_operations"]:
                if op.startswith("cr") and typ == "dossier":
                    cmd = TEMPLATES["create_dir"].substitute(path=path, mode=mode)
                elif op.startswith("cr") and typ == "fichier":
                    cmd = TEMPLATES["create_file"].substitute(path=path, mode=mode)
                else:
                    cmd = TEMPLATES["update_file"].substitute(path=path)
                lines.append(f"run_cmd \"{cmd}\"")
        if actions.get("touch_files"):
            for path, ts in actions["touch_files"]:
                if ts:
                    cmd = TEMPLATES["touch_ts"].substitute(path=path, ts=ts)
                else:
                    cmd = TEMPLATES["update_file"].substitute(path=path)
                lines.append(f"run_cmd \"{cmd}\"")
        if actions.get("purge_dirs"):
            for path in actions["purge_dirs"]:
                cmd = TEMPLATES["purge_dir"].substitute(path=path)
                lines.append(f"run_cmd \"{cmd}\"")
        if actions.get("copy_operations"):
            for op, typ, src, dest in actions["copy_operations"]:
                if op.startswith("copier"):
                    key = "copy_dir" if typ == "dossier" else "copy_file"
                    cmd = TEMPLATES[key].substitute(src=src, dest=dest)
                else:
                    cmd = TEMPLATES["move"].substitute(src=src, dest=dest)
                lines.append(f"run_cmd \"{cmd}\"")
        if actions.get("cat_files"):
            for f in actions["cat_files"]:
                cmd = TEMPLATES["cat_file"].substitute(file=f)
                lines.append(f"run_cmd \"{cmd}\"")
        if actions.get("validation"):
            vals = actions["validation"]
            if skip_ident:
                vals = [v for v in vals if v != "identifiants configurés"]
                skip_ident = False
            if "identifiants configurés" in vals and "SQL_CONN" not in actions.get("arguments", {}):
                pending_ident = True
                vals = [v for v in vals if v != "identifiants configurés"]
            for v in vals:
                lines.extend(compile_validation(v, counter))

    if pending_ident:
        lines.extend(compile_validation("identifiants configurés", counter))

    return "\n".join(lines)

def generate_tests(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    for txt_file in glob(os.path.join(input_dir, "*.shtest")):
        with open(txt_file, encoding="utf-8") as f:
            test_description = f.read()
        actions = parse_test_file(test_description)
        script = generate_shell_script(actions)
        out_name = os.path.splitext(os.path.basename(txt_file))[0] + ".sh"
        out_path = os.path.join(output_dir, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(script)
        print(f"✅ Generated {out_path}")
