import re
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Any
from parser.alias_resolver import AliasResolver
from .rule_registry import build_handler_map, load_default_rules
from common_patterns import (
    ACTION_RESULT_RE,
    ACTION_ONLY_RE,
    RESULT_ONLY_RE,
    STEP_RE,
    COMMENT_RE,
    SIMPLE_RULES,
)



@dataclass
class Rule:
    pattern: re.Pattern
    handler: Callable[[re.Match, Dict[str, Any]], None]


class Parser:
    """Parser for structured French-like test scenario descriptions."""

    def __init__(self) -> None:
        self.rules: List[Rule] = []
        self.arg_pattern = re.compile(
            r"(?:argument|paramètre|et\s+(?:l['ae]|l'))\s*(\S+)=\s*(\S+)", re.I
        )
        self._handler_map = build_handler_map()
        self.rules = [Rule(pat, h) for pat, h in load_default_rules(self._handler_map)]

    def _register(self, pattern: str, handler: Callable[[re.Match, Dict[str, Any]], None]) -> None:
        self.rules.append(Rule(re.compile(pattern, re.I), handler))

    def _register_default_rules(self) -> None:
        for rule in SIMPLE_RULES:
            pattern = rule["pattern"]
            handler_spec = rule["handler"]
            handler = self._make_handler(handler_spec)
            self._register(pattern, handler)

    def _build_handler_map(self) -> Dict[str, Callable[..., None]]:
        return {
            "initialization": lambda a, text: a["initialization"].append(text.strip()),
            "set_variable": lambda a, name, value: a["arguments"].update({name: value.strip()}),
            "sql_script": lambda a, line: self._handle_sql_script_text(line, a),
            "batch_script": lambda a, path: a.update({"batch_path": path}),
            "execution": lambda a, text: a["execution"].append(text.strip()),
            "validation": lambda a, expr: a["validation"].append(expr.rstrip(".;").strip()),
            "logs_check": lambda a, text: a["logs_check"].append(text.strip()),
            "arguments": lambda a, name, value: a["arguments"].update({name.strip(): value.strip()}),
            "variable": lambda a, name, value: a["arguments"].update({name.strip(): value.strip()}),
            "log_path": lambda a, path: a["log_paths"].append(path),
            "sql_script_single": lambda a, script: a["sql_scripts"].append(script) if script not in a["sql_scripts"] else None,
            "file_op": lambda a, op, typ, path, mode: a["file_operations"].append((op, typ, path, mode)),
            "create_dir": lambda a, path: a["file_operations"].append(("créer", "dossier", path, "0755")),
            "create_file": lambda a, path: a["file_operations"].append(("créer", "fichier", path, "0644")),
            "touch_date": lambda a, path, ts=None: a["touch_files"].append((path, ts)),
            "touch": lambda a, path, ts=None: a["touch_files"].append((path, ts)),
            "compare_files": lambda a, src, dest: a["compare_files"].append((src, dest)),
            "copy_move": lambda a, op, typ, src, dest: a["copy_operations"].append((op, typ or "fichier", src, dest)),
            "cat": lambda a, path: a["cat_files"].append(path),
            "purge_dir": lambda a, path: a["purge_dirs"].append(path),
        }

    def _make_handler(self, spec: str) -> Callable[[re.Match, Dict[str, Any]], None]:
        tokens = spec.split()
        name = tokens[0]
        arg_specs = tokens[1:]

        def get_value(match: re.Match, token: str) -> Optional[str]:
            if token.startswith("{{") and token.endswith("}}"):
                idx = int(token[2:-2])
                return match.group(idx) if idx <= match.lastindex else None
            if token.startswith("{") and token.endswith("}"):
                idx = int(token[1:-1])
                return match.group(idx)
            return token

        def _handler(match: re.Match, actions: Dict[str, Any]) -> None:
            args = [get_value(match, t) for t in arg_specs]
            func = self._handler_map[name]
            func(actions, *args)

        return _handler

    def _handle_sql_script_text(self, text: str, actions: Dict[str, Any]) -> None:
        scripts = re.findall(r"\S+\.sql", text, re.I)
        for path in scripts:
            if path not in actions["sql_scripts"]:
                actions["sql_scripts"].append(path)

    def _handle_arguments(self, match: re.Match, actions: Dict[str, Any]) -> None:
        for m in self.arg_pattern.finditer(match.string):
            actions["arguments"][m[1].strip()] = m[2].strip()

    def _handle_variable(self, match: re.Match, actions: Dict[str, Any]) -> None:
        actions["arguments"][match[1].strip()] = match[2].strip()

    def _handle_result_only(self, match: re.Match, actions: Dict[str, Any]) -> None:
        result = match[1].rstrip('.;').strip()
        if result:
            resolver = AliasResolver()
            actions["validation"].extend(resolver.resolve(result))

    def _handle_sql_script(self, match: re.Match, actions: Dict[str, Any]) -> None:
        scripts = re.findall(r"\S+\.sql", match.string, re.I)
        for path in scripts:
            if path not in actions["sql_scripts"]:
                actions["sql_scripts"].append(path)

    def _merge_actions(self, sub_actions: Dict[str, Any], actions: Dict[str, Any]) -> None:
        """Merge *sub_actions* dictionary into *actions*."""
        for key, value in sub_actions.items():
            if key == "batch_path" and value:
                actions[key] = value
            elif isinstance(value, dict):
                actions[key].update(value)
            elif isinstance(value, list):
                actions[key].extend(value)

    def _handle_action_result(self, match: re.Match, actions: Dict[str, Any]) -> None:
        sub_parser = Parser()
        action_text = match[1].rstrip(" ;")
        sub_actions = sub_parser.parse(action_text)
        self._merge_actions(sub_actions, actions)

        result = match[2].rstrip('.;').strip()
        if result:
            resolver = AliasResolver()
            resolved = resolver.resolve(result)
            if sub_actions.get("compare_files") and any(r.lower() == "les fichiers sont identiques" for r in resolved):
                src, dest = sub_actions["compare_files"][-1]
                actions["validation"].append(f"fichier_identique {src} {dest}")
            else:
                actions["validation"].extend(resolved)

    def parse(self, description: str) -> Dict[str, Any]:
        actions = {
            "initialization": [], "execution": [], "validation": [],
            "logs_check": [], "arguments": {}, "log_paths": [],
            "sql_scripts": [], "file_operations": [], "copy_operations": [],
            "cat_files": [], "touch_files": [], "purge_dirs": [], "compare_files": [],
            "steps": [], "batch_path": None,
        }

        for line in description.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if COMMENT_RE.match(stripped):
                continue

            m = STEP_RE.match(stripped)
            if m:
                actions["steps"].append(m.group(1).strip())
                continue

            m = ACTION_RESULT_RE.match(stripped)
            if m:
                self._handle_action_result(m, actions)
                continue

            m = ACTION_ONLY_RE.match(stripped)
            if m:
                sub_parser = Parser()
                sub_actions = sub_parser.parse(m.group(1).rstrip(" ;"))
                self._merge_actions(sub_actions, actions)
                continue

            m = RESULT_ONLY_RE.match(stripped)
            if m:
                self._handle_result_only(m, actions)
                continue

            for rule in self.rules:
                match = rule.pattern.search(stripped)
                if match:
                    rule.handler(match, actions)
        return actions
