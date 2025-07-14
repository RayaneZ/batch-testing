from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    # Try to get file and date from params or groups
    file = params.get('file') or params.get('groups', [None, None])[0]
    date = params.get('date') or params.get('groups', [None, None])[1]
    last_file_var = params.get('last_file_var', None)
    last_action = params.get('last_action', None)
    action_context = params.get('action_context', {})

    # Try to extract from action_context if not provided
    if (not file or not date) and action_context and isinstance(action_context, dict):
        command = action_context.get('command', '')
        if command:
            try:
                from shtest_compiler.compiler.argument_extractor import extract_action_args
                extracted = extract_action_args(command)
                if extracted:
                    file = file or extracted.get('file') or extracted.get('path')
                    date = date or extracted.get('date') or extracted.get('timestamp')
            except Exception:
                pass

    # Fallback: try to infer from last_action if not provided
    if (not file or not date) and last_action and isinstance(last_action, dict):
        file = file or last_action.get('file')
        date = date or last_action.get('date')

    # Fallback: use last_file_var if file is still missing
    if not file and last_file_var:
        file = last_file_var

    # Determine scope based on argument presence
    if not file or not date:
        scope = 'last_action'
    else:
        scope = params.get('scope', 'global')

    if not file or not date:
        return ValidationCheck(
            expected='date_modified',
            actual_cmd="echo 'ERROR: Missing file or date for date_modified validation'",
            handler='date_modified',
            scope=scope,
            params=params
        )

    # Return atomic command only - no if/then/else logic
    actual_cmd = f"test \"$(date -r '{file}' +%Y%m%d%H%M)\" = '{date}'"
    
    return ValidationCheck(
        expected='date_modified',
        actual_cmd=actual_cmd,
        handler='date_modified',
        scope=scope,
        params={'file': file, 'date': date}
    ) 