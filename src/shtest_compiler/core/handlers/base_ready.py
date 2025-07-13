from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    handler = params.get('handler', 'base_ready')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', "la base est prête")
    opposite = params.get('opposite', "la base n'est pas prête")
    actual_cmd = f"if [ -f 'db_ready.flag' ]; then echo '{{expected}}'; else echo '{{opposite}}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'opposite': opposite}
    ) 