from shtest_compiler.ast.shell_framework_ast import ValidationCheck


def handle(params):
    file = params.get("file") or params.get("groups", [None])[0]
    last_file_var = params.get("last_file_var", None)
    file_path = file if file else last_file_var
    handler = params.get("handler", "file_absent")
    # Scope logic: if file_path is missing, this is local (last_action)
    if not file_path:
        scope = "last_action"
    else:
        scope = params.get("scope", "global")
    expected = params.get("canonical_phrase", f"le fichier {file_path} est absent")
    opposite = params.get("opposite", f"le fichier {file_path} est présent")
    # Atomic check: file does not exist
    actual_cmd = f"[ ! -f {file_path} ]"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={"file_path": file_path, "opposite": opposite},
    )
