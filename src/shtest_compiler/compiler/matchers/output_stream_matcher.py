from shtest_compiler.compiler.matcher_registry import register_matcher
import re


@register_matcher("stdout_stderr")
def match(expected, _):
    patterns = [
        (r"stdout\s*=\s*(.*)", "$last_stdout"),
        (r"stdout\s+contient\s+(.*)", "$last_stdout"),
        (r"stderr\s*=\s*(.*)", "$last_stderr"),
        (r"stderr\s+contient\s+(.*)", "$last_stderr"),
    ]
    for pattern, var in patterns:
        m = re.search(pattern, expected)
        if m:
            val = m.group(1).strip().strip("\"''")
            if "contient" in pattern:
                return [
                    f'if echo "{var}" | grep -q {val!r}; then actual={val!r}; else actual=""; fi',
                    f"expected={val!r}",
                ]
            return [f'actual="{var}"', f'expected="{val}"']
    return None
