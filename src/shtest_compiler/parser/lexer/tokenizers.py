"""
Tokenizers for the configurable lexer.

This module provides different tokenizer implementations that can be used
by the configurable lexer.
"""

import re
from typing import Any, Dict, Iterator, List

from ...utils.logger import debug_log, is_debug_enabled
from .core import Token, TokenType


class Tokenizer:
    """Base class for tokenizers."""

    def tokenize(self, text: str) -> Iterator[Token]:
        """Tokenize text into tokens."""
        raise NotImplementedError


def _token_type_from_str(type_str: str) -> TokenType:
    try:
        return TokenType[type_str.upper()]
    except Exception:
        return TokenType.TEXT


class RegexTokenizer(Tokenizer):
    """Tokenizer that uses regex patterns."""

    def __init__(self, pattern, token_type: str, debug: bool = False):
        """
        Initialize the regex tokenizer.

        Args:
            pattern: Regex pattern to match (string or compiled pattern)
            token_type: Type of token to create (string, e.g. 'ACTION_ONLY')
            debug: Enable debug output for this tokenizer
        """
        import re

        if isinstance(pattern, str):
            self.pattern = re.compile(pattern, re.IGNORECASE)
        else:
            self.pattern = pattern  # already compiled
        self.token_type = _token_type_from_str(token_type)
        self.debug = debug

    def tokenize(self, text: str) -> Iterator[Token]:
        """Tokenize text using regex patterns."""
        lines = text.split("\n")

        for lineno, line in enumerate(lines, 1):
            stripped = line.strip()

            # Skip empty lines
            if not stripped:
                if self.debug or is_debug_enabled():
                    debug_log(
                        f"RegexTokenizer.tokenize: Yielding EMPTY token at line {lineno}"
                    )
                yield Token(
                    type=TokenType.EMPTY, value="", lineno=lineno, original=line
                )
                continue

            # Try to match the pattern
            match = self.pattern.match(stripped)
            if match:
                token = Token(
                    type=self.token_type,
                    value=match.group(1) if match.groups() else stripped,
                    result=match.groups() if match.groups() else None,
                    lineno=lineno,
                    original=line,
                )
                if self.debug or is_debug_enabled():
                    debug_log(
                        f"RegexTokenizer.tokenize: Yielding token type={token.type}, value={token.value}, result={getattr(token, 'result', None)}, original={getattr(token, 'original', None)} at line {lineno}"
                    )
                yield token
            else:
                # No match, yield as TEXT token
                token = Token(
                    type=TokenType.TEXT, value=stripped, lineno=lineno, original=line
                )
                if self.debug or is_debug_enabled():
                    debug_log(
                        f"RegexTokenizer.tokenize: Yielding TEXT token value={stripped} at line {lineno}"
                    )
                yield token


class FallbackTokenizer(Tokenizer):
    """Fallback tokenizer for unrecognized text."""

    def tokenize(self, text: str) -> Iterator[Token]:
        """Tokenize text as TEXT tokens."""
        lines = text.split("\n")

        for lineno, line in enumerate(lines, 1):
            stripped = line.strip()

            if stripped:
                token = Token(
                    type=TokenType.TEXT, value=stripped, lineno=lineno, original=line
                )
                yield token


class PatternTokenizer(Tokenizer):
    """Tokenizer that uses a dictionary of patterns."""

    def __init__(self, patterns: Dict[str, str]):
        """
        Initialize the pattern tokenizer.

        Args:
            patterns: Dictionary mapping token types to regex patterns
        """
        self.patterns = {}
        for token_type, pattern in patterns.items():
            self.patterns[token_type] = re.compile(pattern, re.IGNORECASE)

    def tokenize(self, text: str) -> Iterator[Token]:
        """Tokenize text using multiple patterns."""
        lines = text.split("\n")

        for lineno, line in enumerate(lines, 1):
            stripped = line.strip()

            if not stripped:
                yield Token(
                    type=TokenType.EMPTY, value="", lineno=lineno, original=line
                )
                continue

            # Try each pattern
            matched = False
            for token_type, pattern in self.patterns.items():
                match = pattern.match(stripped)
                if match:
                    token = Token(
                        type=_token_type_from_str(token_type),
                        value=match.group(1) if match.groups() else stripped,
                        result=match.groups() if match.groups() else None,
                        lineno=lineno,
                        original=line,
                    )
                    yield token
                    matched = True
                    break

            if not matched:
                # No pattern matched, yield as TEXT
                token = Token(
                    type=TokenType.TEXT, value=stripped, lineno=lineno, original=line
                )
                yield token
