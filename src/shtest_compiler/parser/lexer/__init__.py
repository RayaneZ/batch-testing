"""
Modular lexer package for KnightBatch.

This package provides a configurable, extensible lexer architecture that supports:
- Configurable token patterns via YAML
- Pluggable token filters
- Extensible token types
- Debug and validation modes
"""

from .configurable_lexer import ConfigurableLexer
from .core import LexerError, Token, TokenType
from .filters import (
    CommentFilter,
    CompositeFilter,
    DebugFilter,
    EmptyFilter,
    Filter,
    WhitespaceFilter,
)
from .pattern_loader import PatternLoader

__all__ = [
    "ConfigurableLexer",
    "Token",
    "TokenType",
    "LexerError",
    "PatternLoader",
    "Filter",
    "EmptyFilter",
    "WhitespaceFilter",
    "CommentFilter",
    "DebugFilter",
    "CompositeFilter",
]
