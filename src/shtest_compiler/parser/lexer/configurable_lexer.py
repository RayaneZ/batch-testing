"""
Configurable lexer that can use different tokenizers and filters.
"""

import os
from typing import Any, Dict, Iterator, Optional

import yaml

from ...utils.logger import debug_log, is_debug_enabled
from .core import Token, TokenType
from .filters import EmptyFilter, Filter, WhitespaceFilter
from .pattern_loader import PatternLoader
from .tokenizers import FallbackTokenizer, RegexTokenizer, Tokenizer

debug_log(
    "LEXER DEBUG ACTIVE: src/shtest_compiler/parser/lexer/configurable_lexer.py loaded"
)


class ConfigurableLexer:
    """A lexer that can be configured with different tokenizers and filters."""

    def __init__(
        self,
        config_path: Optional[str] = None,
        tokenizers: Optional[list] = None,
        filters: Optional[list] = None,
        debug: bool = False,
    ):
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
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

            # Load tokenizers
            if "tokenizers" in config:
                for tokenizer_config in config["tokenizers"]:
                    tokenizer = self._create_tokenizer(tokenizer_config)
                    if tokenizer:
                        self.tokenizers.append(tokenizer)

            # Load filters
            if "filters" in config:
                for filter_config in config["filters"]:
                    filter_obj = self._create_filter(filter_config)
                    if filter_obj:
                        self.filters.append(filter_obj)

        except Exception as e:
            if self.debug:
                debug_log(f"Using fallback tokenizer: {e}")
            self._add_default_tokenizers()

    def _create_tokenizer(self, config: Dict[str, Any]) -> Optional[Tokenizer]:
        """Create a tokenizer from configuration."""
        tokenizer_type = config.get("type", "regex")

        if tokenizer_type == "regex":
            pattern = config.get("pattern", "")
            token_type = config.get("token_type", "TEXT")
            return RegexTokenizer(pattern, token_type, debug=self.debug)

        return None

    def _create_filter(self, config: Dict[str, Any]) -> Optional[Filter]:
        """Create a filter from configuration."""
        filter_type = config.get("type", "empty")

        if filter_type == "empty":
            return EmptyFilter()
        elif filter_type == "whitespace":
            return WhitespaceFilter()

        return None

    def _add_default_tokenizers(self) -> None:
        """Add default tokenizers using patterns from regex_config.yml."""
        try:
            # Load patterns from regex_config.yml
            pattern_loader = PatternLoader()
            patterns = pattern_loader.load()
            if self.debug:
                debug_log(f"Loaded patterns: {list(patterns.keys())}")
                for k, v in patterns.items():
                    debug_log(
                        f"Pattern for {k}: {v.pattern if hasattr(v, 'pattern') else v}"
                    )
            # Add tokenizers in order of specificity (most specific first)
            # 1. STEP pattern
            if "step" in patterns:
                self.add_tokenizer(
                    RegexTokenizer(patterns["step"], "STEP", debug=self.debug)
                )
                if self.debug:
                    debug_log(
                        f"Added STEP tokenizer with pattern: {patterns['step'].pattern if hasattr(patterns['step'], 'pattern') else patterns['step']}"
                    )
            # 2. ACTION_RESULT pattern
            if "action_result" in patterns:
                self.add_tokenizer(
                    RegexTokenizer(
                        patterns["action_result"], "ACTION_RESULT", debug=self.debug
                    )
                )
                if self.debug:
                    debug_log(
                        f"Added ACTION_RESULT tokenizer with pattern: {patterns['action_result'].pattern if hasattr(patterns['action_result'], 'pattern') else patterns['action_result']}"
                    )
            # 3. ACTION_ONLY pattern
            if "action_only" in patterns:
                self.add_tokenizer(
                    RegexTokenizer(
                        patterns["action_only"], "ACTION_ONLY", debug=self.debug
                    )
                )
                if self.debug:
                    debug_log(
                        f"Added ACTION_ONLY tokenizer with pattern: {patterns['action_only'].pattern if hasattr(patterns['action_only'], 'pattern') else patterns['action_only']}"
                    )
            # 4. RESULT_ONLY pattern
            if "result_only" in patterns:
                self.add_tokenizer(
                    RegexTokenizer(
                        patterns["result_only"], "RESULT_ONLY", debug=self.debug
                    )
                )
                if self.debug:
                    debug_log(
                        f"Added RESULT_ONLY tokenizer with pattern: {patterns['result_only'].pattern if hasattr(patterns['result_only'], 'pattern') else patterns['result_only']}"
                    )
            # 5. COMMENT pattern
            if "comment" in patterns:
                self.add_tokenizer(
                    RegexTokenizer(patterns["comment"], "COMMENT", debug=self.debug)
                )
                if self.debug:
                    debug_log(
                        f"Added COMMENT tokenizer with pattern: {patterns['comment'].pattern if hasattr(patterns['comment'], 'pattern') else patterns['comment']}"
                    )
            # 6. Fallback
            self.add_tokenizer(FallbackTokenizer())
            if self.debug:
                debug_log(f"Added FallbackTokenizer")
        except Exception as e:
            debug_log(f"[ERROR] Failed to add default tokenizers: {e}")
            raise

    def _add_default_filters(self) -> None:
        """Add default filters."""
        self.filters.append(EmptyFilter())
        self.filters.append(WhitespaceFilter())

    def lex(self, text: str) -> Iterator[Token]:
        """Lex text into tokens."""
        if self.debug:
            debug_log(f"Lexing text with {len(text.splitlines())} lines")
        lines = text.split("\n")
        for lineno, line in enumerate(lines, 1):
            stripped = line.strip()
            matched = False
            for tokenizer in self.tokenizers:
                tokens = list(tokenizer.tokenize(line))
                if tokens:
                    token = tokens[0]
                    # Only yield if not TEXT, or if it's the fallback
                    if token.type != TokenType.TEXT or isinstance(
                        tokenizer, FallbackTokenizer
                    ):
                        if self.debug:
                            debug_log(f"Yielding token: {token}")
                        yield token
                        matched = True
                        break
            if not matched:
                # If no tokenizer matched, yield as TEXT
                token = Token(
                    type=TokenType.TEXT, value=stripped, lineno=lineno, original=line
                )
                if self.debug:
                    debug_log(f"Yielding fallback TEXT token: {token}")
                yield token

    def lex_file(self, file_path: str) -> Iterator[Token]:
        """Lex a file into tokens."""
        if self.debug:
            debug_log(f"Lexing file: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            for token in self.lex(text):
                if self.debug:
                    debug_log(
                        f"ConfigurableLexer.lex_file: Yielding token kind={token.kind}, value={token.value}, result={getattr(token, 'result', None)}, original={getattr(token, 'original', None)}"
                    )
                yield token

        except Exception as e:
            from shtest_compiler.utils.logger import log_pipeline_error
            import traceback
            log_pipeline_error(f"[ERROR] {type(e).__name__}: {e}\n{traceback.format_exc()}")
            raise

    def reload_config(self) -> None:
        """Reload configuration from file."""
        if self.config_path:
            if self.debug:
                debug_log("Reloading configuration")
            try:
                self._load_config(self.config_path)
            except Exception as e:
                if self.debug:
                    debug_log(f"Failed to reload config: {e}")

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
            "debug": self.debug,
        }
