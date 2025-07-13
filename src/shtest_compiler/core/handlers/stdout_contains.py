from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    text = params.get('text')
    expected = f"stdout contient {text}"
    opposite = f"stdout ne contient pas {text}"
    actual_cmd = f"if echo \"$stdout\" | grep -q \"{text}\"; then echo '{expected}'; else echo '{opposite}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler="stdout_contains",
        scope="global"
    ) 