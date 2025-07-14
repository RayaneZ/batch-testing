from shtest_compiler.ast.shell_framework_ast import ValidationCheck


def handle(params):
    handler = params.get("handler", "base_ready")
    scope = params.get("scope", "global")
    expected = params.get("canonical_phrase", "la base est prête")
    opposite = params.get("opposite", "la base n'est pas prête")

    # Return atomic command only - no if/then/else logic
    actual_cmd = "test -f 'db_ready.flag'"

    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={"opposite": opposite},
    )
