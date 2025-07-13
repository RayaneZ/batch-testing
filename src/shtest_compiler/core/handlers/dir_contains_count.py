from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    dir_ = params.get('dir') or params.get('groups', [None, None, None])[0]
    count = params.get('count') or params.get('groups', [None, None, None])[1]
    pattern = params.get('pattern') or params.get('groups', [None, None, None])[2]
    last_file_var = params.get('last_file_var', None)
    dir_path = dir_ if dir_ else last_file_var
    handler = params.get('handler', 'dir_contains_count')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le dossier {dir_path} contient {count} fichiers correspondant au motif {pattern}")
    opposite = params.get('opposite', f"le dossier {dir_path} ne contient pas {count} fichiers correspondant au motif {pattern}")
    actual_cmd = (
        "actual=$(find '{dir_path}' -type f -name '{pattern}' | wc -l); "
        "if [ \"$actual\" -eq {count} ]; then echo '{expected}'; else echo '{opposite}'; fi"
    )
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'dir_path': dir_path, 'count': count, 'pattern': pattern, 'opposite': opposite}
    ) 