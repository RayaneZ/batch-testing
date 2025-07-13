from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    file = params.get('file')
    date = params.get('date')
    if not file or not date:
        return ValidationCheck(
            expected='file_date',
            actual_cmd="echo 'ERROR: Missing file or date for file_date validation'",
            handler='file_date',
            scope=params.get('scope', 'last_action'),
            params=params
        )
    # Return just the command, let the shell construction be handled by the node
    cmd = f"date -r '{file}' +%Y%m%d%H%M"
    return ValidationCheck(
        expected='file_date',
        actual_cmd=cmd,
        handler='file_date',
        scope=params.get('scope', 'last_action'),
        params=params
    ) 