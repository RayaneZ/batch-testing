from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    file = params.get('file') or params.get('groups', [None])[0]
    last_file_var = params.get('last_file_var', None)
    file_path = file if file else last_file_var
    handler = params.get('handler', 'logs_accessible')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le fichier {file_path} est accessible")
    opposite = params.get('opposite', f"le fichier {file_path} n'est pas accessible")
    actual_cmd = f"if [ -f '{{file_path}}' ]; then echo '{{expected}}'; else echo '{{opposite}}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'file_path': file_path, 'opposite': opposite}
    ) 