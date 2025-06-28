from .matchers import file_matchers, stdout_stderr, simple_checks

def compile_atomic(expected: str, varname: str, last_file_var: list):
    lines = [f"# Attendu : {expected}"]
    for matcher in (file_matchers.match, stdout_stderr.match, simple_checks.match):
        matched = matcher(expected, last_file_var)
        if matched:
            lines.extend(matched)
            break
    else:
        lines.extend([
            "actual=\"non vérifié\"",
            f"expected=\"{expected}\""
        ])
    lines.append("log_diff \"$expected\" \"$actual\"")
    lines.append(f"if [ \"$expected\" = \"$actual\" ]; then {varname}=1; else {varname}=0; fi")
    return lines