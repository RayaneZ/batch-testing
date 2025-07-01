"""Common regex patterns loaded from ``regex_config.yml``."""

from __future__ import annotations

import os
import re
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "regex_config.yml")
SIMPLE_RULES_PATH = os.path.join(os.path.dirname(__file__), "simple_rules.yml")

with open(CONFIG_PATH, encoding="utf-8") as f:
    _PATTERNS = yaml.safe_load(f)

with open(SIMPLE_RULES_PATH, encoding="utf-8") as f:
    SIMPLE_RULES: list[dict[str, str]] = yaml.safe_load(f)

STEP_RE = re.compile(_PATTERNS["step"], re.IGNORECASE)
ACTION_RESULT_RE = re.compile(_PATTERNS["action_result"], re.IGNORECASE)
ACTION_ONLY_RE = re.compile(_PATTERNS["action_only"], re.IGNORECASE)
RESULT_ONLY_RE = re.compile(_PATTERNS["result_only"], re.IGNORECASE)
COMMENT_RE = re.compile(_PATTERNS["comment"], re.IGNORECASE)
