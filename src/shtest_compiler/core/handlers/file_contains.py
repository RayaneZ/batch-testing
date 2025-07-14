from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    phrase = params['canonical_phrase']
    handler = params.get('handler', 'file_contains')
    pattern_entry = params.get('pattern_entry', {})
    file = params.get('file')
    text = params.get('text')
    # Scope logic: if file is missing, this is local (last_action)
    if not file:
        scope = 'last_action'
    else:
        scope = params.get('scope', 'global')
    expected = phrase  # template, not substituted
    opposite_phrase = pattern_entry.get('opposite', {}).get('phrase')
    opposite = opposite_phrase if opposite_phrase else f"NOT({expected})"
    # Return atomic command only - no if/then/else logic
    actual_cmd = f"grep -q '{text}' '{file}'"
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'file': file, 'text': text, 'opposite': opposite}
    ) 