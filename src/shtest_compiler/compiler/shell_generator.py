import os
import re
from shtest_compiler.compiler.matchers.drivers import get_sql_command
from shtest_compiler.compiler.compiler import compile_validation
from shtest_compiler.parser.shunting_yard import SQLScriptExecution
from shtest_compiler.templates import TEMPLATES

def generate_shell_script(actions_list):
    lines = [
        "#!/bin/sh",
        "set -e",
        "",
        "run_cmd() {",
        "  local _stdout=$(mktemp)",
        "  local _stderr=$(mktemp)",
        "  /bin/sh -c \"$1\" >\"$_stdout\" 2>\"$_stderr\"",
        "  last_ret=$?",
        "  last_stdout=$(cat \"$_stdout\")",
        "  last_stderr=$(cat \"$_stderr\")",
        "  rm -f \"$_stdout\" \"_stderr\"",
        "  if [ $last_ret -ne 0 ]; then",
        "    echo \"STDERR: $last_stderr\"",
        "  fi",
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
        ""
    ]

    counter = [0]
    current_driver = os.environ.get("SQL_DRIVER", "oracle")
    pending_ident = False
    skip_ident = False

    for actions in actions_list:
        arguments = actions.get("arguments", {})
        current_driver = arguments.get("SQL_DRIVER", current_driver)

        if actions.get("steps"):
            lines.append(f"# ---- {actions['steps'][0]} ----")

        for key, value in arguments.items():
            lines.append(f"export {key}=\"{value}\"")

        if "SQL_CONN" in arguments and pending_ident:
            lines.extend(compile_validation("identifiants configurés", counter))
            pending_ident = False
            skip_ident = True

        for action in actions.get("initialization", []):
            scripts = re.findall(r"\S+\.sql", action, re.IGNORECASE)
            if scripts:
                for script in scripts:
                    cmd = get_sql_command(
                        script=script,
                        conn=arguments.get("SQL_CONN", "${SQL_CONN:-user/password@db}"),
                        driver=current_driver
                    )
                    lines.append(f"run_cmd \"{cmd}\"")
            else:
                lines.append(f"run_cmd \"echo '{action}'\"")

        actual_path = actions.get("batch_path")
        arg_str = ' '.join([f'{k}={v}' for k, v in arguments.items()])

        for action in actions.get("execution", []):
            if actual_path:
                cmd = f"{actual_path} {arg_str}" if arg_str else actual_path
                lines.append(f"run_cmd \"{cmd}\"")
            else:
                lines.append(f"echo '{action}'")

        for op, typ, path, mode in actions.get("file_operations", []):
            if op.startswith("cr") and typ == "dossier":
                cmd = TEMPLATES["create_dir"].substitute(path=path, mode=mode)
            elif op.startswith("cr") and typ == "fichier":
                cmd = TEMPLATES["create_file"].substitute(path=path, mode=mode)
            else:
                cmd = TEMPLATES["update_file"].substitute(path=path)
            lines.append(f"run_cmd \"{cmd}\"")

        for path, ts in actions.get("touch_files", []):
            if ts:
                cmd = TEMPLATES["touch_ts"].substitute(path=path, ts=ts)
            else:
                cmd = TEMPLATES["update_file"].substitute(path=path)
            lines.append(f"run_cmd \"{cmd}\"")

        for path in actions.get("purge_dirs", []):
            cmd = TEMPLATES["purge_dir"].substitute(path=path)
            lines.append(f"run_cmd \"{cmd}\"")

        for op, typ, src, dest in actions.get("copy_operations", []):
            if op.startswith("copier"):
                key = "copy_dir" if typ == "dossier" else "copy_file"
                cmd = TEMPLATES[key].substitute(src=src, dest=dest)
            else:
                cmd = TEMPLATES["move"].substitute(src=src, dest=dest)
            lines.append(f"run_cmd \"{cmd}\"")

        for f in actions.get("cat_files", []):
            cmd = TEMPLATES["cat_file"].substitute(file=f)
            lines.append(f"run_cmd \"{cmd}\"")

        validations = actions.get("validation", [])
        if skip_ident:
            validations = [v for v in validations if v != "identifiants configurés"]
            skip_ident = False

        if "identifiants configurés" in validations and "SQL_CONN" not in arguments:
            pending_ident = True
            validations = [v for v in validations if v != "identifiants configurés"]

        for v in validations:
            lines.extend(compile_validation(v, counter))

    if pending_ident:
        lines.extend(compile_validation("identifiants configurés", counter))

    return "\n\n".join(lines)

