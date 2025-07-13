from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    var = params.get('var') or params.get('groups', [None])[0] or "SQL_CONN"
    handler = params.get('handler', 'credentials_configured')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"la variable {var} est configurée")
    opposite = params.get('opposite', f"la variable {var} n'est pas configurée")
    actual_cmd = f"if [ -n '${{{{var}}}}' ]; then echo '{{expected}}'; else echo '{{opposite}}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'var': var, 'opposite': opposite}
    ) 