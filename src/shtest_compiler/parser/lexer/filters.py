"""
Filters for the configurable lexer.

This module provides different filter implementations that can be used
by the configurable lexer to process tokens.
"""

from typing import Iterator, List

from ...config.debug_config import debug_print, is_debug_enabled
from .core import Token


class Filter:
    """Base class for token filters."""

    def filter(self, tokens: List[Token], verbose: bool = False) -> Iterator[Token]:
        """
        Filter a list of tokens.

        Args:
            tokens: List of tokens to filter
            verbose: Whether to print detailed debug information

        Yields:
            Filtered tokens
        """
        raise NotImplementedError


class EmptyFilter(Filter):
    """Filter that removes empty tokens."""

    def filter(self, tokens: List[Token], verbose: bool = False) -> Iterator[Token]:
        """Remove empty tokens."""
        for token in tokens:
            if token.kind != "EMPTY":
                if verbose and is_debug_enabled():
                    debug_print(f"[DEBUG] Token: {token}")
                yield token


class WhitespaceFilter(Filter):
    """Filter that removes whitespace-only tokens."""

    def filter(self, tokens: List[Token], verbose: bool = False) -> Iterator[Token]:
        """Remove whitespace-only tokens."""
        for token in tokens:
            if token.value.strip():
                if verbose and is_debug_enabled():
                    debug_print(f"[DEBUG] Token: {token}")
                yield token


class CommentFilter(Filter):
    """Filter that removes comment tokens."""

    def filter(self, tokens: List[Token], verbose: bool = False) -> Iterator[Token]:
        """Remove comment tokens."""
        for token in tokens:
            if not token.value.startswith("#"):
                if verbose and is_debug_enabled():
                    debug_print(f"[DEBUG] Token: {token}")
                yield token


class DebugFilter(Filter):
    """Filter that adds debug information."""

    def filter(self, tokens: List[Token], verbose: bool = False) -> Iterator[Token]:
        """Add debug information to tokens."""
        for token in tokens:
            if verbose and is_debug_enabled():
                debug_print(f"[DEBUG] Processing token: {token}")
            yield token


class CompositeFilter(Filter):
    """Filter that combines multiple filters."""

    def __init__(self, filters: List[Filter]):
        """
        Initialize the composite filter.

        Args:
            filters: List of filters to apply in order
        """
        self.filters = filters

    def filter(self, tokens: List[Token], verbose: bool = False) -> Iterator[Token]:
        """Apply all filters in sequence."""
        current_tokens = list(tokens)

        for filter_obj in self.filters:
            current_tokens = list(filter_obj.filter(current_tokens, verbose))

        for token in current_tokens:
            yield token
