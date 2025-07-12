import importlib
import os

plugin_registry = {}

def load_plugins_from_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"shtest_compiler.plugins.{filename[:-3]}"
            module = importlib.import_module(module_name)
            plugin_registry[module_name] = module
    return plugin_registry 