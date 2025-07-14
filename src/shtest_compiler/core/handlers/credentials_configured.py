from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    var = params.get('var') or params.get('groups', [None])[0] or "SQL_CONN"
    
    # Determine scope based on argument presence
    if not var or var == "SQL_CONN":
        scope = 'last_action'
    else:
        scope = params.get('scope', 'global')
    
    handler = params.get('handler', 'credentials_configured')
    expected = params.get('canonical_phrase', f"la variable {var} est configurée")
    opposite = params.get('opposite', f"la variable {var} n'est pas configurée")
    
    # Return atomic command only - no if/then/else logic
    actual_cmd = f"test -n \"${{{var}}}\""
    
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'var': var, 'opposite': opposite}
    ) 