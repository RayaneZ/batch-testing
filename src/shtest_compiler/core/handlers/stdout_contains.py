from shtest_compiler.ast.shell_framework_ast import ValidationCheck


def handle(params):
    text = params.get("text")

    # Determine scope based on argument presence
    if not text:
        scope = "last_action"
    else:
        scope = params.get("scope", "global")

    expected = f"stdout contient {text}"
    opposite = f"stdout ne contient pas {text}"

    # Return atomic command only - no if/then/else logic
    actual_cmd = f'echo "$stdout" | grep -q "{text}"'

    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler="stdout_contains",
        scope=scope,
        params={"text": text, "opposite": opposite},
    )
