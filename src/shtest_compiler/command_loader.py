import re
import yaml
import importlib
import os
from typing import Dict, Tuple, Optional

PATTERNS_PATH = os.path.join(os.path.dirname(__file__), "config", "patterns_actions.yml")
with open(PATTERNS_PATH, encoding="utf-8") as f:
    PATTERNS = yaml.safe_load(f)["actions"]

class PatternRegistry:
    def __init__(self, actions_yml, validations_yml):
        self.actions = self._load_patterns(actions_yml, 'actions')
        self.validations = self._load_patterns(validations_yml, 'validations')

    def _load_patterns(self, yml_path, section):
        if not os.path.exists(yml_path):
            raise FileNotFoundError(f"YAML file not found: {yml_path}")
        with open(yml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        canonicals = {}
        alias_map = {}
        regex_aliases = []
        for entry in data.get(section, []):
            phrase = entry["phrase"]
            handler = entry["handler"]
            canonicals[self._normalize(phrase)] = {"phrase": phrase, "handler": handler}
            for alias in entry.get("aliases", []):
                alias_map[self._normalize(alias)] = phrase
                # Si l'alias contient des caractères regex, on le stocke aussi comme regex
                if self._is_regex(alias):
                    regex_aliases.append((alias, phrase))
        return {"canonicals": canonicals, "alias_map": alias_map, "regex_aliases": regex_aliases}

    def _normalize(self, phrase):
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

    def canonize_validation(self, phrase) -> Optional[Tuple[str, str]]:
        norm = self._normalize(phrase)
        validations = self.validations
        # 1. Match exact
        if norm in validations["canonicals"]:
            entry = validations["canonicals"][norm]
            return entry["phrase"], entry["handler"]
        # 2. Alias exact
        if norm in validations["alias_map"]:
            canonical = validations["alias_map"][norm]
            entry = validations["canonicals"][self._normalize(canonical)]
            return entry["phrase"], entry["handler"]
        # 3. Alias regex
        for regex, canonical in validations["regex_aliases"]:
            try:
                if re.match(regex, phrase):
                    entry = validations["canonicals"][self._normalize(canonical)]
                    return entry["phrase"], entry["handler"]
            except re.error:
                continue
        return None

# Exemple d'utilisation :
# registry = PatternRegistry('config/patterns_actions.yml', 'config/patterns_validations.yml')
# print(registry.canonize_action('faire un dossier {path}'))
# print(registry.canonize_validation('le dossier est cree'))

def load_plugin(command_type):
    return importlib.import_module(f"shtest_compiler.plugins.{command_type}")

def action_to_ast(action):
    for entry in PATTERNS:
        m = re.match(entry["pattern"], action, re.IGNORECASE)
        if m:
            plugin = load_plugin(entry["type"])
            return plugin.handle(m.groups())
    return None  # ou lever une exception 