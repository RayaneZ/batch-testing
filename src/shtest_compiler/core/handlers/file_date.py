from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    file = params.get("file")
    date = params.get("date")
    handler = "file_date"

    # Try to extract from context if missing
    context = params.get("context", {})
    if not file:
        file = context.get("variables", {}).get("file") or file
    if not date:
        date = context.get("variables", {}).get("date") or date
    last_action = context.get("last_action", {})
    if not file and isinstance(last_action, dict):
        file = last_action.get("file") or file
    if not date and isinstance(last_action, dict):
        date = last_action.get("date") or date

    if not file:
        scope = "last_action"
    else:
        scope = params.get("scope", "global")

    # Use canonical phrase and opposite directly
    phrase = "La date du fichier {file} est {date}"
    opposite = "La date du fichier {file} n'est pas {date}"

    expected = params.get("canonical_phrase", phrase)
    opposite_msg = params.get("opposite", opposite)
    # Atomic check: compare file modification date
    actual_cmd = f'[ "$(date -r {file} +%Y%m%d%H%M)" = "{date}" ]'
    return ValidationCheck(
        expected=expected,
        actual_cmd=actual_cmd,
        handler=handler,
        scope=scope,
        params={"file": file, "date": date, "opposite": opposite_msg},
    )
