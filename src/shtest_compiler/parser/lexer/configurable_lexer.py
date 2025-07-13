"""
Configurable lexer that can use different tokenizers and filters.
"""

import os
import yaml
from typing import Iterator, Optional, Dict, Any
from .core import Token
from .tokenizers import Tokenizer, RegexTokenizer, FallbackTokenizer
from .filters import Filter, EmptyFilter, WhitespaceFilter
from .pattern_loader import PatternLoader
from ...config.debug_config import is_debug_enabled, debug_print

debug_print("LEXER DEBUG ACTIVE: src/shtest_compiler/parser/lexer/configurable_lexer.py loaded")


class ConfigurableLexer:
    """A lexer that can be configured with different tokenizers and filters."""
    
    def __init__(self, 
                 config_path: Optional[str] = None,
                 tokenizers: Optional[list] = None,
                 filters: Optional[list] = None,
                 debug: bool = False):
        """
        Initialize the configurable lexer.
        
        Args:
            config_path: Path to YAML configuration file
            tokenizers: List of tokenizer instances
            filters: List of filter instances
            debug: Enable debug mode (deprecated, use global debug config)
        """
        # Use global debug configuration
        self.debug = debug or is_debug_enabled()
        self.config_path = config_path
        self.tokenizers = tokenizers or []
        self.filters = filters or []
        
        # Load configuration if provided
        if config_path:
            self._load_config(config_path)
        
        # Add default components if none provided
        if not self.tokenizers:
            self._add_default_tokenizers()
        
        if not self.filters:
            self._add_default_filters()
    
    def _load_config(self, config_path: str) -> None:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Load tokenizers
            if 'tokenizers' in config:
                for tokenizer_config in config['tokenizers']:
                    tokenizer = self._create_tokenizer(tokenizer_config)
                    if tokenizer:
                        self.tokenizers.append(tokenizer)
            
            # Load filters
            if 'filters' in config:
                for filter_config in config['filters']:
                    filter_obj = self._create_filter(filter_config)
                    if filter_obj:
                        self.filters.append(filter_obj)
                        
        except Exception as e:
            if self.debug:
                debug_print(f"[DEBUG] Using fallback tokenizer: {e}")
            self._add_default_tokenizers()
    
    def _create_tokenizer(self, config: Dict[str, Any]) -> Optional[Tokenizer]:
        """Create a tokenizer from configuration."""
        tokenizer_type = config.get('type', 'regex')
        
        if tokenizer_type == 'regex':
            pattern = config.get('pattern', '')
            token_type = config.get('token_type', 'TEXT')
            return RegexTokenizer(pattern, token_type)
        
        return None
    
    def _create_filter(self, config: Dict[str, Any]) -> Optional[Filter]:
        """Create a filter from configuration."""
        filter_type = config.get('type', 'empty')
        
        if filter_type == 'empty':
            return EmptyFilter()
        elif filter_type == 'whitespace':
            return WhitespaceFilter()
        
        return None
    
    def _add_default_tokenizers(self) -> None:
        """Add default tokenizers using patterns from regex_config.yml."""
        try:
            # Load patterns from regex_config.yml
            pattern_loader = PatternLoader()
            patterns = pattern_loader.load()
            
            if self.debug:
                debug_print(f"[DEBUG] Loaded patterns: {list(patterns.keys())}")
            
            # Add tokenizers in order of specificity (most specific first)
            # 1. STEP pattern
            if 'step' in patterns:
                self.tokenizers.append(RegexTokenizer(patterns['step'].pattern, 'STEP'))
                if self.debug:
                    debug_print(f"[DEBUG] Added STEP tokenizer with pattern: {patterns['step'].pattern}")
            
            # 2. ACTION_RESULT pattern (most specific - action and result on same line)
            if 'action_result' in patterns:
                self.tokenizers.append(RegexTokenizer(patterns['action_result'].pattern, 'ACTION_RESULT'))
                if self.debug:
                    debug_print(f"[DEBUG] Added ACTION_RESULT tokenizer with pattern: {patterns['action_result'].pattern}")
            
            # 3. ACTION_ONLY pattern
            if 'action_only' in patterns:
                self.tokenizers.append(RegexTokenizer(patterns['action_only'].pattern, 'ACTION_ONLY'))
                if self.debug:
                    debug_print(f"[DEBUG] Added ACTION_ONLY tokenizer with pattern: {patterns['action_only'].pattern}")
            
            # 4. RESULT_ONLY pattern
            if 'result_only' in patterns:
                self.tokenizers.append(RegexTokenizer(patterns['result_only'].pattern, 'RESULT_ONLY'))
                if self.debug:
                    debug_print(f"[DEBUG] Added RESULT_ONLY tokenizer with pattern: {patterns['result_only'].pattern}")
            
            # 5. Add fallback tokenizer last
            self.tokenizers.append(FallbackTokenizer())
            if self.debug:
                debug_print("[DEBUG] Added FallbackTokenizer")
                
        except Exception as e:
            if self.debug:
                debug_print(f"[DEBUG] Failed to load patterns from regex_config.yml: {e}")
                debug_print("[DEBUG] Using hardcoded fallback patterns")
            
            # Fallback to hardcoded patterns
            self.tokenizers.append(RegexTokenizer(r'^(?:Étape|Etape|Step)\s*:\s*(.+)$', 'STEP'))
            self.tokenizers.append(RegexTokenizer(r'^Action:\s*(.+)$', 'ACTION_ONLY'))
            self.tokenizers.append(RegexTokenizer(r'^Résultat:\s*(.+)$', 'RESULT_ONLY'))
            self.tokenizers.append(FallbackTokenizer())
    
    def _add_default_filters(self) -> None:
        """Add default filters."""
        self.filters.append(EmptyFilter())
        self.filters.append(WhitespaceFilter())
    
    def lex(self, text: str) -> Iterator[Token]:
        """Lex text into tokens."""
        if self.debug:
            debug_print(f"[DEBUG] Lexing text with {len(text.splitlines())} lines")
        
        # Apply tokenizers
        tokens = []
        for tokenizer in self.tokenizers:
            try:
                for token in tokenizer.tokenize(text):
                    tokens.append(token)
                    if self.debug:
                        debug_print(f"[DEBUG] Yielding token: {token}")
            except Exception as e:
                if self.debug:
                    debug_print(f"[DEBUG] Tokenizer error: {e}")
        
        # Apply filters
        for filter_obj in self.filters:
            tokens = list(filter_obj.filter(tokens, verbose=self.debug))
        
        # Yield filtered tokens
        for token in tokens:
            if self.debug:
                debug_print(f"[DEBUG] ConfigurableLexer.lex: Produced token kind={token.kind}, value={token.value}, result={getattr(token, 'result', None)}, original={getattr(token, 'original', None)}")
            yield token
    
    def lex_file(self, file_path: str) -> Iterator[Token]:
        """Lex a file into tokens."""
        if self.debug:
            debug_print(f"[DEBUG] Lexing file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            for token in self.lex(text):
                if self.debug:
                    debug_print(f"[DEBUG] ConfigurableLexer.lex_file: Yielding token kind={token.kind}, value={token.value}, result={getattr(token, 'result', None)}, original={getattr(token, 'original', None)}")
                yield token
                
        except Exception as e:
            if self.debug:
                debug_print(f"[DEBUG] File lexing error: {e}")
            raise
    
    def reload_config(self) -> None:
        """Reload configuration from file."""
        if self.config_path:
            if self.debug:
                debug_print("[DEBUG] Reloading configuration")
            try:
                self._load_config(self.config_path)
            except Exception as e:
                if self.debug:
                    debug_print(f"[DEBUG] Failed to reload config: {e}")
    
    def add_tokenizer(self, tokenizer: Tokenizer) -> None:
        """Add a tokenizer to the lexer."""
        self.tokenizers.append(tokenizer)
    
    def add_filter(self, filter_obj: Filter) -> None:
        """Add a filter to the lexer."""
        self.filters.append(filter_obj)
    
    def get_tokenizer_info(self) -> Dict[str, Any]:
        """Get information about the lexer configuration."""
        return {
            "tokenizers": [type(t).__name__ for t in self.tokenizers],
            "filters": [type(f).__name__ for f in self.filters],
            "config_path": self.config_path,
            "debug": self.debug
        } 