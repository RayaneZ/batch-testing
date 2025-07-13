from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    phrase = params['canonical_phrase']
    scope = params['scope']
    handler = params.get('handler', 'file_contains')
    pattern_entry = params.get('pattern_entry', {})
    file = params['file']
    text = params['text']
    expected = phrase  # template, not substituted
    opposite_phrase = pattern_entry.get('opposite', {}).get('phrase')
    opposite = opposite_phrase if opposite_phrase else f"NOT({expected})"
    actual_cmd = "if grep -q \"{text}\" \"{file}\"; then echo '{expected}'; else echo '{opposite}'; fi"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'file': file, 'text': text, 'opposite': opposite}
    ) 