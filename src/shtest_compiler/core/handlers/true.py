from shtest_compiler.ast.shell_framework_ast import ValidationCheck


def handle(params):
    handler = params.get("handler", "true")
    scope = params.get("scope", "global")
    expected = params.get("canonical_phrase", "always true")

    # Return atomic command that always succeeds
    actual_cmd = "true"

    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={},
    )
