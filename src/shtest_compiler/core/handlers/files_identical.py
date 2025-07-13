from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    file1 = params.get('file1') or params.get('groups', [None, None])[0]
    file2 = params.get('file2') or params.get('groups', [None, None])[1]
    handler = params.get('handler', 'files_identical')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', 'les fichiers {file1} et {file2} sont identiques')
    opposite = params.get('opposite', f"les fichiers {file1} et {file2} ne sont pas identiques")
    actual_cmd = (
        "if [ -f '{file1}' ] && [ -f '{file2}' ]; "
        "then cmp -s '{file1}' '{file2}' && echo '{expected}' || echo '{opposite}'; "
        "else echo '{opposite}'; fi"
    )
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'file1': file1, 'file2': file2, 'opposite': opposite}
    ) 