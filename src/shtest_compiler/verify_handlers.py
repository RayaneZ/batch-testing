import importlib
import os
from shtest_compiler.command_loader import PatternRegistry

# Mapping logique handler -> plugin
PLUGIN_MAP = {
    "file": [
        "create_file", "update_file", "delete_file", "copy_file", "move_file",
        "cat_file", "exists", "touch_ts", "compare_files"
    ],
    "dir": [
        "create_dir", "delete_dir", "copy_dir", "move_dir", "purge_dir"
    ],
    "script": [
        "run_script", "run_with_args"
    ],
    "sql": [
        "run_sql_script"
    ],
    "stdout": [
        "stdout_contains"
    ],
    # Ajoute ici d'autres plugins si besoin
}

def get_plugin_handlers(plugin_name):
    try:
        mod = importlib.import_module(f"shtest_compiler.plugins.{plugin_name}.{plugin_name}")
        return getattr(mod, "PLUGIN_HANDLERS", {})
    except Exception as e:
        print(f"Erreur chargement plugin {plugin_name}: {e}")
        return {}

def main():
    actions_yml = os.path.join(os.path.dirname(__file__), "config/patterns_actions.yml")
    validations_yml = os.path.join(os.path.dirname(__file__), "config/patterns_validations.yml")
    registry = PatternRegistry(actions_yml, validations_yml)

    # 1. Handlers YAML
    yaml_handlers = set()
    for entry in registry.actions["canonicals"].values():
        yaml_handlers.add(entry["handler"])
    for entry in registry.validations["canonicals"].values():
        yaml_handlers.add(entry["handler"])

    # 2. Handlers Python (par plugin)
    plugin_handlers = {}
    for plugin, handlers in PLUGIN_MAP.items():
        plugin_dict = get_plugin_handlers(plugin)
        for h in handlers:
            plugin_handlers[h] = plugin

    # 3. Vérification
    print("=== Vérification correspondance YAML <-> Plugins ===")
    missing = []
    for handler in sorted(yaml_handlers):
        if handler not in plugin_handlers:
            print(f"[ABSENT] Handler '{handler}' n'est pas défini dans un plugin.")
            missing.append(handler)
        else:
            print(f"[OK] Handler '{handler}' trouvé dans plugin '{plugin_handlers[handler]}'.")

    # 4. Handlers Python non utilisés dans le YAML
    extra = []
    for handler, plugin in plugin_handlers.items():
        if handler not in yaml_handlers:
            print(f"[INUTILISÉ] Handler '{handler}' du plugin '{plugin}' n'est pas référencé dans le YAML.")
            extra.append(handler)

    print(f"\nRésumé : {len(missing)} manquants, {len(extra)} non utilisés.")

if __name__ == "__main__":
    main() 