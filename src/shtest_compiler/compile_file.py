"""
Main compilation entry point using the modular compiler system.

This module provides the main interface for compiling .shtest files
using the enhanced modular parser and compiler system.
"""

import os
import sys
from pathlib import Path
from typing import Optional

from .command_loader import build_registry
from .compiler.compiler import ModularCompiler
from .utils.logger import debug_log, is_debug_enabled


def compile_file(
    input_path: str,
    output_path: Optional[str] = None,
    grammar: str = "default",
    ast_builder: str = "default",
    debug: bool = False,
    plugin_dir: Optional[str] = None,
    debug_output_path: Optional[str] = None,
) -> str:
    """
    Compile a .shtest file to a shell script using the modular compiler.

    Args:
        input_path: Path to the .shtest file
        output_path: Optional output path for the shell script
        grammar: Name of the grammar to use
        ast_builder: Name of the AST builder to use
        debug: Enable debug mode (deprecated, use global debug config)
        plugin_dir: Optional directory to load plugins from
        debug_output_path: Path to debug output file (optional)

    Returns:
        Path to the generated shell script
    """
    # Use global debug configuration
    debug_enabled = debug or is_debug_enabled()

    # Create compiler with specified configuration
    compiler = ModularCompiler(
        grammar_name=grammar,
        ast_builder_name=ast_builder,
        debug=debug_enabled,
        debug_output_path=debug_output_path,
    )

    # Compile the file
    return compiler.compile_file(
        input_path, output_path, debug_output_path=debug_output_path
    )


def compile_text(
    text: str,
    output_path: Optional[str] = None,
    grammar: str = "default",
    ast_builder: str = "default",
    debug: bool = False,
    debug_output_path: Optional[str] = None,
) -> str:
    """
    Compile .shtest text to a shell script using the modular compiler.

    Args:
        text: The .shtest content
        output_path: Optional output path for the shell script
        grammar: Name of the grammar to use
        ast_builder: Name of the AST builder to use
        debug: Enable debug mode (deprecated, use global debug config)
        debug_output_path: Path to debug output file (optional)

    Returns:
        Path to the generated shell script
    """
    # Use global debug configuration
    debug_enabled = debug or is_debug_enabled()

    # Create compiler with specified configuration
    compiler = ModularCompiler(
        grammar_name=grammar,
        ast_builder_name=ast_builder,
        debug=debug_enabled,
        debug_output_path=debug_output_path,
    )

    # Compile the text
    return compiler.compile_text(text, output_path, debug_output_path=debug_output_path)


def list_available_components():
    """List all available grammars, AST builders, and plugins."""
    compiler = ModularCompiler()

    print("Available Grammars:")
    for grammar in compiler.list_grammars():
        print(f"  - {grammar}")

    print("\nAvailable AST Builders:")
    for builder in compiler.list_ast_builders():
        print(f"  - {builder}")

    print("\nAvailable Plugins:")
    for plugin in build_registry.list():
        print(f"  - {plugin}")


def get_compiler_info(grammar: str = "default", ast_builder: str = "default") -> dict:
    """Get information about the compiler configuration."""
    compiler = ModularCompiler(grammar, ast_builder)
    return compiler.get_parser_info()


# Backward compatibility
def compile_shtest_file(
    input_path: str, output_path: Optional[str] = None, debug: bool = False
) -> str:
    """Backward compatibility function."""
    return compile_file(input_path, output_path, debug=debug)
