
from .matchers import file_matchers, stdout_stderr, simple_checks
from compiler.context import CompileContext

def compile_atomic(expected: str, varname: str, last_file_var: list, context: CompileContext = None):
    lines = [f"# Attendu : {expected}"]

    context = context or CompileContext(counter=[0], last_file_var=last_file_var, verbose=False)

    for matcher in (file_matchers.match, stdout_stderr.match, simple_checks.match):
        matched = matcher(expected, last_file_var)
        if matched:
            if context.verbose:
                print(f"[MATCH] {matcher.__module__}.{matcher.__name__} matched for: '{expected}'")
            lines.extend(matched)
            break
    else:
        if context.verbose:
            print(f"[MATCH] Aucun matcher trouvé pour: '{expected}'")
        lines.extend([
            'actual="non vérifié"',
            f'expected="{expected}"'
        ])
    lines.append('log_diff "$expected" "$actual"')
    lines.append(f'if [ "$expected" = "$actual" ]; then {varname}=1; else {varname}=0; fi')
    return lines
