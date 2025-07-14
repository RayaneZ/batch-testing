"""
Core types and interfaces for the modular parser.
"""

from typing import Any, List, Optional, Protocol, runtime_checkable


class ParseError(Exception):
    """Exception raised for parser errors."""

    def __init__(
        self, message: str, lineno: Optional[int] = None, column: Optional[int] = None
    ):
        self.message = message
        self.lineno = lineno
        self.column = column
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        msg = self.message
        if self.lineno is not None:
            msg = f"Line {self.lineno}: {msg}"
        if self.column is not None:
            msg += f" (col {self.column})"
        return msg


class TokenLike(Protocol):
    """Protocol for token-like objects."""

    kind: str
    value: str
    lineno: int
    result: Any
    original: Any


@runtime_checkable
class ASTBuilder(Protocol):
    """Protocol for AST builder."""

    def build(self, tokens: List[TokenLike], debug: bool = False) -> Any: ...


@runtime_checkable
class Grammar(Protocol):
    """Protocol for grammar/rule set."""

    def match(self, tokens: List[TokenLike], debug: bool = False) -> Any: ...
