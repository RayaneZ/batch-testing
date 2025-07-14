"""
Core lexer components for KnightBatch.

This module defines the fundamental data structures and types used by the lexer.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, Optional


class TokenType(Enum):
    """Enumeration of all possible token types."""

    STEP = auto()
    ACTION_ONLY = auto()
    ACTION_RESULT = auto()
    RESULT_ONLY = auto()
    COMMENT = auto()
    TEXT = auto()
    EMPTY = auto()
    ERROR = auto()


@dataclass
class Token:
    """Represents a lexical token with metadata."""

    type: TokenType
    value: str
    lineno: int
    column: int = 0
    result: Optional[str] = None
    original: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate token after initialization."""
        if not isinstance(self.type, TokenType):
            raise ValueError(f"Invalid token type: {self.type}")
        if self.lineno < 1:
            raise ValueError(f"Line number must be >= 1, got {self.lineno}")
        if self.column is not None and self.column < 0:
            raise ValueError(f"Column must be >= 0, got {self.column}")

    @property
    def kind(self) -> str:
        """Backward compatibility: return token type name."""
        return self.type.name

    def __str__(self) -> str:
        """String representation of the token."""
        result_part = f" -> '{self.result}'" if self.result else ""
        return (
            f"{self.type.name}@{self.lineno}:{self.column} '{self.value}'{result_part}"
        )

    def __repr__(self) -> str:
        """Detailed representation of the token."""
        return (
            f"Token(type={self.type.name}, value='{self.value}', "
            f"lineno={self.lineno}, column={self.column}, "
            f"result={repr(self.result)}, metadata={self.metadata})"
        )


class LexerError(Exception):
    """Exception raised when lexer encounters an error."""

    def __init__(
        self, message: str, lineno: int, column: int = 0, line: Optional[str] = None
    ):
        self.message = message
        self.lineno = lineno
        self.column = column
        self.line = line
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format the error message with line information."""
        msg = f"Lexer error at line {self.lineno}"
        if self.column > 0:
            msg += f", column {self.column}"
        msg += f": {self.message}"

        if self.line:
            msg += f"\nLine: {self.line}"
            if self.column > 0:
                msg += f"\n{' ' * (self.column - 1)}^"

        return msg
