from shtest_compiler.ast.shell_framework_ast import ValidationCheck
from shtest_compiler.utils.canonicalization import shell_escape

def handle(params):
    file_path = params.get('file') or params.get('groups', [None])[0]
    handler = params.get('handler', 'file_present')
    scope = params.get('scope', 'global')
    expected = params.get('canonical_phrase', f"le fichier {file_path} est présent")
    opposite = params.get('opposite', f"le fichier {file_path} est absent")
    actual_cmd = f"if [ -f {shell_escape(file_path)} ]; then echo {shell_escape(expected)}; else echo {shell_escape(opposite)}; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'file_path': file_path, 'opposite': opposite}
    ) 