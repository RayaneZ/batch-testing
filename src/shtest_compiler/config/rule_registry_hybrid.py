import re
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "patterns_hybrid.yml"
print("🔁 Loading YAML from", CONFIG_PATH)
with open(CONFIG_PATH, encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

HANDLERS = {
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

def _handle_sql_script_text(text, actions):
    import re
    scripts = re.findall(r"\S+\.sql", text, re.I)
    for path in scripts:
        if path not in actions["sql_scripts"]:
            actions["sql_scripts"].append(path)

def load_rules():
    rules = []
    for section, entries in CONFIG["patterns"].items():
        for entry in entries:
            pattern = re.compile(entry["pattern"], re.IGNORECASE)
            handler = HANDLERS[entry["handler"]]
            rules.append((pattern, handler))
    return rules
