from parser import Parser
from string import Template


def parse_test_in_natural_language(test_description: str):
    """Analyse la description du test en utilisant le parseur modulaire."""
    parser = Parser()
    return parser.parse(test_description)


TEMPLATES = {
    "process_batch": Template("./process_batch.sh ${args}"),
    "grep_log": Template("grep 'ERROR' ${path}"),
    "execute_sql": Template("sqlplus -S user/password@db @${script}"),
    "create_dir": Template("mkdir -p ${path} && chmod ${mode} ${path}"),
    "create_file": Template("touch ${path} && chmod ${mode} ${path}"),
    "update_file": Template("touch ${path}"),
    "cat_file": Template("cat ${file}"),
}


def generate_shell_script(actions):
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

    if actions["initialization"]:
        lines.append("# Initialisation")
        for action in actions["initialization"]:
            lines.append(f"echo '{action}'  # TODO: implémenter la commande")
        lines.append("")

    if actions["execution"]:
        lines.append("# Exécution du batch")
        arg_str = ' '.join([f'{k}={v}' for k, v in actions["arguments"].items()])
        for action in actions["execution"]:
            lines.append(f"echo '{action}'")
            lines.append(TEMPLATES["process_batch"].substitute(args=arg_str))
        lines.append("")

    if actions["sql_scripts"]:
        lines.append("# Exécution des scripts SQL")
        for script in actions["sql_scripts"]:
            lines.append(TEMPLATES["execute_sql"].substitute(script=script))
        lines.append("")

    if actions["file_operations"]:
        lines.append("# Opérations sur les fichiers et dossiers")
        for operation, path, mode in actions["file_operations"]:
            if "dossier" in operation.lower():
                lines.append(TEMPLATES["create_dir"].substitute(path=path, mode=mode))
            if "fichier" in operation.lower():
                lines.append(TEMPLATES["create_file"].substitute(path=path, mode=mode))
            lines.append(TEMPLATES["update_file"].substitute(path=path))
        lines.append("")

    if actions["cat_files"]:
        lines.append("# Affichage du contenu des fichiers")
        for file in actions["cat_files"]:
            lines.append(TEMPLATES["cat_file"].substitute(file=file))
        lines.append("")

    if actions["logs_check"]:
        lines.append("# Vérification des logs")
        for path in actions["log_paths"]:
            lines.append(TEMPLATES["grep_log"].substitute(path=path))
        lines.append("")

    if actions["validation"]:
        lines.append("# Validation des résultats")
        for expected in actions["validation"]:
            lines.append(f"# Attendu : {expected}")
            lines.append("actual=\"<commande à implémenter>\"")
            lines.append(f"expected=\"{expected}\"")
            lines.append("log_diff \"$expected\" \"$actual\"")
            lines.append("")

    return "\n".join(lines)


def main():
    with open('tests/test_case_1.txt', encoding='utf-8') as f:
        test_description = f.read()
    actions = parse_test_in_natural_language(test_description)
    script = generate_shell_script(actions)
    print(script)


if __name__ == '__main__':
    main()
