from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    file = params.get('file')
    date = params.get('date')
    handler = 'file_date'
    
    # If file is missing, this validation depends on the last action's context
    if not file:
        scope = 'last_action'
    else:
        scope = params.get('scope', 'global')
    
    if not file or not date:
        return ValidationCheck(
            expected='file_date',
            actual_cmd="false",  # Always fail if missing params
            handler=handler,
            scope=scope,
            params=params
        )
    # Atomic check: compare file modification date
    actual_cmd = f"[ \"$(date -r {file} +%Y%m%d%H%M)\" = \"{date}\" ]"
    return ValidationCheck(
        expected=f"le fichier {file} a la date {date}",
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={'file': file, 'date': date}
    ) 