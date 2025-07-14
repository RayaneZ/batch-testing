from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    code = params.get("code")
    
    # Determine scope based on argument presence
    if not code:
        scope = 'last_action'
    else:
        scope = params.get('scope', 'global')
    
    handler = params.get('handler', 'return_code')
    expected = params.get('canonical_phrase', f"le code de retour est {code}")
    opposite = params.get('opposite', f"le code de retour n'est pas {code}")
    
    # Use $last_ret instead of $? to check the return code of the executed command
    # $last_ret is set by the run_action function
    actual_cmd = f"test $last_ret -eq {code}"
    
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'code': code, 'opposite': opposite}
    ) 