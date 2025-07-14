from shtest_compiler.ast.shell_framework_ast import ValidationCheck


def handle(params):
    dir1 = params.get("dir1") or params.get("groups", [None, None])[0]
    dir2 = params.get("dir2") or params.get("groups", [None, None])[1]

    # Determine scope based on argument presence
    if not dir1 or not dir2:
        scope = "last_action"
    else:
        scope = params.get("scope", "global")

    handler = params.get("handler", "dir_copied")
    expected = params.get(
        "canonical_phrase", f"le dossier {dir1} a été copié vers {dir2}"
    )
    opposite = params.get(
        "opposite", f"le dossier {dir1} n'a pas été copié vers {dir2}"
    )

    # Return atomic command only - no if/then/else logic
    actual_cmd = f"test -d '{dir1}' && test -d '{dir2}' && diff -r '{dir1}' '{dir2}' >/dev/null 2>&1"

    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={"dir1": dir1, "dir2": dir2, "opposite": opposite},
    )
