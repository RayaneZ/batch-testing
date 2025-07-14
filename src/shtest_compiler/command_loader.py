import importlib
import os
import re
from typing import Callable, Dict, List, Optional, Tuple

import yaml

from .utils.logger import SingletonLogger
from shtest_compiler.utils.shell_utils import resource_path

CORE_CONFIG_PATH = resource_path("config")
PLUGINS_PATH = resource_path("plugins")


# --- YAML Loader Utilities ---
def load_yaml(path):
    with open(resource_path(path), encoding="utf-8") as f:
        return yaml.safe_load(f)


def discover_plugins():
    return [
        name
        for name in os.listdir(PLUGINS_PATH)
        if os.path.isdir(os.path.join(PLUGINS_PATH, name))
    ]


def find_plugin_yaml(plugin, kind):
    # kind: 'actions' or 'validations'
    config_dir = os.path.join(PLUGINS_PATH, plugin, "config")
    # Try standard names
    candidates = [
        f"patterns_{kind}.yml",
        f"patterns_{plugin}.yml",
    ]
    # Also accept any yml in config dir
    if os.path.exists(config_dir):
        for fname in os.listdir(config_dir):
            if fname.endswith(".yml") and kind in fname:
                candidates.append(fname)
    for fname in candidates:
        path = os.path.join(config_dir, fname)
        if os.path.exists(path):
            return path
    return None


def merge_yaml_lists(core_list, plugin_lists):
    merged = list(core_list)
    for plugin in plugin_lists:
        merged.extend(plugin)
    return merged


def load_and_merge_patterns():
    # Load core
    core_actions = load_yaml(os.path.join(CORE_CONFIG_PATH, "patterns_actions.yml"))[
        "actions"
    ]
    core_validations = load_yaml(
        os.path.join(CORE_CONFIG_PATH, "patterns_validations.yml")
    )["validations"]
    # Load plugins
    plugin_actions, plugin_validations = [], []
    for plugin in discover_plugins():
        actions_path = find_plugin_yaml(plugin, "actions")
        validations_path = find_plugin_yaml(plugin, "validations")
        if actions_path:
            plugin_actions.append(
                load_yaml(actions_path).get("actions")
                or load_yaml(actions_path).get("patterns", [])
            )
        if validations_path:
            plugin_validations.append(
                load_yaml(validations_path).get("validations")
                or load_yaml(validations_path).get("patterns", [])
            )
    all_actions = merge_yaml_lists(core_actions, plugin_actions)
    all_validations = merge_yaml_lists(core_validations, plugin_validations)
    return all_actions, all_validations


def find_handler(handler_name, is_action, entry=None):
    # Try core first
    try:
        if is_action:
            mod = importlib.import_module(
                f"shtest_compiler.core.action_handlers.{handler_name}"
            )
        else:
            mod = importlib.import_module(
                f"shtest_compiler.core.handlers.{handler_name}"
            )
        return mod.handle
    except ImportError:
        # Try plugins
        for plugin in discover_plugins():
            try:
                if is_action:
                    mod = importlib.import_module(
                        f"shtest_compiler.plugins.{plugin}.action_handlers.{handler_name}"
                    )
                else:
                    mod = importlib.import_module(
                        f"shtest_compiler.plugins.{plugin}.handlers.{handler_name}"
                    )
                return mod.handle
            except ImportError:
                continue
        # Enhanced error message
        error_msg = f"Handler '{handler_name}' (is_action={is_action}) not found in core or plugins."
        if entry is not None:
            error_msg += (
                f"\nTo implement this handler, create a Python file named '{handler_name}.py' "
                f"\nin the appropriate directory: "
                f"\n'shtest_compiler/core/{'action_handlers' if is_action else 'handlers'}' for core, "
                f"\nor 'shtest_compiler/plugins/<your_plugin>/{'action_handlers' if is_action else 'handlers'}' for plugins. "
                f"\nThe handler should define a 'handle(params)' function.\n"
                f"Pattern entry for reference: {entry}"
            )
        raise ImportError(error_msg)


