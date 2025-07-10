import re
from parser.shunting_yard import (
    VarEquals,
    StdoutContains,
    StderrContains,
    SQLScriptExecution
)

__all__ = ["resolve_alias"]

def resolve_alias(resolved: str):
    resolved = resolved.strip()

    match = re.match(r"variable\s+([^\s]+)\s+vaut\s+(.+)", resolved, re.IGNORECASE)
    if match:
        var, value = match.groups()
        return VarEquals(variable=var.strip(), expected=value.strip())

    match = re.match(r"stdout\s+contient\s+(.+)", resolved, re.IGNORECASE)
    if match:
        return StdoutContains(expected=match.group(1).strip())

    match = re.match(r"stderr\s+contient\s+(.+)", resolved, re.IGNORECASE)
    if match:
        return StderrContains(expected=match.group(1).strip())

    match = re.match(r"(\S+\.sql)", resolved, re.IGNORECASE)
    if match:
        return SQLScriptExecution(script=match.group(1).strip())

    return None