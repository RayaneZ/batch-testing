"""
Enhanced compiler that integrates with the modular parser system.

This module provides a compiler that can work with different parser configurations,
grammars, and AST builders through the modular system.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from shtest_compiler.ast.visitor import ASTVisitor

from ..ast.shell_framework_ast import pretty_print_ast
from ..utils.logger import debug_log, is_debug_enabled, export_log
from ..core.context import CompileContext
from ..parser import ConfigurableParser, ast_builder_registry, grammar_registry
from ..parser.shtest_ast import ShtestFile
from .matcher_registry import MatcherRegistry
from .shell_generator import ShellGenerator


class ModularCompiler:
    """Enhanced compiler that uses the modular parser system."""

    def __init__(
        self,
        grammar_name: str = "default",
        ast_builder_name: str = "default",
        debug: bool = False,
        debug_output_path: str = None,
    ):
        """
        Initialize the modular compiler.

        Args:
            grammar_name: Name of the grammar to use (from grammar_registry)
            ast_builder_name: Name of the AST builder to use (from ast_builder_registry)
            debug: Enable debug mode (deprecated, use global debug config)
            debug_output_path: Path to debug output file (optional)
        """
        # Use global debug configuration
        self.debug = debug or is_debug_enabled()
        self.grammar_name = grammar_name
        self.ast_builder_name = ast_builder_name
        self.debug_output_path = debug_output_path

        # Create parser with specified components
        self.parser = ConfigurableParser(
            grammar=grammar_registry.create(grammar_name),
            ast_builder=ast_builder_registry.create(ast_builder_name),
            debug=self.debug,
        )

        # Initialize other components
        self.shell_generator = ShellGenerator(debug_output_path=debug_output_path)
        self.matcher_registry = MatcherRegistry()
        self.context = CompileContext()

        # Add registries for plugin integration
        self.grammar_registry = grammar_registry
        self.ast_builder_registry = ast_builder_registry

    def compile_file(
        self,
        file_path: str,
        output_path: Optional[str] = None,
        debug_output_path: str = None,
        debug_ast: bool = False,
    ) -> str:
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            # Parse the file
            ast = self.parser.parse_file(file_path)
            if debug_ast:
                pretty_print_ast(ast)
            # Set debug_output_path to match test name if not provided
            if debug_output_path is None:
                base = os.path.splitext(os.path.basename(file_path))[0]
                dir_path = os.path.dirname(os.path.abspath(file_path))
                debug_output_path = os.path.join(dir_path, base + ".txt")
            # Generate shell script
            shell_script = self._generate_shell_script(
                ast, debug_output_path=debug_output_path
            )
            # Write output
            if output_path is None:
                output_path = self._get_default_output_path(file_path)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(shell_script)
            if self.debug:
                debug_log(f"Compiled {file_path} -> {output_path}")
            # Export debug log if enabled
            if self.debug and debug_output_path:
                export_log(debug_output_path)
            return output_path
        except Exception as e:
            import traceback
            from shtest_compiler.utils.logger import log_pipeline_error
            error_msg = f"[ERROR] {type(e).__name__}: {e}"
            stack = traceback.format_exc()
            log_pipeline_error(error_msg + "\n" + stack)
            debug_log(error_msg)
            debug_log(stack)
            print(error_msg)
            if debug_output_path:
                export_log(debug_output_path)
            # Optionally, write a fallback shell script
            if output_path:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(f'echo "{error_msg}"\nexit 1')
            raise

    def compile_text(
        self,
        text: str,
        output_path: Optional[str] = None,
        debug_output_path: str = None,
        debug_ast: bool = False,
    ) -> str:
        """
        Compile .shtest text to a shell script.

        Args:
            text: The .shtest content
            output_path: Optional output path for the shell script
            debug_output_path: Path to debug output file (optional)

        Returns:
            Path to the generated shell script
        """
        # Parse the text
        ast = self.parser.parse(text)
        if debug_ast:
            pretty_print_ast(ast)

        # Generate shell script
        shell_script = self._generate_shell_script(
            ast, debug_output_path=debug_output_path
        )

        # Write output
        if output_path is None:
            output_path = "output.sh"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(shell_script)

        if self.debug:
            debug_log(f"Compiled text -> {output_path}")

        return output_path

    def _generate_shell_script(
        self, ast: ShtestFile, debug_output_path: str = None
    ) -> str:
        """Generate shell script from AST."""
        # Reset context for new compilation
        self.context.reset()
        # Visit the AST to generate shell code
        visitor = ShellGenerator(
            debug_output_path=debug_output_path or self.debug_output_path
        )
        visitor.context = self.context
        visitor.matcher_registry = self.matcher_registry
        return visitor.visit(ast)

    def _get_default_output_path(self, input_path: str) -> str:
        """Get default output path for input file."""
        input_path = Path(input_path)
        return str(input_path.with_suffix(".sh"))

    def set_grammar(self, grammar_name: str) -> None:
        """Change the grammar used by the parser."""
        if grammar_name not in grammar_registry.list():
            raise ValueError(f"Grammar '{grammar_name}' not found")

        self.grammar_name = grammar_name
        self.parser.grammar = grammar_registry.create(grammar_name)

    def set_ast_builder(self, ast_builder_name: str) -> None:
        """Change the AST builder used by the parser."""
        if ast_builder_name not in ast_builder_registry.list():
            raise ValueError(f"AST builder '{ast_builder_name}' not found")

        self.ast_builder_name = ast_builder_name
        self.parser.ast_builder = ast_builder_registry.create(ast_builder_name)

    def add_matcher(self, matcher) -> None:
        """Add a custom matcher to the registry."""
        self.matcher_registry.register(matcher)

    def list_grammars(self) -> list:
        """List available grammars."""
        return grammar_registry.list()

    def list_ast_builders(self) -> list:
        """List available AST builders."""
        return ast_builder_registry.list()

    def get_parser_info(self) -> Dict[str, Any]:
        """Get information about the current parser configuration."""
        return {
            "grammar": self.grammar_name,
            "ast_builder": self.ast_builder_name,
            "debug": self.debug,
            "available_grammars": self.list_grammars(),
            "available_ast_builders": self.list_ast_builders(),
        }


# Legacy Compiler class removed - use ModularCompiler directly
