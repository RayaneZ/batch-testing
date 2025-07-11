from .matcher_registry import run_matcher
from shtest_compiler.compiler.context import CompileContext

def compile_atomic(expected: str, varname: str, last_file_var: list, context: CompileContext = None):
    lines = [f"# Attendu : {expected}"]

    context = context or CompileContext(counter=[0], last_file_var=last_file_var, verbose=False)
    matched = run_matcher(expected, last_file_var)

    if matched:
        if context.verbose:
            print(f"[MATCH] Matcher trouvé pour : '{expected}'")
        lines.extend(matched)
    else:
        msg = f"[ERREUR] Aucun matcher trouvé pour: '{expected}'"
        print(msg)
        lines.extend([
            f'echo "{msg}" 1>&2',
            'actual="non vérifié"',
            f'expected="{expected}"'
        ])

    lines.append('log_diff "$expected" "$actual"')
    lines.append(f'if [ "$expected" = "$actual" ]; then {varname}=1; else {varname}=0; fi')

    return lines
