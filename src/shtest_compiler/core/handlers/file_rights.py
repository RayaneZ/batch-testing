from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    file = params.get('file') or params.get('groups', [None, None])[0]
    mode = params.get('mode') or params.get('groups', [None, None])[1]
    last_file_var = params.get('last_file_var', None)
    file_path = file if file else last_file_var
    handler = params.get('handler', 'file_rights')
    # Scope logic: if file_path is missing, this is local (last_action)
    if not file_path:
        scope = 'last_action'
    else:
        scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le fichier {file_path} a les droits {mode}")
    opposite = params.get('opposite', f"le fichier {file_path} n'a pas les droits {mode}")
    # Atomic check: file has the expected mode
    actual_cmd = f"[ $(stat -c '%a' {file_path}) = '{mode}' ]"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'file_path': file_path, 'mode': mode, 'opposite': opposite}
    ) 