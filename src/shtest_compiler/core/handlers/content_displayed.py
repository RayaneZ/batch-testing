from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    file = params.get('file') or params.get('groups', [None])[0]
    last_file_var = params.get('last_file_var', None)
    file_path = file if file else last_file_var
    
    # Determine scope based on argument presence
    if not file:
        scope = 'last_action'
    else:
        scope = params.get('scope', 'global')
    
    handler = params.get('handler', 'content_displayed')
    expected = params.get('canonical_phrase', f"le contenu de {file_path} est affiché")
    opposite = params.get('opposite', f"le contenu de {file_path} n'est pas affiché")
    
    # Return atomic command only - no if/then/else logic
    actual_cmd = f"test -s '{file_path}'"
    
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'file_path': file_path, 'opposite': opposite}
    ) 