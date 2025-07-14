import os

import yaml


def get_canonical_phrase_and_opposite(handler, plugin_name=None):
    # 1. Try plugin-specific YAML
    if plugin_name:
        plugin_path = os.path.join(
            os.path.dirname(__file__),
            f"../plugins/{plugin_name}/config/patterns_{plugin_name}.yml",
        )
        if os.path.exists(plugin_path):
            with open(plugin_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
                for section, patterns in data.get("patterns", {}).items():
                    for entry in patterns:
                        if entry.get("handler") == handler:
                            phrase = entry.get("pattern")
                            opposite = entry.get("opposite", None)
                            return phrase, opposite
    # 2. Fallback to built-in YAML
    builtin_path = os.path.join(
        os.path.dirname(__file__), "../config/patterns_validations.yml"
    )
    with open(builtin_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
        for entry in data.get("validations", []):
            if entry.get("handler") == handler:
                phrase = entry.get("phrase")
                opposite = (
                    entry.get("opposite", {}).get("phrase")
                    if entry.get("opposite")
                    else None
                )
                return phrase, opposite
    return None, None


def shell_escape(value):
    """Escape a string for safe use in single-quoted shell strings."""
    if value is None:
        return ""
    return "'" + str(value).replace("'", "'\\''") + "'"
