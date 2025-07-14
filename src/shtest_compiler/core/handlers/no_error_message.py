from shtest_compiler.ast.shell_framework_ast import ValidationCheck


def handle(params):
    handler = params.get("handler", "no_error_message")
    scope = params.get("scope", "global")
    expected = params.get("canonical_phrase", "aucun message d'erreur")
    opposite = params.get("opposite", "un message d'erreur est présent")

    # Return atomic command only - no if/then/else logic
    actual_cmd = "test ! -s 'stderr.log'"

    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={"opposite": opposite},
    )
