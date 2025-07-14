from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    var = params.get('var')
    value = params.get('value')
    
    # Determine scope based on argument presence
    if not var or not value:
        scope = 'last_action'
    else:
        scope = params.get('scope', 'global')
    
    expected = f"variable {var} vaut {value}"
    opposite = f"variable {var} ne vaut pas {value}"
    
    # Return atomic command only - no if/then/else logic
    actual_cmd = f"test \"${var}\" = \"{value}\""
    
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler="var_equals",
        scope=scope,
        params={'var': var, 'value': value, 'opposite': opposite}
    ) 