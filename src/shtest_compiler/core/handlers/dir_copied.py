from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    dir1 = params.get('dir1') or params.get('groups', [None, None])[0]
    dir2 = params.get('dir2') or params.get('groups', [None, None])[1]
    handler = params.get('handler', 'dir_copied')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le dossier {dir1} a été copié vers {dir2}")
    opposite = params.get('opposite', f"le dossier {dir1} n'a pas été copié vers {dir2}")
    actual_cmd = (
        "if [ -d '{dir1}' ] && [ -d '{dir2}' ]; "
        "then diff -r '{dir1}' '{dir2}' >/dev/null 2>&1 && echo '{expected}' || echo '{opposite}'; "
        "else echo '{opposite}'; fi"
    )
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'dir1': dir1, 'dir2': dir2, 'opposite': opposite}
    ) 