def build_registry():
    all_actions, all_validations = load_and_merge_patterns()
    handler_registry = {}
    for entry in all_actions:
        handler_registry[entry["handler"]] = find_handler(
            entry["handler"], is_action=True, entry=entry
        )
    for entry in all_validations:
        handler_registry[entry["handler"]] = find_handler(
            entry["handler"], is_action=False, entry=entry
        )
    return handler_registry, all_actions, all_validations


def find_handler_requirements_yaml(base_path):
    config_dir = os.path.join(base_path, "config")
    candidates = [
        "handler_requirements.yml",
        "handler_requirements.yaml",
    ]
    for fname in candidates:
        path = os.path.join(config_dir, fname)
        if os.path.exists(path):
            return path
    return None


def load_and_merge_handler_requirements():
    # Load core requirements
    core_path = find_handler_requirements_yaml(CORE_CONFIG_PATH)
    requirements = {}
    if core_path:
        core_reqs = load_yaml(core_path)
        if core_reqs:
            requirements.update(core_reqs)
    # Load plugin requirements
    for plugin in discover_plugins():
        plugin_path = find_handler_requirements_yaml(os.path.join(PLUGINS_PATH, plugin))
        if plugin_path:
            plugin_reqs = load_yaml(plugin_path)
            if plugin_reqs:
                requirements.update(plugin_reqs)
    return requirements


def get_handler_requirements():
    """
    Returns a merged dictionary of all handler requirements (core + plugins), keyed by handler name.
    """
    return load_and_merge_handler_requirements()


# --- PatternRegistry (unchanged, but now can be initialized with merged YAMLs) ---
class PatternRegistry:
    def __init__(self, actions_list, validations_list):
        self.actions = self._load_patterns(actions_list)
        self.validations = self._load_patterns(validations_list)

    def _load_patterns(self, data, section=None):
        canonicals = {}
        alias_map = {}
        regex_aliases = []
        logger = SingletonLogger()
        for entry in data:
            phrase = entry.get("phrase") or entry.get("pattern")
            handler = entry.get("handler")
            if not phrase:
                logger.warning(f"Skipping entry without 'phrase' or 'pattern': {entry}")
                continue
            scope = entry.get("scope", "global")
            canonicals[self._normalize(phrase)] = {
                "phrase": phrase,
                "handler": handler,
                "scope": scope,
            }
            for alias in entry.get("aliases", []):
                alias_str = alias.get("pattern") if isinstance(alias, dict) else alias
                if not alias_str:
                    continue
                alias_map[self._normalize(alias_str)] = phrase
                if self._is_regex(alias_str):
                    regex_aliases.append((alias_str, phrase))
        return {
            "canonicals": canonicals,
            "alias_map": alias_map,
            "regex_aliases": regex_aliases,
        }

    def _normalize(self, phrase):
        if isinstance(phrase, dict):
            phrase = phrase.get("pattern") or phrase.get("phrase")
        if phrase is None:
            return ""
        return phrase.lower().strip()

    def _is_regex(self, alias):
        return any(c in alias for c in ".*+?^$[](){}|\\")

    def canonize_action(self, phrase) -> Optional[Tuple[str, str]]:
        norm = self._normalize(phrase)
        actions = self.actions
        if norm in actions["canonicals"]:
            entry = actions["canonicals"][norm]
            return entry["phrase"], entry["handler"]
        if norm in actions["alias_map"]:
            canonical = actions["alias_map"][norm]
            entry = actions["canonicals"][self._normalize(canonical)]
            return entry["phrase"], entry["handler"]
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
        if norm in validations["canonicals"]:
            entry = validations["canonicals"][norm]
            return entry["phrase"], entry["handler"], entry.get("scope", "global")
        if norm in validations["alias_map"]:
            canonical = validations["alias_map"][norm]
            entry = validations["canonicals"][self._normalize(canonical)]
            return entry["phrase"], entry["handler"], entry.get("scope", "global")
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


# --- Unified Handler Dispatch Example ---
# Usage:
# handler_registry, all_actions, all_validations = build_registry()
# registry = PatternRegistry(all_actions, all_validations)
# phrase, handler_name = registry.canonize_action("créer le fichier test.txt")
# handler = handler_registry[handler_name]
# handler(params)
