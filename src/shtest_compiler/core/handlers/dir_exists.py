from shtest_compiler.ast.shell_framework_ast import ValidationCheck
from shtest_compiler.utils.canonicalization import shell_escape

def handle(params):
    dir_ = params.get('dir') or params.get('groups', [None])[0]
    last_file_var = params.get('last_file_var', None)
    dir_path = dir_ if dir_ else last_file_var
    handler = params.get('handler', 'dir_exists')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le dossier {dir_path} existe")
    opposite = params.get('opposite', f"le dossier {dir_path} n'existe pas")
    actual_cmd = f"if [ -d {shell_escape(dir_path)} ]; then echo {shell_escape(expected)}; else echo {shell_escape(opposite)}; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'dir_path': dir_path, 'opposite': opposite}
    ) 