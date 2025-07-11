"""
Tokenizers for the modular lexer.

This module provides different tokenizer implementations that can be used
with the configurable lexer.
"""

from abc import ABC, abstractmethod
from typing import Iterator, Dict, Optional
import re
from .core import Token, TokenType, LexerError


class Tokenizer(ABC):
    """Base class for tokenizers."""
    
    @abstractmethod
    def tokenize(self, text: str) -> Iterator[Token]:
        """Tokenize text into tokens.
        
        Args:
            text: Input text to tokenize.
            
        Yields:
            Tokens from the input text.
        """
        pass


class RegexTokenizer(Tokenizer):
    """Tokenizer that uses regex patterns for tokenization."""
    
    def __init__(self, patterns: Dict[str, re.Pattern]):
        """Initialize the regex tokenizer.
        
        Args:
            patterns: Dictionary mapping token type names to compiled regex patterns.
        """
        self.patterns = patterns
        self.token_type_map = {
            'step': TokenType.STEP,
            'action_result': TokenType.ACTION_RESULT,
            'action_only': TokenType.ACTION_ONLY,
            'result_only': TokenType.RESULT_ONLY,
            'comment': TokenType.COMMENT,
        }
    
    def tokenize(self, text: str) -> Iterator[Token]:
        """Tokenize text using regex patterns.
        
        Args:
            text: Input text to tokenize.
            
        Yields:
            Tokens from the input text.
        """
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            
            # Handle empty lines
            if not stripped:
                yield Token(
                    type=TokenType.EMPTY,
                    value="",
                    lineno=lineno,
                    original=line
                )
                continue
            
            # Try to match patterns in order
            token = self._match_patterns(stripped, lineno, line)
            if token:
                yield token
            else:
                # No pattern matched, treat as text
                yield Token(
                    type=TokenType.TEXT,
                    value=stripped,
                    lineno=lineno,
                    original=line
                )
    
    def _match_patterns(self, line: str, lineno: int, original: str) -> Optional[Token]:
        """Try to match line against all patterns.
        
        Args:
            line: Line to match.
            lineno: Line number.
            original: Original line content.
            
        Returns:
            Token if pattern matched, None otherwise.
        """
        # Define pattern priority order
        priority_patterns = [
            'comment',
            'step', 
            'action_result',
            'action_only',
            'result_only'
        ]
        
        for pattern_name in priority_patterns:
            pattern = self.patterns.get(pattern_name)
            if pattern:
                match = pattern.match(line)
                if match:
                    return self._create_token(pattern_name, match, lineno, original)
        
        return None
    
    def _create_token(self, pattern_name: str, match: re.Match, lineno: int, original: str) -> Token:
        """Create a token from a regex match.
        
        Args:
            pattern_name: Name of the pattern that matched.
            match: Regex match object.
            lineno: Line number.
            original: Original line content.
            
        Returns:
            Token created from the match.
        """
        token_type = self.token_type_map.get(pattern_name, TokenType.TEXT)
        
        if pattern_name == 'action_result':
            # Handle action_result pattern with groups
            if len(match.groups()) >= 2:
                return Token(
                    type=token_type,
                    value=match.group(1).strip(),
                    lineno=lineno,
                    result=match.group(2).strip(),
                    original=original
                )
            else:
                # Fallback if groups don't match expected
                return Token(
                    type=token_type,
                    value=match.group(0).strip(),
                    lineno=lineno,
                    original=original
                )
        else:
            # Handle other patterns
            value = match.group(1) if match.groups() else match.group(0)
            return Token(
                type=token_type,
                value=value.strip(),
                lineno=lineno,
                original=original
            )


class DefaultTokenizer(RegexTokenizer):
    """Default tokenizer with built-in patterns for backward compatibility."""
    
    def __init__(self):
        """Initialize with default patterns."""
        # Default patterns for backward compatibility
        default_patterns = {
            'step': re.compile(r'^(?:Étape|Etape|Step)\s*:\s*(.*)$', re.IGNORECASE),
            'action_result': re.compile(r'^Action\s*:\s*(.*?)\s*;\s*(?:R[ée]sultat|Resultat)\s*:\s*(.*)$', re.IGNORECASE),
            'action_only': re.compile(r'^Action\s*:\s*(.*)$', re.IGNORECASE),
            'result_only': re.compile(r'^R[ée]sultat\s*:\s*(.*)$', re.IGNORECASE),
            'comment': re.compile(r'^\s*#.*$', re.IGNORECASE),
        }
        super().__init__(default_patterns)


