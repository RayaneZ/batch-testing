from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    dir_ = params.get('dir') or params.get('groups', [None, None])[0]
    mode = params.get('mode') or params.get('groups', [None, None])[1]
    last_file_var = params.get('last_file_var', None)
    dir_path = dir_ if dir_ else last_file_var
    handler = params.get('handler', 'dir_rights')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le dossier {dir_path} a les droits {mode}")
    opposite = params.get('opposite', f"le dossier {dir_path} n'a pas les droits {mode}")
    actual_cmd = f"if [ $(stat -c '%a' '{{dir_path}}') = '{{mode}}' ]; then echo '{{expected}}'; else echo '{{opposite}}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'dir_path': dir_path, 'mode': mode, 'opposite': opposite}
    ) 