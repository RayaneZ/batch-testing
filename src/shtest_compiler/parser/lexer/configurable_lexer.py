"""
Configurable lexer for KnightBatch.

This module provides the main lexer interface that combines pattern loading,
tokenization, and filtering into a unified, configurable system.
"""

from typing import Iterator, Optional, List
from pathlib import Path

from .core import Token, TokenType, LexerError
from .pattern_loader import PatternLoader
from .tokenizers import Tokenizer, RegexTokenizer, DefaultTokenizer, FlexibleTokenizer
from .filters import TokenFilter, CompositeFilter, EmptyLineFilter, CommentFilter, DebugFilter


class ConfigurableLexer:
    """Main configurable lexer class."""
    
    def __init__(self, 
                 config_path: Optional[str] = None,
                 tokenizer: Optional[Tokenizer] = None,
                 filters: Optional[List[TokenFilter]] = None,
                 debug: bool = False):
        """Initialize the configurable lexer.
        
        Args:
            config_path: Path to YAML configuration file.
            tokenizer: Tokenizer to use. If None, creates default.
            filters: List of filters to apply. If None, uses default filters.
            debug: Whether to enable debug mode.
        """
        self.config_path = config_path
        self.debug = debug
        
        # Initialize pattern loader
        self.pattern_loader = PatternLoader(config_path)
        
        # Initialize tokenizer
        if tokenizer is None:
            self.tokenizer = self._create_default_tokenizer()
        else:
            self.tokenizer = tokenizer
        
        # Initialize filters
        if filters is None:
            self.filters = self._create_default_filters()
        else:
            self.filters = filters
        
        # Create composite filter
        self.composite_filter = CompositeFilter(self.filters)
    
    def _create_default_tokenizer(self) -> Tokenizer:
        """Create default tokenizer with loaded patterns."""
        try:
            patterns = self.pattern_loader.load()
            return RegexTokenizer(patterns)
        except (FileNotFoundError, Exception) as e:
            # Fallback to default patterns if config loading fails
            if self.debug:
                print(f"[DEBUG] Using fallback tokenizer: {e}")
            return DefaultTokenizer()
    
    def _create_default_filters(self) -> List[TokenFilter]:
        """Create default filter chain."""
        filters = []
        
        # Always filter empty lines
        filters.append(EmptyLineFilter(enabled=True))
        
        # Filter comments unless in debug mode
        filters.append(CommentFilter(enabled=not self.debug))
        
        # Add debug filter if debug mode is enabled
        if self.debug:
            filters.append(DebugFilter(enabled=True, verbose=True))
        
        return filters
    
    def lex(self, text: str) -> Iterator[Token]:
        """Tokenize text using the configured lexer.
        
        Args:
            text: Input text to tokenize.
            
        Yields:
            Tokens from the input text.
        """
        if self.debug:
            print(f"[DEBUG] Lexing text with {len(text.splitlines())} lines")
        
        # Tokenize the text
        tokens = self.tokenizer.tokenize(text)
        
        # Apply filters
        filtered_tokens = self.composite_filter(tokens)
        
        # Yield filtered tokens
        for token in filtered_tokens:
            if self.debug:
                print(f"[DEBUG] Yielding token: {token}")
            yield token
    
    def lex_file(self, file_path: str) -> Iterator[Token]:
        """Tokenize a file using the configured lexer.
        
        Args:
            file_path: Path to the file to tokenize.
            
        Yields:
            Tokens from the file.
            
        Raises:
            FileNotFoundError: If the file doesn't exist.
            LexerError: If there's an error during tokenization.
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if self.debug:
            print(f"[DEBUG] Lexing file: {file_path}")
        
        try:
            with open(file_path, encoding="utf-8") as f:
                text = f.read()
            
            yield from self.lex(text)
            
        except UnicodeDecodeError as e:
            raise LexerError(f"Unicode decode error in {file_path}: {e}", 0)
        except Exception as e:
            raise LexerError(f"Error reading file {file_path}: {e}", 0)
    
    def reload_config(self) -> None:
        """Reload the configuration and recreate the tokenizer."""
        if self.debug:
            print("[DEBUG] Reloading configuration")
        
        try:
            # Reload patterns
            self.pattern_loader.reload()
            
            # Recreate tokenizer with new patterns
            if isinstance(self.tokenizer, RegexTokenizer):
                patterns = self.pattern_loader.load()
                self.tokenizer = RegexTokenizer(patterns)
            
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Failed to reload config: {e}")
            raise LexerError(f"Failed to reload configuration: {e}", 0)
    
    def add_filter(self, filter_obj: TokenFilter) -> None:
        """Add a filter to the filter chain.
        
        Args:
            filter_obj: Filter to add.
        """
        self.composite_filter.add_filter(filter_obj)
    
    def remove_filter(self, filter_class: type) -> None:
        """Remove filters of a specific class.
        
        Args:
            filter_class: Class of filters to remove.
        """
        self.composite_filter.remove_filter(filter_class)
    
    def set_debug(self, enabled: bool) -> None:
        """Enable or disable debug mode.
        
        Args:
            enabled: Whether to enable debug mode.
        """
        self.debug = enabled
        
        # Update debug filter
        debug_filters = [f for f in self.filters if isinstance(f, DebugFilter)]
        if debug_filters:
            debug_filters[0].enabled = enabled
            debug_filters[0].verbose = enabled
        else:
            # Add debug filter if not present
            self.add_filter(DebugFilter(enabled=enabled, verbose=enabled))
        
        # Update comment filter
        comment_filters = [f for f in self.filters if isinstance(f, CommentFilter)]
        if comment_filters:
            comment_filters[0].enabled = not enabled
    
    def get_patterns(self) -> dict:
        """Get current patterns.
        
        Returns:
            Dictionary of current patterns.
        """
        return self.pattern_loader.load()
    
    def add_pattern(self, name: str, pattern: str, token_type: TokenType) -> None:
        """Add a new pattern to the tokenizer.
        
        Args:
            name: Pattern name.
            pattern: Regex pattern string.
            token_type: Token type for this pattern.
        """
        if isinstance(self.tokenizer, FlexibleTokenizer):
            self.tokenizer.add_pattern(name, pattern, token_type)
        else:
            # Add to pattern loader for future reloads
            self.pattern_loader.add_pattern(name, pattern)
            
            # Recreate tokenizer with new patterns
            patterns = self.pattern_loader.load()
            self.tokenizer = RegexTokenizer(patterns)
    
    def list_patterns(self) -> list[str]:
        """List all available patterns.
        
        Returns:
            List of pattern names.
        """
        return self.pattern_loader.list_patterns()


# Convenience functions for backward compatibility
def lex(text: str, debug: bool = False) -> Iterator[Token]:
    """Tokenize text using default configuration.
    
    Args:
        text: Input text to tokenize.
        debug: Whether to enable debug mode.
        
    Yields:
        Tokens from the input text.
    """
    lexer = ConfigurableLexer(debug=debug)
    yield from lexer.lex(text)


def lex_file(path: str, debug: bool = False) -> Iterator[Token]:
    """Tokenize a file using default configuration.
    
    Args:
        path: Path to the file to tokenize.
        debug: Whether to enable debug mode.
        
    Yields:
        Tokens from the file.
    """
    lexer = ConfigurableLexer(debug=debug)
    yield from lexer.lex_file(path) 