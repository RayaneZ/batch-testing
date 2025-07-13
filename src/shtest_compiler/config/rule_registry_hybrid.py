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

print("Loading YAML from", ACTIONS_CONFIG_PATH)
with open(ACTIONS_CONFIG_PATH, encoding="utf-8") as f:
    actions_patterns = yaml.safe_load(f)["actions"]

print("Loading YAML from", VALIDATIONS_CONFIG_PATH)
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
    "initialization": lambda a, text: _add_to_list(a, "initialization", text.strip()),
    "set_variable": lambda a, name, value: _set_variable(a, name, value.strip()),
    "sql_script": lambda a, line: _handle_sql_script_text(line, a),
    "batch_script": lambda a, path: _set_dict_value(a, "batch_path", path),
    "execution": lambda a, text: _add_to_list(a, "execution", text.strip()),
    "validation": lambda a, expr: _add_to_list(a, "validation", expr.rstrip(".;").strip()),
    "logs_check": lambda a, text: _add_to_list(a, "logs_check", text.strip()),
    "arguments": lambda a, name, value: _set_dict_value(a, "arguments", {name.strip(): value.strip()}),
    "variable": lambda a, name, value: _set_dict_value(a, "arguments", {name.strip(): value.strip()}),
    "log_path": lambda a, path: _add_to_list(a, "log_paths", path),
    "sql_script_single": lambda a, script: _add_to_list_if_not_exists(a, "sql_scripts", script),
    "file_op": lambda a, op, typ, path, mode: _add_to_list(a, "file_operations", (op, typ, path, mode)),
    "create_dir": lambda a, path: _add_to_list(a, "file_operations", ("créer", "dossier", path, "0755")),
    "create_file": lambda a, path: _add_to_list(a, "file_operations", ("créer", "fichier", path, "0644")),
    "touch_date": lambda a, path, ts=None: _add_to_list(a, "touch_files", (path, ts)),
    "touch": lambda a, path, ts=None: _add_to_list(a, "touch_files", (path, ts)),
    "compare_files": lambda a, src, dest: _add_to_list(a, "compare_files", (src, dest)),
    "copy_move": lambda a, op, typ, src, dest: _add_to_list(a, "copy_operations", (op, typ or "fichier", src, dest)),
    "cat": lambda a, path: _add_to_list(a, "cat_files", path),
    "purge_dir": lambda a, path: _add_to_list(a, "purge_dirs", path),
    
    # Additional handlers for actions
    "delete_dir": lambda a, path: _add_to_list(a, "file_operations", ("supprimer", "dossier", path, "0755")),
    "copy_dir": lambda a, src, dest: _add_to_list(a, "copy_operations", ("copier", "dossier", src, dest)),
    "move_dir": lambda a, src, dest: _add_to_list(a, "copy_operations", ("déplacer", "dossier", src, dest)),
    "delete_file": lambda a, path: _add_to_list(a, "file_operations", ("supprimer", "fichier", path, "0644")),
    "copy_file": lambda a, src, dest: _add_to_list(a, "copy_operations", ("copier", "fichier", src, dest)),
    "move_file": lambda a, src, dest: _add_to_list(a, "copy_operations", ("déplacer", "fichier", src, dest)),
    "cat_file": lambda a, path: _add_to_list(a, "cat_files", path),
    "run_script": lambda a, script: _add_to_list(a, "execution", f"sh {script}"),
    "run_sql_script": lambda a, script: _add_to_list(a, "sql_scripts", script),
    "export_var": lambda a, var, value: _set_dict_value(a, "arguments", {var: value}),
    "touch_ts": lambda a, path, timestamp: _add_to_list(a, "touch_files", (path, timestamp)),
    "update_file": lambda a, path, mode: _add_to_list(a, "file_operations", ("mettre à jour", "fichier", path, mode)),
    
    # Validation handlers - these expect different signatures
    "content_displayed": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "file_copied": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "dir_copied": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "file_present": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "file_absent": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "dir_ready": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "base_ready": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "date_modified": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "return_code": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "files_identical": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "credentials_configured": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "logs_accessible": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "no_error_message": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "stdout_contains": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "stderr_contains": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "file_contains": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "file_exists": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
    "file_empty": lambda a, *args: _add_to_list(a, "validation", " ".join(args)),
}

# Helper functions to handle both ShtestFile objects and legacy dictionaries
def _add_to_list(obj, key, value):
    """Add value to a list, handling both ShtestFile and dict objects"""
    if hasattr(obj, key):
        # ShtestFile object
        getattr(obj, key).append(value)
    elif isinstance(obj, dict):
        # Legacy dict format
        if key not in obj:
            obj[key] = []
        obj[key].append(value)
    else:
        # Try to set as attribute
        if not hasattr(obj, key):
            setattr(obj, key, [])
        getattr(obj, key).append(value)

def _set_dict_value(obj, key, value):
    """Set a dictionary value, handling both ShtestFile and dict objects"""
    if hasattr(obj, key):
        # ShtestFile object
        current = getattr(obj, key)
        if isinstance(current, dict):
            current.update(value)
        else:
            setattr(obj, key, value)
    elif isinstance(obj, dict):
        # Legacy dict format
        if key not in obj:
            obj[key] = {}
        if isinstance(value, dict):
            obj[key].update(value)
        else:
            obj[key] = value
    else:
        # Try to set as attribute
        setattr(obj, key, value)

def _add_to_list_if_not_exists(obj, key, value):
    """Add value to list only if it doesn't exist"""
    if hasattr(obj, key):
        # ShtestFile object
        current_list = getattr(obj, key)
        if value not in current_list:
            current_list.append(value)
    elif isinstance(obj, dict):
        # Legacy dict format
        if key not in obj:
            obj[key] = []
        if value not in obj[key]:
            obj[key].append(value)
    else:
        # Try to set as attribute
        if not hasattr(obj, key):
            setattr(obj, key, [])
        current_list = getattr(obj, key)
        if value not in current_list:
            current_list.append(value)

def _set_variable(obj, name, value):
    """Set a variable, handling both ShtestFile and dict objects"""
    if hasattr(obj, 'set_variable'):
        # ShtestFile object
        obj.set_variable(name, value)
    elif hasattr(obj, 'variables'):
        # ShtestFile object with direct access
        obj.variables[name] = value
    elif isinstance(obj, dict):
        # Legacy dict format
        if 'variables' not in obj:
            obj['variables'] = {}
        obj['variables'][name] = value
    else:
        # Try to set as attribute
        if not hasattr(obj, 'variables'):
            setattr(obj, 'variables', {})
        obj.variables[name] = value

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
            # Handle both 'phrase' (main YAML) and 'pattern' (plugin YAML) keys
            pattern_text = entry.get("pattern") or entry.get("phrase")
            if not pattern_text:
                print(f"Warning: No pattern or phrase found in entry: {entry}")
                continue
                
            pattern = re.compile(pattern_text, re.IGNORECASE)
            handler = HANDLERS[entry["handler"]]
            rules.append((pattern, handler))
    return rules
