import re
import yaml
import os
from typing import Dict, Any, Optional

# Load action patterns from YAML
PATTERNS_PATH = os.path.join(
    os.path.dirname(__file__), "../config/patterns_actions.yml"
)


def load_action_patterns():
    with open(PATTERNS_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("actions", [])


def build_regex_from_phrase(phrase: str) -> str:
    # Replace {var} with named regex groups
    regex = re.sub(r"{(\w+)}", r"(?P<\1>.+)", phrase)
    regex = "^" + regex + "$"
    return regex


def extract_action_args(command: str) -> Optional[Dict[str, str]]:
    """
    Try to match the command to a pattern and extract arguments.
    Returns a dict of argument names to values, or None if no match.
    """
    patterns = load_action_patterns()
    for action in patterns:
        # Try main phrase
        regex = build_regex_from_phrase(action["phrase"])
        m = re.match(regex, command)
        if m:
            return m.groupdict()
        # Try aliases
        for alias in action.get("aliases", []):
            # If alias is a dict (from YAML), extract the pattern string
            if isinstance(alias, dict):
                alias_str = alias.get("pattern") or alias.get("phrase")
                if not alias_str:
                    continue
            else:
                alias_str = alias
            # If alias has {var}, treat as phrase
            if "{" in alias_str:
                regex = build_regex_from_phrase(alias_str)
            else:
                regex = alias_str
            try:
                m = re.match(regex, command)
            except re.error:
                continue
            if m:
                # If alias uses named groups, return them; else use positional
                if m.groupdict():
                    return m.groupdict()
                else:
                    # Map to generic arg names
                    return {f"arg{i+1}": v for i, v in enumerate(m.groups())}
    return None
