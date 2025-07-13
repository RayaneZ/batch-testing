from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    file = params.get('file') or params.get('groups', [None])[0]
    last_file_var = params.get('last_file_var', None)
    file_path = file if file else last_file_var
    handler = params.get('handler', 'content_displayed')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le contenu de {file_path} est affiché")
    opposite = params.get('opposite', f"le contenu de {file_path} n'est pas affiché")
    actual_cmd = f"if [ -s '{{file_path}}' ]; then echo '{{expected}}'; else echo '{{opposite}}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'file_path': file_path, 'opposite': opposite}
    ) 