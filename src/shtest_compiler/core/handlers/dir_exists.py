from shtest_compiler.ast.shell_framework_ast import ValidationCheck
from shtest_compiler.utils.canonicalization import shell_escape

def handle(params):
    dir_ = params.get('dir') or params.get('groups', [None])[0]
    last_file_var = params.get('last_file_var', None)
    dir_path = dir_ if dir_ else last_file_var
    handler = params.get('handler', 'dir_exists')
    # Scope logic: if dir_path is missing, this is local (last_action)
    if not dir_path:
        scope = 'last_action'
    else:
        scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le dossier {dir_path} existe")
    opposite = params.get('opposite', f"le dossier {dir_path} n'existe pas")
    # Return atomic command only - no if/then/else logic
    actual_cmd = f"test -d {shell_escape(dir_path)}"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'dir_path': dir_path, 'opposite': opposite}
    ) 