class FlexibleTokenizer(Tokenizer):
    """Tokenizer that can adapt patterns at runtime."""
    
    def __init__(self):
        """Initialize the flexible tokenizer."""
        self.patterns: Dict[str, re.Pattern] = {}
        self.token_type_map: Dict[str, TokenType] = {}
        self.pattern_priority: list[str] = []
    
    def add_pattern(self, name: str, pattern: str, token_type: TokenType, priority: Optional[int] = None):
        """Add a pattern to the tokenizer.
        
        Args:
            name: Pattern name.
            pattern: Regex pattern string.
            token_type: Token type for this pattern.
            priority: Priority order (lower numbers = higher priority).
        """
        try:
            compiled_pattern = re.compile(pattern, re.IGNORECASE)
            self.patterns[name] = compiled_pattern
            self.token_type_map[name] = token_type
            
            if priority is not None:
                # Insert at specific priority
                if priority < len(self.pattern_priority):
                    self.pattern_priority.insert(priority, name)
                else:
                    self.pattern_priority.append(name)
            else:
                # Add to end
                self.pattern_priority.append(name)
                
        except re.error as e:
            raise LexerError(f"Invalid regex pattern '{name}': {e}", 0)
    
    def remove_pattern(self, name: str):
        """Remove a pattern from the tokenizer.
        
        Args:
            name: Pattern name to remove.
        """
        self.patterns.pop(name, None)
        self.token_type_map.pop(name, None)
        if name in self.pattern_priority:
            self.pattern_priority.remove(name)
    
    def tokenize(self, text: str) -> Iterator[Token]:
        """Tokenize text using current patterns.
        
        Args:
            text: Input text to tokenize.
            
        Yields:
            Tokens from the input text.
        """
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            
            # Handle empty lines
            if not stripped:
                yield Token(
                    type=TokenType.EMPTY,
                    value="",
                    lineno=lineno,
                    original=line
                )
                continue
            
            # Try to match patterns in priority order
            token = self._match_patterns(stripped, lineno, line)
            if token:
                yield token
            else:
                # No pattern matched, treat as text
                yield Token(
                    type=TokenType.TEXT,
                    value=stripped,
                    lineno=lineno,
                    original=line
                )
    
    def _match_patterns(self, line: str, lineno: int, original: str) -> Optional[Token]:
        """Try to match line against patterns in priority order.
        
        Args:
            line: Line to match.
            lineno: Line number.
            original: Original line content.
            
        Returns:
            Token if pattern matched, None otherwise.
        """
        for pattern_name in self.pattern_priority:
            pattern = self.patterns.get(pattern_name)
            if pattern:
                match = pattern.match(line)
                if match:
                    return self._create_token(pattern_name, match, lineno, original)
        
        return None
    
    def _create_token(self, pattern_name: str, match: re.Match, lineno: int, original: str) -> Token:
        """Create a token from a regex match.
        
        Args:
            pattern_name: Name of the pattern that matched.
            match: Regex match object.
            lineno: Line number.
            original: Original line content.
            
        Returns:
            Token created from the match.
        """
        token_type = self.token_type_map.get(pattern_name, TokenType.TEXT)
        
        # Handle patterns with multiple groups
        if len(match.groups()) >= 2:
            return Token(
                type=token_type,
                value=match.group(1).strip(),
                lineno=lineno,
                result=match.group(2).strip(),
                original=original
            )
        elif len(match.groups()) == 1:
            return Token(
                type=token_type,
                value=match.group(1).strip(),
                lineno=lineno,
                original=original
            )
        else:
            return Token(
                type=token_type,
                value=match.group(0).strip(),
                lineno=lineno,
                original=original
            ) 