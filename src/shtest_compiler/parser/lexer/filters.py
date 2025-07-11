"""
Token filters for the modular lexer.

This module provides a filter system that allows preprocessing and postprocessing
of tokens during lexical analysis.
"""

from abc import ABC, abstractmethod
from typing import Iterator, Optional
from .core import Token, TokenType


class TokenFilter(ABC):
    """Base class for token filters."""
    
    def __init__(self, enabled: bool = True):
        """Initialize the filter.
        
        Args:
            enabled: Whether the filter is active.
        """
        self.enabled = enabled
    
    @abstractmethod
    def filter(self, tokens: Iterator[Token]) -> Iterator[Token]:
        """Filter a stream of tokens.
        
        Args:
            tokens: Input token stream.
            
        Yields:
            Filtered token stream.
        """
        pass
    
    def __call__(self, tokens: Iterator[Token]) -> Iterator[Token]:
        """Make the filter callable."""
        if self.enabled:
            return self.filter(tokens)
        return tokens


class EmptyLineFilter(TokenFilter):
    """Filter that removes empty line tokens."""
    
    def filter(self, tokens: Iterator[Token]) -> Iterator[Token]:
        """Remove empty line tokens from the stream."""
        for token in tokens:
            if token.type != TokenType.EMPTY:
                yield token


class CommentFilter(TokenFilter):
    """Filter that removes comment tokens."""
    
    def filter(self, tokens: Iterator[Token]) -> Iterator[Token]:
        """Remove comment tokens from the stream."""
        for token in tokens:
            if token.type != TokenType.COMMENT:
                yield token


class DebugFilter(TokenFilter):
    """Filter that adds debug information to tokens."""
    
    def __init__(self, enabled: bool = True, verbose: bool = False):
        """Initialize the debug filter.
        
        Args:
            enabled: Whether the filter is active.
            verbose: Whether to print detailed debug information.
        """
        super().__init__(enabled)
        self.verbose = verbose
    
    def filter(self, tokens: Iterator[Token]) -> Iterator[Token]:
        """Add debug information to tokens."""
        for token in tokens:
            if self.verbose:
                print(f"[DEBUG] Token: {token}")
            
            # Add debug metadata
            token.metadata['debug'] = True
            yield token


class ValidationFilter(TokenFilter):
    """Filter that validates token consistency."""
    
    def __init__(self, enabled: bool = True, strict: bool = False):
        """Initialize the validation filter.
        
        Args:
            enabled: Whether the filter is active.
            strict: Whether to raise errors on validation failures.
        """
        super().__init__(enabled)
        self.strict = strict
    
    def filter(self, tokens: Iterator[Token]) -> Iterator[Token]:
        """Validate tokens and optionally raise errors."""
        for token in tokens:
            # Validate token
            if not self._validate_token(token):
                if self.strict:
                    raise ValueError(f"Invalid token: {token}")
                else:
                    # Mark as error token
                    token.type = TokenType.ERROR
                    token.metadata['validation_error'] = True
            
            yield token
    
    def _validate_token(self, token: Token) -> bool:
        """Validate a single token.
        
        Args:
            token: Token to validate.
            
        Returns:
            True if token is valid, False otherwise.
        """
        # Basic validation
        if not token.value or token.lineno < 1:
            return False
        
        # Type-specific validation
        if token.type == TokenType.ACTION_RESULT:
            if not token.result:
                return False
        
        return True


class MetadataFilter(TokenFilter):
    """Filter that adds metadata to tokens based on patterns."""
    
    def __init__(self, enabled: bool = True, metadata_rules: Optional[dict] = None):
        """Initialize the metadata filter.
        
        Args:
            enabled: Whether the filter is active.
            metadata_rules: Rules for adding metadata to tokens.
        """
        super().__init__(enabled)
        self.metadata_rules = metadata_rules or {}
    
    def filter(self, tokens: Iterator[Token]) -> Iterator[Token]:
        """Add metadata to tokens based on rules."""
        for token in tokens:
            # Apply metadata rules
            for rule_name, rule_func in self.metadata_rules.items():
                if callable(rule_func):
                    result = rule_func(token)
                    if result:
                        token.metadata[rule_name] = result
            
            yield token


class CompositeFilter(TokenFilter):
    """Filter that combines multiple filters."""
    
    def __init__(self, filters: list[TokenFilter], enabled: bool = True):
        """Initialize the composite filter.
        
        Args:
            filters: List of filters to apply in order.
            enabled: Whether the filter is active.
        """
        super().__init__(enabled)
        self.filters = filters
    
    def filter(self, tokens: Iterator[Token]) -> Iterator[Token]:
        """Apply all filters in sequence."""
        current_tokens = tokens
        
        for filter_obj in self.filters:
            if filter_obj.enabled:
                current_tokens = filter_obj(current_tokens)
        
        yield from current_tokens
    
    def add_filter(self, filter_obj: TokenFilter):
        """Add a filter to the composite filter.
        
        Args:
            filter_obj: Filter to add.
        """
        self.filters.append(filter_obj)
    
    def remove_filter(self, filter_class: type):
        """Remove filters of a specific class.
        
        Args:
            filter_class: Class of filters to remove.
        """
        self.filters = [f for f in self.filters if not isinstance(f, filter_class)] 