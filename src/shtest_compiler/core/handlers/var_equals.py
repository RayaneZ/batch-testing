from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    var = params.get('var')
    value = params.get('value')
    expected = f"variable {var} vaut {value}"
    opposite = f"variable {var} ne vaut pas {value}"
    actual_cmd = f"if [ \"${var}\" = \"{value}\" ]; then echo '{expected}'; else echo '{opposite}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler="var_equals",
        scope="global"
    ) 