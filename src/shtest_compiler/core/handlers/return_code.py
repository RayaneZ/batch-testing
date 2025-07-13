from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    code = params["code"]
    handler = params.get('handler', 'return_code')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le code de retour est {code}")
    opposite = params.get('opposite', f"le code de retour n'est pas {code}")
    actual_cmd = f"if [ ${{?}} -eq {{code}} ]; then echo '{{expected}}'; else echo '{{opposite}}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'code': code, 'opposite': opposite}
    ) 