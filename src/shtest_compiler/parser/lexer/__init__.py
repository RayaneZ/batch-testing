"""
Modular lexer package for KnightBatch.

This package provides a configurable, extensible lexer architecture that supports:
- Configurable token patterns via YAML
- Pluggable token filters
- Extensible token types
- Debug and validation modes
"""

from .configurable_lexer import ConfigurableLexer
from .core import Token, TokenType, LexerError
from .pattern_loader import PatternLoader
from .filters import (
    Filter,
    EmptyFilter,
    WhitespaceFilter,
    CommentFilter,
    DebugFilter,
    CompositeFilter,
)

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
