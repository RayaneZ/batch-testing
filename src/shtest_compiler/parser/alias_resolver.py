
from shtest_compiler.parser.shunting_yard import VarEquals
import re

def resolve_alias(resolved: str):
    resolved = resolved.strip()
    if resolved.startswith("variable "):
        match = re.match(r"variable\s+([^\s]+)\s+vaut\s+(.+)", resolved, re.IGNORECASE)
        if match:
            var, value = match.groups()
            return VarEquals(var=var.strip(), expected=value.strip())
    return None


__all__ = ["resolve_alias"]
