"""
Backward compatibility layer for the old parser interface.

This module provides the old parser interface while using the new modular parser
under the hood for better maintainability and extensibility.
"""

import re
from typing import List
from .shtest_ast import ShtestFile, Action
from shtest_compiler.config.rule_registry_hybrid import load_rules
from .configurable_parser import ConfigurableParser

class Parser:
    """Backward compatibility parser that uses the new modular parser."""
    
    def __init__(self) -> None:
        self.rules: List = load_rules()
        self.arg_pattern = re.compile(r"(?:argument|paramètre|et\s+(?:l['ae]|l'))\s*(\S+)=\s*(\S+)", re.I)
        # Use the new modular parser
        self._modular_parser = ConfigurableParser(debug=False)

    def parse(self, description: str, path: str = None, debug: bool = False) -> ShtestFile:
        # Use the new modular parser for the main parsing
        shtest = self._modular_parser.parse(description, path=path)
        
        # Apply legacy rule matching and argument extraction
        self._apply_legacy_rules(shtest, description, debug)
        
        return shtest
    
    def _apply_legacy_rules(self, shtest: ShtestFile, description: str, debug: bool = False) -> None:
        """Apply legacy rule matching and argument extraction."""
        # Get tokens for rule matching
        tokens = list(self._modular_parser.lexer.lex(description))
        
        for token in tokens:
            # Apply legacy rule matching
            for rule in self.rules:
                pattern, handler = rule
                match = pattern.search(token.original or token.value)
                if match:
                    if debug:
                        print(f"DEBUG: Calling handler {handler.__name__ if hasattr(handler, '__name__') else str(handler)} with {len(match.groups())} groups: {match.groups()}")
                    try:
                        handler(shtest, *match.groups())
                        self._handle_arguments(match, shtest)
                    except Exception as e:
                        if debug:
                            print(f"DEBUG: Error in handler: {e}")
                        raise
            
            # Extract inline arguments from actions
            if token.kind in ["ACTION_RESULT", "ACTION_ONLY"] and token.value:
                # Find the corresponding action in the AST
                for step in shtest.steps:
                    for action in step.actions:
                        if action.raw_line == token.original:
                            self._extract_inline_arguments(token.value, action)

    def _handle_arguments(self, match: re.Match, shtest: ShtestFile) -> None:
        """Handle legacy argument extraction."""
        # Initialize arguments dict if it doesn't exist
        if not hasattr(shtest, 'arguments'):
            shtest.arguments = {}
        
        for m in self.arg_pattern.finditer(match.string):
            shtest.arguments[m[1].strip()] = m[2].strip()

    def _extract_inline_arguments(self, command: str, action: Action) -> None:
        """Extract inline arguments from command strings."""
        for m in self.arg_pattern.finditer(command):
            if not hasattr(action, "arguments"):
                action.arguments = {}
            action.arguments[m[1].strip()] = m[2].strip()
