"""
Registry central des matchers (patterns) et handlers pour SHTEST.
- Charge tous les patterns génériques (built-in) et plugins (YAML)
- Associe chaque pattern à un handler Python
- Fournit load_rules() pour le parser
- Charge dynamiquement les handlers déclarés dans chaque plugin (PLUGIN_HANDLERS)
"""
import re
import yaml
from pathlib import Path
import glob
import importlib.util

# === 1. Charger les patterns d'actions et de validations ===
ACTIONS_CONFIG_PATH = Path(__file__).parent / "patterns_actions.yml"
VALIDATIONS_CONFIG_PATH = Path(__file__).parent / "patterns_validations.yml"

print("🔁 Loading YAML from", ACTIONS_CONFIG_PATH)
with open(ACTIONS_CONFIG_PATH, encoding="utf-8") as f:
    actions_patterns = yaml.safe_load(f)["actions"]

print("🔁 Loading YAML from", VALIDATIONS_CONFIG_PATH)
with open(VALIDATIONS_CONFIG_PATH, encoding="utf-8") as f:
    validations_patterns = yaml.safe_load(f)["validations"]

# === 2. Charger dynamiquement les patterns de chaque plugin ===
PLUGINS_DIR = Path(__file__).parent.parent / "plugins"
plugin_patterns = {}
for plugin_dir in PLUGINS_DIR.iterdir():
    config_dir = plugin_dir / "config"
    if config_dir.exists():
        for yml_file in config_dir.glob("patterns_*.yml"):
            with open(yml_file, encoding="utf-8") as f:
                patterns = yaml.safe_load(f).get("patterns", {})
                for section, entries in patterns.items():
                    plugin_patterns.setdefault(section, []).extend(entries)

# === 3. Fusionner tous les patterns (actions, validations, plugins) ===
ALL_PATTERNS = {"actions": [], "validations": []}
ALL_PATTERNS["actions"].extend(actions_patterns)
ALL_PATTERNS["validations"].extend(validations_patterns)
for section, entries in plugin_patterns.items():
    ALL_PATTERNS.setdefault(section, []).extend(entries)

# === 4. Dictionnaire des handlers ===
HANDLERS = {
    # Built-in handlers
    "initialization": lambda a, text: a["initialization"].append(text.strip()),
    "set_variable": lambda a, name, value: a["arguments"].update({name: value.strip()}),
    "sql_script": lambda a, line: _handle_sql_script_text(line, a),
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

# === 5. Charger dynamiquement les handlers plugins (PLUGIN_HANDLERS) ===
for plugin_dir in PLUGINS_DIR.iterdir():
    plugin_py = plugin_dir / f"{plugin_dir.name}.py"
    if plugin_py.exists():
        spec = importlib.util.spec_from_file_location(
            f"shtest_compiler.plugins.{plugin_dir.name}.{plugin_dir.name}", plugin_py
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "PLUGIN_HANDLERS"):
            HANDLERS.update(module.PLUGIN_HANDLERS)

def _handle_sql_script_text(text, actions):
    scripts = re.findall(r"\S+\.sql", text, re.I)
    for path in scripts:
        if path not in actions["sql_scripts"]:
            actions["sql_scripts"].append(path)

def load_rules():
    """
    Retourne la liste [(pattern, handler)] pour le parser.
    Chaque pattern est une regex compilée, chaque handler est une fonction Python.
    """
    rules = []
    for section, entries in ALL_PATTERNS.items():
        for entry in entries:
            pattern = re.compile(entry["pattern"], re.IGNORECASE)
            handler = HANDLERS[entry["handler"]]
            rules.append((pattern, handler))
    return rules
