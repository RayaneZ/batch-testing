import importlib
import os
import re
from typing import Dict, Optional, Tuple

import yaml

PATTERNS_PATH = os.path.join(
    os.path.dirname(__file__), "config", "patterns_actions.yml"
)
with open(PATTERNS_PATH, encoding="utf-8") as f:
    PATTERNS = yaml.safe_load(f)["actions"]


class PatternRegistry:
    def __init__(self, actions_yml, validations_yml):
        self.actions = self._load_patterns(actions_yml, "actions")
        self.validations = self._load_patterns(validations_yml, "validations")

    def _load_patterns(self, yml_path, section):
        if not os.path.exists(yml_path):
            raise FileNotFoundError(f"YAML file not found: {yml_path}")
        with open(yml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        canonicals = {}
        alias_map = {}
        regex_aliases = []
        for entry in data.get(section, []):
            phrase = entry.get("phrase")
            handler = entry.get("handler")
            if not phrase:
                print(f"Warning: Skipping entry without 'phrase': {entry}")
                continue
            # Stocker aussi le scope s'il existe
            scope = entry.get("scope", "global")  # Default to global
            canonicals[self._normalize(phrase)] = {
                "phrase": phrase,
                "handler": handler,
                "scope": scope,
            }
            for alias in entry.get("aliases", []):
                # If alias is a dict, extract the string value
                if isinstance(alias, dict):
                    alias_str = alias.get("pattern") or alias.get("phrase")
                    if not alias_str:
                        print(
                            f"Warning: Skipping alias without 'pattern' or 'phrase': {alias}"
                        )
                        continue
                else:
                    alias_str = alias
                alias_map[self._normalize(alias_str)] = phrase
                # Si l'alias contient des caractères regex, on le stocke aussi comme regex
                if self._is_regex(alias_str):
                    regex_aliases.append((alias_str, phrase))
        return {
            "canonicals": canonicals,
            "alias_map": alias_map,
            "regex_aliases": regex_aliases,
        }

    def _normalize(self, phrase):
        # If phrase is a dict, extract the string value
        if isinstance(phrase, dict):
            phrase = phrase.get("pattern") or phrase.get("phrase")
        if phrase is None:
            return ""
        return phrase.lower().strip()

    def _is_regex(self, alias):
        # Heuristique simple : présence de caractères regex courants
        return any(c in alias for c in ".*+?^$[](){}|\\")

    def canonize_action(self, phrase) -> Optional[Tuple[str, str]]:
        norm = self._normalize(phrase)
        actions = self.actions
        # 1. Match exact
        if norm in actions["canonicals"]:
            entry = actions["canonicals"][norm]
            return entry["phrase"], entry["handler"]
        # 2. Alias exact
        if norm in actions["alias_map"]:
            canonical = actions["alias_map"][norm]
            entry = actions["canonicals"][self._normalize(canonical)]
            return entry["phrase"], entry["handler"]
        # 3. Alias regex
        for regex, canonical in actions["regex_aliases"]:
            try:
                if re.match(regex, phrase):
                    entry = actions["canonicals"][self._normalize(canonical)]
                    return entry["phrase"], entry["handler"]
            except re.error:
                continue
        return None

    def canonize_validation(self, phrase) -> Optional[Tuple[str, str, str]]:
        norm = self._normalize(phrase)
        validations = self.validations
        # 1. Match exact
        if norm in validations["canonicals"]:
            entry = validations["canonicals"][norm]
            return entry["phrase"], entry["handler"], entry.get("scope", "global")
        # 2. Alias exact
        if norm in validations["alias_map"]:
            canonical = validations["alias_map"][norm]
            entry = validations["canonicals"][self._normalize(canonical)]
            return entry["phrase"], entry["handler"], entry.get("scope", "global")
        # 3. Alias regex
        for regex, canonical in validations["regex_aliases"]:
            try:
                if re.match(regex, phrase):
                    entry = validations["canonicals"][self._normalize(canonical)]
                    return (
                        entry["phrase"],
                        entry["handler"],
                        entry.get("scope", "global"),
                    )
            except re.error:
                continue
        return None


# Exemple d'utilisation :
# registry = PatternRegistry('config/patterns_actions.yml', 'config/patterns_validations.yml')
# print(registry.canonize_action('faire un dossier {path}'))
# print(registry.canonize_validation('le dossier est cree'))


def load_plugin(command_type):
    # Mapping des handlers vers les vrais modules
    handler_mapping = {
        # Actions (now in core.action_handlers)
        "create_dir": "core.action_handlers.create_dir",
        "delete_dir": "core.action_handlers.delete_dir",
        "copy_dir": "core.action_handlers.copy_dir",
        "move_dir": "core.action_handlers.move_dir",
        "purge_dir": "core.action_handlers.purge_dir",
        "create_file": "core.action_handlers.create_file",
        "delete_file": "core.action_handlers.delete_file",
        "copy_file": "core.action_handlers.copy_file",
        "move_file": "core.action_handlers.move_file",
        "cat_file": "core.action_handlers.cat_file",
        "compare_files": "core.action_handlers.compare_files",  # If implemented
        "touch_ts": "core.action_handlers.touch_ts",
        "run_script": "core.action_handlers.run_script",
        "run_sql_script": "core.action_handlers.run_sql_script",
        "export_var": "core.action_handlers.export_var",
        "update_file": "core.action_handlers.create_file",  # Fallback vers create_file
        # Validations (still in core.handlers)
        "return_code": "core.handlers.return_code",
        "content_displayed": "core.handlers.content_displayed",
        "file_copied": "core.handlers.file_copied",
        "dir_copied": "core.handlers.dir_copied",
        "file_present": "core.handlers.file_present",
        "dir_exists": "core.handlers.dir_exists",
        "dir_absent": "core.handlers.dir_absent",
        "base_ready": "core.handlers.base_ready",
        "date_modified": "core.handlers.date_modified",
        "files_identical": "core.handlers.files_identical",
        "credentials_configured": "core.handlers.credentials_configured",
        "logs_accessible": "core.handlers.logs_accessible",
        "no_error_message": "core.handlers.no_error_message",
        "stdout_contains": "core.handlers.stdout_contains",
        "stderr_contains": "core.handlers.stderr_contains",
    }
    module_name = handler_mapping.get(command_type, command_type)
    return importlib.import_module(f"shtest_compiler.{module_name}")


def action_to_ast(action):
    for entry in PATTERNS:
        m = re.match(entry["phrase"], action, re.IGNORECASE)
        if m:
            plugin = load_plugin(entry["handler"])
            if entry["handler"] == "run_sql_script":
                driver = os.environ.get("SQL_DRIVER", "oracle")
                return plugin.handle({"script": m.groups()[0], "driver": driver})
            else:
                # Map groups to params by name if possible
                params = {
                    k: v
                    for k, v in zip(
                        re.findall(r"\{(\w+)\}", entry["phrase"]), m.groups()
                    )
                }
                return plugin.handle(params)
        for alias in entry.get("aliases", []):
            m = re.match(alias, action, re.IGNORECASE)
            if m:
                plugin = load_plugin(entry["handler"])
                if entry["handler"] == "run_sql_script":
                    driver = os.environ.get("SQL_DRIVER", "oracle")
                    return plugin.handle({"script": m.groups()[0], "driver": driver})
                else:
                    params = {
                        k: v
                        for k, v in zip(
                            re.findall(r"\{(\w+)\}", entry["phrase"]), m.groups()
                        )
                    }
                    return plugin.handle(params)
    return None
