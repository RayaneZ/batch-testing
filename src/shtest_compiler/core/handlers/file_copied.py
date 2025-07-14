from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    file1 = params.get('file1') or params.get('groups', [None, None])[0]
    file2 = params.get('file2') or params.get('groups', [None, None])[1]
    handler = params.get('handler', 'file_copied')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le fichier {file1} a été copié vers {file2}")
    opposite = params.get('opposite', f"le fichier {file1} n'a pas été copié vers {file2}")
    # Atomic check: both files exist and are identical
    actual_cmd = f"[ -f {file1} ] && [ -f {file2} ] && cmp -s {file1} {file2}"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'file1': file1, 'file2': file2, 'opposite': opposite}
    ) 