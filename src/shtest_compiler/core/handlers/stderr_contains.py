from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    text = params.get('text')
    expected = f"stderr contient {text}"
    opposite = f"stderr ne contient pas {text}"
    actual_cmd = f"if echo \"$stderr\" | grep -q \"{text}\"; then echo '{expected}'; else echo '{opposite}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler="stderr_contains",
        scope="global"
    ) 