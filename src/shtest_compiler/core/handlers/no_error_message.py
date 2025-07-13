from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    handler = params.get('handler', 'no_error_message')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', "aucun message d'erreur")
    opposite = params.get('opposite', "un message d'erreur est présent")
    actual_cmd = f"if [ ! -s 'stderr.log' ]; then echo '{{expected}}'; else echo '{{opposite}}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'opposite': opposite}
    ) 