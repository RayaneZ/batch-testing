from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    dir_ = params.get('dir') or params.get('groups', [None])[0]
    last_file_var = params.get('last_file_var', None)
    dir_path = dir_ if dir_ else last_file_var
    handler = params.get('handler', 'dir_absent')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le dossier {dir_path} est absent")
    opposite = params.get('opposite', f"le dossier {dir_path} est présent")
    actual_cmd = f"if [ ! -d '{{dir_path}}' ]; then echo '{{expected}}'; else echo '{{opposite}}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'dir_path': dir_path, 'opposite': opposite}
    ) 