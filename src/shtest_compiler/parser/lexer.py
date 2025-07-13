"""
Backward compatibility layer for the old lexer interface.

This module provides the old lexer interface while using the new modular lexer
under the hood for better maintainability and extensibility.
"""

from typing import Iterator, Optional
from dataclasses import dataclass

# Import the new modular lexer
from .lexer import Token as NewToken, TokenType, lex as new_lex, lex_file as new_lex_file


# Backward compatibility Token class
@dataclass
class Token:
    kind: str                    # Type de jeton (STEP, ACTION_ONLY, etc.)
    value: str                   # Contenu principal du jeton
    lineno: int                  # Numéro de ligne dans le fichier source
    result: Optional[str] = None  # Résultat attendu (si applicable)
    original: Optional[str] = None  # Ligne originale complète
    
    @classmethod
    def from_new_token(cls, new_token: NewToken) -> 'Token':
        """Convert new token to old token format."""
        return cls(
            kind=new_token.kind,
            value=new_token.value,
            lineno=new_token.lineno,
            result=new_token.result,
            original=new_token.original
        )


def _convert_tokens(tokens: Iterator[NewToken]) -> Iterator[Token]:
    """Convert new tokens to old token format."""
    for token in tokens:
        yield Token.from_new_token(token)


def lex(text: str, debug: bool = False) -> Iterator[Token]:
    """Tokenize the contents of a `.shtest` file."""
    new_tokens = new_lex(text, debug=debug)
    yield from _convert_tokens(new_tokens)


def lex_file(path: str) -> Iterator[Token]:
    """Read *path* and yield :class:`Token` objects."""
    new_tokens = new_lex_file(path, debug=True)
    for token in _convert_tokens(new_tokens):
        print(f"[DEBUG] Lexer: Produced token kind={token.kind}, value={token.value}, result={token.result}, original={token.original}")
        yield token

print("LEXER DEBUG ACTIVE: src/shtest_compiler/parser/lexer.py loaded")
