import re
from validation_ast import (
    ASTNode,
    Atomic,
    BinaryOp,
    parse_validation_expression,
)




def _compile_atomic(expected: str, varname: str, last_file_var: list):
    """Compile a single validation expression into shell code."""
    lines = [f"# Attendu : {expected}"]
    m = re.search(r"le fichier (\S+) existe", expected, re.IGNORECASE)
    if m:
        last_file_var[0] = m.group(1)
        lines.append(f"if [ -e {last_file_var[0]} ]; then actual=\"le fichier {last_file_var[0]} existe\"; else actual=\"le fichier {last_file_var[0]} absent\"; fi")
        lines.append(f"expected=\"le fichier {last_file_var[0]} existe\"")
    elif re.search(r"(?:le\s+)?fichier\s+est\s+présent", expected, re.IGNORECASE) and last_file_var[0]:
        lines.append(f"if [ -e {last_file_var[0]} ]; then actual=\"Le fichier est présent\"; else actual=\"fichier absent\"; fi")
        lines.append("expected=\"Le fichier est présent\"")
    elif re.search(r"le\s+(fichier|dossier)\s+est\s+copié", expected, re.IGNORECASE):
        lines.append(f"if [ $last_ret -eq 0 ]; then actual=\"{expected}\"; else actual=\"échec copie\"; fi")
        lines.append(f"expected=\"{expected}\"")
    elif m := re.search(r"le dossier (\S+) existe", expected, re.IGNORECASE):
        path = m.group(1)
        lines.append(f"if [ -d {path} ]; then actual=\"le dossier {path} existe\"; else actual=\"le dossier {path} absent\"; fi")
        lines.append(f"expected=\"le dossier {path} existe\"")
    elif m := re.search(r"le (?:fichier|dossier) (\S+) a(?: pour)?(?: les)? droits\s*(\d+)", expected, re.IGNORECASE):
        path, mode = m.groups()
        lines.append(f"actual=$(stat -c '%a' {path})")
        lines.append(f"expected=\"{mode}\"")
    elif m := re.search(r"la date du (?:fichier|dossier) (\S+) est\s*(\d{8,14})", expected, re.IGNORECASE):
        path, ts = m.groups()
        lines.append(f"actual=$(date -d @$(stat -c '%Y' {path}) +%Y%m%d%H%M%S)")
        lines.append(f"expected=\"{ts}\"")
    elif m := re.search(r"le fichier (\S+) contient exactement\s*(.+)", expected, re.IGNORECASE):
        path, value = m.groups()
        lines.append(f"actual=$(cat {path})")
        lines.append(f"expected=\"{value}\"")
    elif m := re.search(r"le fichier (\S+) contient\s*(.+)", expected, re.IGNORECASE):
        path, pattern = m.groups()
        lines.append(f"if grep -q {pattern!r} {path}; then actual={pattern!r}; else actual=\"\"; fi")
        lines.append(f"expected={pattern!r}")
    elif m := re.search(r"le dossier (\S+) contient\s*(\d+)\s*fichiers?(?:\s+(.*))?", expected, re.IGNORECASE):
        path, count, pat = m.groups()
        pat = pat or ''
        if pat:
            search = f"-name {pat!r}"
        else:
            search = "-type f"
        lines.append(f"actual=$(find {path} -maxdepth 1 {search} | wc -l)")
        lines.append(f"expected={count}")
    else:
        ret_match = re.search(r"retour\s*(\d+)", expected)
        if ret_match:
            lines.append("actual=\"$last_ret\"")
            lines.append(f"expected=\"{ret_match.group(1)}\"")
        else:
            stdout_match = re.search(r"stdout\s*=\s*(.*)", expected)
            if stdout_match:
                lines.append("actual=\"$last_stdout\"")
                lines.append(f"expected=\"{stdout_match.group(1)}\"")
            else:
                stdout_grep = re.search(r"stdout\s+contient\s+(.*)", expected)
                if stdout_grep:
                    pattern = stdout_grep.group(1)
                    lines.append(f"if echo \"$last_stdout\" | grep -q {pattern!r}; then actual={pattern!r}; else actual=\"\"; fi")
                    lines.append(f"expected={pattern!r}")
                else:
                    stderr_match = re.search(r"stderr\s*=\s*(.*)", expected)
                    if stderr_match:
                        lines.append("actual=\"$last_stderr\"")
                        lines.append(f"expected=\"{stderr_match.group(1)}\"")
                    else:
                        stderr_grep = re.search(r"stderr\s+contient\s+(.*)", expected)
                        if stderr_grep:
                            pattern = stderr_grep.group(1)
                            lines.append(f"if echo \"$last_stderr\" | grep -q {pattern!r}; then actual={pattern!r}; else actual=\"\"; fi")
                            lines.append(f"expected={pattern!r}")
                        else:
                            lines.append("actual=\"non vérifié\"")
                            lines.append(f"expected=\"{expected}\"")
    lines.append("log_diff \"$expected\" \"$actual\"")
    lines.append(f"if [ \"$expected\" = \"$actual\" ]; then {varname}=1; else {varname}=0; fi")
    return lines


def _compile_validation(expression: str):
    """Compile a complex validation expression into shell instructions."""

    def _compile_ast(node: ASTNode, counter: list, last_file_var: list):
        if isinstance(node, BinaryOp):
            left_lines, left_var = _compile_ast(node.left, counter, last_file_var)
            right_lines, right_var = _compile_ast(node.right, counter, last_file_var)
            counter[0] += 1
            var = f"cond{counter[0]}"
            op = "&&" if node.op == "et" else "||"
            lines = left_lines + right_lines
            lines.append(
                f"if [ ${{{left_var}}} -eq 1 ] {op} [ ${{{right_var}}} -eq 1 ]; then {var}=1; else {var}=0; fi"
            )
            return lines, var
        elif isinstance(node, Atomic):
            counter[0] += 1
            var = f"cond{counter[0]}"
            lines = _compile_atomic(node.value, var, last_file_var)
            return lines, var
        else:
            raise TypeError("Unknown AST node")

    ast = parse_validation_expression(expression)
    counter = [0]
    last_file_var = [None]
    lines, final_var = _compile_ast(ast, counter, last_file_var)
    lines.append(f"if [ ${{{final_var}}} -eq 1 ]; then actual=\"OK\"; else actual=\"KO\"; fi")
    lines.append("expected=\"OK\"")
    lines.append("log_diff \"$expected\" \"$actual\"")
    return lines

