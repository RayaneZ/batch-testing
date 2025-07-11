"""
Configurable parser that can use different lexers, grammars, and AST builders.
"""

import os
from typing import Optional
from .core import ParseError
from .shtest_ast import ShtestFile
from .lexer import ConfigurableLexer
from .grammar import DefaultGrammar
from .ast_builder import DefaultASTBuilder


class ConfigurableParser:
    """A parser that can be configured with different components."""
    
    def __init__(self, 
                 lexer: Optional[ConfigurableLexer] = None,
                 grammar: Optional[DefaultGrammar] = None,
                 ast_builder: Optional[DefaultASTBuilder] = None,
                 debug: bool = False):
        self.lexer = lexer or ConfigurableLexer(debug=debug)
        self.grammar = grammar or DefaultGrammar()
        self.ast_builder = ast_builder or DefaultASTBuilder()
        self.debug = debug
    
    def parse(self, text: str, path: Optional[str] = None) -> ShtestFile:
        """Parse text into an AST."""
        try:
            if self.debug:
                print(f"[DEBUG] Parsing text with {len(text.splitlines())} lines")
            tokens = list(self.lexer.lex(text))
            if self.debug:
                print(f"[DEBUG] Got {len(tokens)} tokens")
            grammar_result = self.grammar.match(tokens)
            ast = self.ast_builder.build(grammar_result, path=path)
            return ast
        except Exception as e:
            raise ParseError(f"Parser error: {e}")
    
    def parse_file(self, file_path: str) -> ShtestFile:
        """Parse a file into an AST."""
        try:
            with open(file_path, encoding="utf-8") as f:
                text = f.read()
            return self.parse(text, path=file_path)
        except Exception as e:
            raise ParseError(f"Parser error in file {file_path}: {e}") 