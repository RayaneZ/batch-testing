"""
Configurable parser that can use different lexers, grammars, and AST builders.
"""

import os
from typing import Optional

from ..utils.logger import debug_log, is_debug_enabled
from .ast_builder import DefaultASTBuilder
from .core import ParseError
from .grammar import DefaultGrammar
from .lexer import ConfigurableLexer
from .shtest_ast import ShtestFile


class ConfigurableParser:
    """A parser that can be configured with different components."""

    def __init__(
        self,
        lexer: Optional[ConfigurableLexer] = None,
        grammar: Optional[DefaultGrammar] = None,
        ast_builder: Optional[DefaultASTBuilder] = None,
        debug: bool = False,
    ):
        # Use global debug configuration
        self.debug = debug or is_debug_enabled()
        self.lexer = lexer or ConfigurableLexer(debug=self.debug)
        self.grammar = grammar or DefaultGrammar()
        self.ast_builder = ast_builder or DefaultASTBuilder()

    def parse(self, text: str, path: Optional[str] = None) -> ShtestFile:
        """Parse text into an AST."""
        try:
            if self.debug:
                debug_log(f"Parsing text with {len(text.splitlines())} lines")
            tokens = list(self.lexer.lex(text))
            if self.debug:
                debug_log(f"Got {len(tokens)} tokens")
            grammar_result = self.grammar.match(tokens)
            ast = self.ast_builder.build(grammar_result, path=path)
            return ast
        except Exception as e:
            from shtest_compiler.utils.logger import log_pipeline_error
            import traceback
            log_pipeline_error(f"[ERROR] Parser error: {e}\n{traceback.format_exc()}")
            raise ParseError(f"Parser error: {e}")

    def parse_file(self, file_path: str) -> ShtestFile:
        """Parse a file into an AST."""
        try:
            with open(file_path, encoding="utf-8") as f:
                text = f.read()
            return self.parse(text, path=file_path)
        except Exception as e:
            from shtest_compiler.utils.logger import log_pipeline_error
            import traceback
            log_pipeline_error(f"[ERROR] Parser error in file {file_path}: {e}\n{traceback.format_exc()}")
            raise ParseError(f"Parser error in file {file_path}: {e}")
