"""
Plugin system for extending the shtest compiler.

This module provides a flexible plugin system that allows users to:
- Add custom grammars
- Add custom AST builders
- Add custom matchers
- Add custom validators and transformers
- Add custom output formats
"""

import os
import sys
import importlib
import importlib.util
from typing import Dict, List, Any, Optional, Type
from pathlib import Path

from ..parser import Grammar, ASTBuilder
from ..compiler.matcher_registry import MatcherRegistry


class Plugin:
    """Base class for all plugins."""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
    
    def install(self, registry) -> None:
        """Install the plugin into the registry."""
        raise NotImplementedError("Subclasses must implement install()")
    
    def uninstall(self, registry) -> None:
        """Uninstall the plugin from the registry."""
        raise NotImplementedError("Subclasses must implement uninstall()")


class GrammarPlugin(Plugin):
    """Plugin for adding custom grammars."""
    
    def __init__(self, name: str, grammar_class: Type[Grammar], version: str = "1.0.0"):
        super().__init__(name, version)
        self.grammar_class = grammar_class
    
    def install(self, registry) -> None:
        """Install the grammar into the grammar registry."""
        registry.grammar_registry.register(self.name, self.grammar_class)
    
    def uninstall(self, registry) -> None:
        """Uninstall the grammar from the grammar registry."""
        # Note: This would need to be implemented in the registry
        pass


class ASTBuilderPlugin(Plugin):
    """Plugin for adding custom AST builders."""
    
    def __init__(self, name: str, builder_class: Type[ASTBuilder], version: str = "1.0.0"):
        super().__init__(name, version)
        self.builder_class = builder_class
    
    def install(self, registry) -> None:
        """Install the AST builder into the AST builder registry."""
        registry.ast_builder_registry.register(self.name, self.builder_class)
    
    def uninstall(self, registry) -> None:
        """Uninstall the AST builder from the AST builder registry."""
        # Note: This would need to be implemented in the registry
        pass


class MatcherPlugin(Plugin):
    """Plugin for adding custom matchers."""
    
    def __init__(self, name: str, matcher_instance, version: str = "1.0.0"):
        super().__init__(name, version)
        self.matcher_instance = matcher_instance
    
    def install(self, registry) -> None:
        """Install the matcher into the matcher registry."""
        registry.matcher_registry.register(self.matcher_instance)
    
    def uninstall(self, registry) -> None:
        """Uninstall the matcher from the matcher registry."""
        # Note: This would need to be implemented in the registry
        pass


class PluginRegistry:
    """Registry for managing plugins."""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.loaded_modules: Dict[str, Any] = {}
    
    def register(self, plugin: Plugin) -> None:
        """Register a plugin."""
        self.plugins[plugin.name] = plugin
    
    def unregister(self, name: str) -> None:
        """Unregister a plugin."""
        if name in self.plugins:
            del self.plugins[name]
    
    def install(self, name: str, registry) -> None:
        """Install a plugin."""
        if name not in self.plugins:
            raise KeyError(f"Plugin '{name}' not found")
        
        plugin = self.plugins[name]
        plugin.install(registry)
    
    def uninstall(self, name: str, registry) -> None:
        """Uninstall a plugin."""
        if name not in self.plugins:
            raise KeyError(f"Plugin '{name}' not found")
        
        plugin = self.plugins[name]
        plugin.uninstall(registry)
    
    def list(self) -> List[str]:
        """List all registered plugins."""
        return list(self.plugins.keys())
    
    def get(self, name: str) -> Optional[Plugin]:
        """Get a plugin by name."""
        return self.plugins.get(name)
    
    def load_from_file(self, file_path: str) -> Plugin:
        """Load a plugin from a Python file."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Plugin file not found: {file_path}")
        
        # Load the module
        spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Look for plugin classes
        plugin = None
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, Plugin) and attr != Plugin:
                plugin = attr()
                break
        
        if plugin is None:
            raise ValueError(f"No plugin class found in {file_path}")
        
        # Register the plugin
        self.register(plugin)
        self.loaded_modules[plugin.name] = module
        
        return plugin
    
    def load_from_directory(self, directory: str) -> List[Plugin]:
        """Load all plugins from a directory."""
        directory = Path(directory)
        plugins = []
        
        if not directory.exists():
            raise FileNotFoundError(f"Plugin directory not found: {directory}")
        
        for file_path in directory.glob("*.py"):
            if file_path.name.startswith("__"):
                continue
            
            try:
                plugin = self.load_from_file(str(file_path))
                plugins.append(plugin)
            except Exception as e:
                print(f"Failed to load plugin from {file_path}: {e}")
        
        return plugins


# Global plugin registry
plugin_registry = PluginRegistry()


def load_plugin(file_path: str) -> Plugin:
    """Load a plugin from a file."""
    return plugin_registry.load_from_file(file_path)


def load_plugins_from_directory(directory: str) -> List[Plugin]:
    """Load all plugins from a directory."""
    return plugin_registry.load_from_directory(directory)


def install_plugin(name: str, registry) -> None:
    """Install a plugin by name."""
    plugin_registry.install(name, registry)


def list_plugins() -> List[str]:
    """List all registered plugins."""
    return plugin_registry.list()


# Example plugin classes for common use cases
class CustomGrammarPlugin(GrammarPlugin):
    """Example plugin for adding a custom grammar."""
    
    def __init__(self, name: str, grammar_class: Type[Grammar], version: str = "1.0.0"):
        super().__init__(name, grammar_class, version)


class CustomASTBuilderPlugin(ASTBuilderPlugin):
    """Example plugin for adding a custom AST builder."""
    
    def __init__(self, name: str, builder_class: Type[ASTBuilder], version: str = "1.0.0"):
        super().__init__(name, builder_class, version)


class CustomMatcherPlugin(MatcherPlugin):
    """Example plugin for adding a custom matcher."""
    
    def __init__(self, name: str, matcher_instance, version: str = "1.0.0"):
        super().__init__(name, matcher_instance, version) 