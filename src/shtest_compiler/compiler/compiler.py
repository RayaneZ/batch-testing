"""
Enhanced compiler that integrates with the modular parser system.

This module provides a compiler that can work with different parser configurations,
grammars, and AST builders through the modular system.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path

from ..parser import ConfigurableParser, grammar_registry, ast_builder_registry
from ..parser.shtest_ast import ShtestFile
from ..core.visitor import ASTVisitor
from ..core.context import CompileContext
from .shell_generator import ShellGenerator
from .matcher_registry import MatcherRegistry
from ..config.debug_config import is_debug_enabled, debug_print


class ModularCompiler:
    """Enhanced compiler that uses the modular parser system."""
    
    def __init__(self, 
                 grammar_name: str = "default",
                 ast_builder_name: str = "default",
                 debug: bool = False):
        """
        Initialize the modular compiler.
        
        Args:
            grammar_name: Name of the grammar to use (from grammar_registry)
            ast_builder_name: Name of the AST builder to use (from ast_builder_registry)
            debug: Enable debug mode (deprecated, use global debug config)
        """
        # Use global debug configuration
        self.debug = debug or is_debug_enabled()
        self.grammar_name = grammar_name
        self.ast_builder_name = ast_builder_name
        
        # Create parser with specified components
        self.parser = ConfigurableParser(
            grammar=grammar_registry.create(grammar_name),
            ast_builder=ast_builder_registry.create(ast_builder_name),
            debug=self.debug
        )
        
        # Initialize other components
        self.shell_generator = ShellGenerator()
        self.matcher_registry = MatcherRegistry()
        self.context = CompileContext()
        
        # Add registries for plugin integration
        self.grammar_registry = grammar_registry
        self.ast_builder_registry = ast_builder_registry
    
    def compile_file(self, file_path: str, output_path: Optional[str] = None) -> str:
        """
        Compile a .shtest file to a shell script.
        
        Args:
            file_path: Path to the .shtest file
            output_path: Optional output path for the shell script
            
        Returns:
            Path to the generated shell script
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Parse the file
        ast = self.parser.parse_file(file_path)
        
        # Generate shell script
        shell_script = self._generate_shell_script(ast)
        
        # Write output
        if output_path is None:
            output_path = self._get_default_output_path(file_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(shell_script)
        
        if self.debug:
            debug_print(f"Compiled {file_path} -> {output_path}")
        
        return output_path
    
    def compile_text(self, text: str, output_path: Optional[str] = None) -> str:
        """
        Compile .shtest text to a shell script.
        
        Args:
            text: The .shtest content
            output_path: Optional output path for the shell script
            
        Returns:
            Path to the generated shell script
        """
        # Parse the text
        ast = self.parser.parse(text)
        
        # Generate shell script
        shell_script = self._generate_shell_script(ast)
        
        # Write output
        if output_path is None:
            output_path = "output.sh"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(shell_script)
        
        if self.debug:
            debug_print(f"Compiled text -> {output_path}")
        
        return output_path
    
    def _generate_shell_script(self, ast: ShtestFile) -> str:
        """Generate shell script from AST."""
        # Reset context for new compilation
        self.context.reset()
        
        # Visit the AST to generate shell code
        visitor = ShellGenerator()
        visitor.context = self.context
        visitor.matcher_registry = self.matcher_registry
        
        return visitor.visit(ast)
    
    def _get_default_output_path(self, input_path: str) -> str:
        """Get default output path for input file."""
        input_path = Path(input_path)
        return str(input_path.with_suffix('.sh'))
    
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
            "available_ast_builders": self.list_ast_builders()
        }


# Backward compatibility: keep the old compiler interface
class Compiler(ModularCompiler):
    """Backward compatibility wrapper for the old compiler interface."""
    
    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)
    
    def compile(self, file_path: str, output_path: Optional[str] = None) -> str:
        """Backward compatibility method."""
        return self.compile_file(file_path, output_path)