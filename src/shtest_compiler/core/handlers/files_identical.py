from shtest_compiler.ast.shell_framework_ast import ValidationCheck


def handle(params):
    file1 = params.get("file1") or params.get("groups", [None, None])[0]
    file2 = params.get("file2") or params.get("groups", [None, None])[1]

    # Determine scope based on argument presence
    if not file1 or not file2:
        scope = "last_action"
    else:
        scope = params.get("scope", "global")

    handler = params.get("handler", "files_identical")
    expected = params.get(
        "canonical_phrase", f"les fichiers {file1} et {file2} sont identiques"
    )
    opposite = params.get(
        "opposite", f"les fichiers {file1} et {file2} ne sont pas identiques"
    )

    # Return atomic command only - no if/then/else logic
    actual_cmd = f"test -f '{file1}' && test -f '{file2}' && cmp -s '{file1}' '{file2}'"

    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={"file1": file1, "file2": file2, "opposite": opposite},
    )
