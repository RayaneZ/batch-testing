"""
Tests for the modular lexer architecture.

This module tests all components of the new modular lexer system.
"""

import os
import re
import tempfile
from pathlib import Path

import pytest

from shtest_compiler.parser.lexer import (
    ConfigurableLexer,
    LexerError,
    PatternLoader,
    Token,
    TokenType,
)
from shtest_compiler.parser.lexer.tokenizers import RegexTokenizer


class TestToken:
    """Test the Token class."""

    def test_token_creation(self):
        """Test basic token creation."""
        token = Token(TokenType.STEP, "Test step", 1)
        assert token.type == TokenType.STEP
        assert token.value == "Test step"
        assert token.lineno == 1
        assert token.column == 0
        assert token.result is None

    def test_token_with_result(self):
        """Test token creation with result."""
        token = Token(TokenType.ACTION_RESULT, "echo hello", 2, result="hello")
        assert token.type == TokenType.ACTION_RESULT
        assert token.value == "echo hello"
        assert token.result == "hello"
        assert token.lineno == 2

    def test_token_validation(self):
        """Test token validation."""
        # Invalid token type
        with pytest.raises(ValueError, match="Invalid token type"):
            Token("INVALID", "test", 1)

        # Invalid line number
        with pytest.raises(ValueError, match="Line number must be >= 1"):
            Token(TokenType.STEP, "test", 0)

        # Invalid column
        with pytest.raises(ValueError, match="Column must be >= 0"):
            Token(TokenType.STEP, "test", 1, column=-1)

    def test_token_string_representation(self):
        """Test token string representation."""
        token = Token(TokenType.STEP, "Test step", 1)
        assert str(token) == "STEP@1:0 'Test step'"

        token_with_result = Token(
            TokenType.ACTION_RESULT, "echo hello", 2, result="hello"
        )
        assert str(token_with_result) == "ACTION_RESULT@2:0 'echo hello' -> 'hello'"

    def test_token_backward_compatibility(self):
        """Test backward compatibility with 'kind' property."""
        token = Token(TokenType.STEP, "test", 1)
        assert token.kind == "STEP"


class TestLexerError:
    """Test the LexerError class."""

    def test_lexer_error_creation(self):
        """Test basic lexer error creation."""
        error = LexerError("Test error", 5)
        assert error.message == "Test error"
        assert error.lineno == 5
        assert error.column == 0
        assert error.line is None

    def test_lexer_error_with_line(self):
        """Test lexer error with line information."""
        error = LexerError("Test error", 5, 10, "echo hello")
        assert error.line == "echo hello"
        assert "Line: echo hello" in str(error)
        assert "         ^" in str(error)


class TestPatternLoader:
    """Test the PatternLoader class."""

    def test_pattern_loader_creation(self):
        """Test pattern loader creation."""
        loader = PatternLoader()
        assert loader.config_path.exists()
        assert not loader._compiled

    def test_pattern_loader_load(self):
        """Test pattern loading."""
        loader = PatternLoader()
        patterns = loader.load()

        # Check that we get some patterns
        assert len(patterns) > 0

        # Check that patterns are compiled
        for pattern in patterns.values():
            assert hasattr(pattern, "match")

    def test_pattern_loader_get_pattern(self):
        """Test getting specific patterns."""
        loader = PatternLoader()
        step_pattern = loader.get_pattern("step")
        if step_pattern is not None:
            assert step_pattern.match("Step: Test")

        # Non-existent pattern
        assert loader.get_pattern("nonexistent") is None

    def test_pattern_loader_add_pattern(self):
        """Test adding patterns at runtime."""
        loader = PatternLoader()
        loader.add_pattern("test", r"^test\s+(.+)$")

        pattern = loader.get_pattern("test")
        assert pattern is not None
        assert pattern.match("test value")

    def test_pattern_loader_invalid_pattern(self):
        """Test handling of invalid patterns."""
        loader = PatternLoader()

        with pytest.raises(re.error):
            loader.add_pattern("invalid", "[invalid")


class TestRegexTokenizer:
    """Test the RegexTokenizer class."""

    def test_regex_tokenizer_creation(self):
        """Test regex tokenizer creation."""
        tokenizer = RegexTokenizer(r"^test\s+(.+)$", "TEXT")
        assert tokenizer.pattern is not None
        assert tokenizer.token_type == TokenType.TEXT

    def test_regex_tokenizer_tokenize(self):
        """Test regex tokenizer tokenization."""
        tokenizer = RegexTokenizer(r"^Step:\s+(.+)$", "STEP")
        text = "Step: Test step"

        tokens = list(tokenizer.tokenize(text))
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.STEP
        assert tokens[0].value == "Test step"


class TestConfigurableLexer:
    """Test the ConfigurableLexer class."""

    def test_configurable_lexer_creation(self):
        """Test configurable lexer creation."""
        lexer = ConfigurableLexer()
        assert lexer.debug is False
        assert len(lexer.tokenizers) > 0
        assert len(lexer.filters) > 0

    def test_configurable_lexer_debug_mode(self):
        """Test configurable lexer in debug mode."""
        lexer = ConfigurableLexer(debug=True)
        assert lexer.debug is True

    def test_configurable_lexer_lex_text(self):
        """Test lexing text with configurable lexer."""
        lexer = ConfigurableLexer()
        text = "Step: Test step\nAction: echo hello"

        tokens = list(lexer.lex(text))
        # Just check that we get some tokens
        assert len(tokens) > 0
        for token in tokens:
            assert hasattr(token, "type")
            assert hasattr(token, "value")

    def test_configurable_lexer_lex_file(self):
        """Test lexing file with configurable lexer."""
        lexer = ConfigurableLexer()

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".shtest", encoding="utf-8"
        ) as f:
            f.write("Step: Test step\nAction: echo hello")
            temp_file = f.name

        try:
            tokens = list(lexer.lex_file(temp_file))
            # Just check that we get some tokens
            assert len(tokens) > 0
            for token in tokens:
                assert hasattr(token, "type")
                assert hasattr(token, "value")
        finally:
            os.unlink(temp_file)

    def test_configurable_lexer_file_not_found(self):
        """Test lexing non-existent file."""
        lexer = ConfigurableLexer()

        with pytest.raises(FileNotFoundError):
            list(lexer.lex_file("/nonexistent/file.shtest"))

    def test_configurable_lexer_add_tokenizer(self):
        """Test adding tokenizers to configurable lexer."""
        lexer = ConfigurableLexer()
        initial_tokenizer_count = len(lexer.tokenizers)

        # Add a custom tokenizer
        custom_tokenizer = RegexTokenizer(r"^custom\s+(.+)$", "TEXT")
        lexer.add_tokenizer(custom_tokenizer)

        assert len(lexer.tokenizers) == initial_tokenizer_count + 1

    def test_configurable_lexer_get_tokenizer_info(self):
        """Test getting tokenizer information."""
        lexer = ConfigurableLexer()
        info = lexer.get_tokenizer_info()

        assert "tokenizers" in info
        assert "filters" in info
        assert "config_path" in info
        assert "debug" in info
