from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    varname = params.get('varname', 'result')
    handler = params.get('handler', 'true')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', 'always true')
    actual_cmd = f"{varname}=1"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'varname': varname}
    ) 