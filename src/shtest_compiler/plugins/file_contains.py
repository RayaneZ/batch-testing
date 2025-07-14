"""
Plugin for file contains validation.
"""

from shtest_compiler.ast.shell_framework_ast import ValidationCheck


def file_contains_validation(file, text, **kwargs):
    return ValidationCheck(
        expected="Le fichier {file} contient {text}",
        actual_cmd="if grep -q \"{text}\" \"{file}\"; then actual='Le fichier {file} contient {text}'; else actual='Le fichier {file} ne contient pas {text}'; fi",
        handler="file_contains",
        scope="global",
    )


PLUGIN_HANDLERS = {
    "file_contains": file_contains_validation,
}
