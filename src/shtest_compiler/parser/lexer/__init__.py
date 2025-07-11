"""
Modular lexer package for KnightBatch.

This package provides a configurable, extensible lexer architecture that supports:
- Configurable token patterns via YAML
- Pluggable token filters
- Extensible token types
- Debug and validation modes
"""

from .core import Token, TokenType, LexerError
from .configurable_lexer import ConfigurableLexer, lex, lex_file
from .pattern_loader import PatternLoader
from .filters import TokenFilter, CommentFilter, EmptyLineFilter, DebugFilter, CompositeFilter
from .tokenizers import RegexTokenizer, DefaultTokenizer, FlexibleTokenizer

__all__ = [
    'Token',
    'TokenType', 
    'LexerError',
    'ConfigurableLexer',
    'PatternLoader',
    'TokenFilter',
    'CommentFilter',
    'EmptyLineFilter',
    'DebugFilter',
    'CompositeFilter',
    'RegexTokenizer',
    'DefaultTokenizer',
    'FlexibleTokenizer',
    'lex',
    'lex_file',
] 