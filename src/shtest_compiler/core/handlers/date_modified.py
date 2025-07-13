from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    # Try to get file and date from params or groups
    file = params.get('file') or params.get('groups', [None, None])[0]
    date = params.get('date') or params.get('groups', [None, None])[1]
    last_file_var = params.get('last_file_var', None)
    last_action = params.get('last_action', None)

    # Fallback: try to infer from last_action if not provided
    if (not file or not date) and last_action and isinstance(last_action, dict):
        # Example: last_action = {'type': 'touch', 'file': 'foo.txt', 'date': '202401010101'}
        file = file or last_action.get('file')
        date = date or last_action.get('date')

    # Fallback: use last_file_var if file is still missing
    if not file and last_file_var:
        file = last_file_var

    if not file or not date:
        return ValidationCheck(
            expected='date_modified',
            actual_cmd="echo 'ERROR: Missing file or date for date_modified validation'",
            handler='date_modified',
            scope=params.get('scope', 'last_action'),
            params=params
        )

    # Return just the command, let the shell construction be handled by the node
    cmd = f"date -r '{file}' +%Y%m%d%H%M"
    return ValidationCheck(
        expected='date_modified',
        actual_cmd=cmd,
        handler='date_modified',
        scope=params.get('scope', 'last_action'),
        params=params
    ) 