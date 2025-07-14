from shtest_compiler.ast.shell_framework_ast import ValidationCheck


def handle(params):
    dir_ = params.get("dir") or params.get("groups", [None, None])[0]
    mode = params.get("mode") or params.get("groups", [None, None])[1]
    last_file_var = params.get("last_file_var", None)
    dir_path = dir_ if dir_ else last_file_var

    # Determine scope based on argument presence
    if not dir_ or not mode:
        scope = "last_action"
    else:
        scope = params.get("scope", "global")

    handler = params.get("handler", "dir_rights")
    expected = params.get(
        "canonical_phrase", f"le dossier {dir_path} a les droits {mode}"
    )
    opposite = params.get(
        "opposite", f"le dossier {dir_path} n'a pas les droits {mode}"
    )

    # Return atomic command only - no if/then/else logic
    actual_cmd = f"test \"$(stat -c '%a' '{dir_path}')\" = '{mode}'"

    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={"dir_path": dir_path, "mode": mode, "opposite": opposite},
    )
