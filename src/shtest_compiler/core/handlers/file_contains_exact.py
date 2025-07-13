from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    file = params.get('file') or params.get('groups', [None, None])[0]
    text = params.get('text') or params.get('groups', [None, None])[1]
    last_file_var = params.get('last_file_var', None)
    file_path = file if file else last_file_var
    handler = params.get('handler', 'file_contains_exact')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le fichier {file_path} contient exactement {text}")
    opposite = params.get('opposite', f"le fichier {file_path} ne contient pas exactement {text}")
    actual_cmd = f"if [ \"$(cat '{{file_path}}')\" = \"{{text}}\" ]; then echo '{{expected}}'; else echo '{{opposite}}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'file_path': file_path, 'text': text, 'opposite': opposite}
    ) 