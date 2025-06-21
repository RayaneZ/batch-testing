from parser import Parser
from string import Template
import argparse
import os
from glob import glob


def parse_test_in_natural_language(test_description: str):
    """Analyse la description du test en utilisant le parseur modulaire."""
    parser = Parser()
    return parser.parse(test_description)


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


def generate_shell_script(actions, batch_path: str):
    """Génère un script shell à partir des actions extraites."""
    lines = [
        "#!/bin/bash",
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

    steps = actions.get("steps", [])
    step_idx = 0

    def maybe_step():
        nonlocal step_idx
        if step_idx < len(steps):
            lines.append(f"# ---- {steps[step_idx]} ----")
            step_idx += 1

    if actions["initialization"]:
        maybe_step()
        lines.append("# Initialisation")
        for action in actions["initialization"]:
            lines.append(f"echo '{action}'  # TODO: implémenter la commande")
        lines.append("")

    if actions["execution"]:
        maybe_step()
        lines.append("# Exécution du batch")
        arg_str = ' '.join([f'{k}={v}' for k, v in actions["arguments"].items()])
        actual_path = actions.get("batch_path") or batch_path
        for action in actions["execution"]:
            lines.append(f"echo '{action}'")
            lines.append(TEMPLATES["process_batch"].substitute(path=actual_path, args=arg_str))
        lines.append("")

    if actions["sql_scripts"]:
        maybe_step()
        lines.append("# Exécution des scripts SQL")
        for script in actions["sql_scripts"]:
            lines.append(TEMPLATES["execute_sql"].substitute(script=script))
        lines.append("")

    if actions["file_operations"]:
        maybe_step()
        lines.append("# Opérations sur les fichiers et dossiers")
        for operation, ftype, path, mode in actions["file_operations"]:
            if ftype.lower() == "dossier":
                lines.append(TEMPLATES["create_dir"].substitute(path=path, mode=mode))
            if ftype.lower() == "fichier":
                lines.append(TEMPLATES["create_file"].substitute(path=path, mode=mode))
            lines.append(TEMPLATES["update_file"].substitute(path=path))
        lines.append("")

    if actions.get("copy_operations"):
        maybe_step()
        lines.append("# Copies de fichiers et dossiers")
        for ftype, src, dest in actions["copy_operations"]:
            if ftype.lower() == "dossier":
                lines.append(TEMPLATES["copy_dir"].substitute(src=src, dest=dest))
            else:
                lines.append(TEMPLATES["copy_file"].substitute(src=src, dest=dest))
        lines.append("")

    if actions.get("touch_files"):
        maybe_step()
        lines.append("# Mise à jour de fichiers")
        for entry in actions["touch_files"]:
            if isinstance(entry, tuple):
                path, ts = entry
            else:
                path, ts = entry, None
            if ts:
                lines.append(TEMPLATES["touch_ts"].substitute(path=path, ts=ts))
            else:
                lines.append(TEMPLATES["update_file"].substitute(path=path))
        lines.append("")

    if actions["cat_files"]:
        maybe_step()
        lines.append("# Affichage du contenu des fichiers")
        for file in actions["cat_files"]:
            lines.append(TEMPLATES["cat_file"].substitute(file=file))
        lines.append("")

    if actions["logs_check"]:
        maybe_step()
        lines.append("# Vérification des logs")
        for path in actions["log_paths"]:
            lines.append(TEMPLATES["grep_log"].substitute(path=path))
        lines.append("")

    if actions["validation"]:
        maybe_step()
        lines.append("# Validation des résultats")
        for expected in actions["validation"]:
            lines.append(f"# Attendu : {expected}")
            lines.append("actual=\"<commande à implémenter>\"")
            lines.append(f"expected=\"{expected}\"")
            lines.append("log_diff \"$expected\" \"$actual\"")
            lines.append("")

    return "\n".join(lines)


INPUT_DIR = "tests"
OUTPUT_DIR = "output"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-path", default="./process_batch.sh", help="Chemin vers le script batch")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for txt_file in glob(os.path.join(INPUT_DIR, "*.shtest")):
        with open(txt_file, encoding="utf-8") as f:
            test_description = f.read()
        actions = parse_test_in_natural_language(test_description)
        script = generate_shell_script(actions, batch_path=args.batch_path)
        out_name = os.path.splitext(os.path.basename(txt_file))[0] + ".sh"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(script)
        print(f"Generated {out_path}")


if __name__ == '__main__':
    main()
