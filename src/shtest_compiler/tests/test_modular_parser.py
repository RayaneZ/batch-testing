"""
Tests for the modular parser architecture.

This module tests all components of the new modular parser system.
"""

import pytest
import tempfile
import os
from pathlib import Path

from shtest_compiler.parser import (
    ParseError, TokenLike, ASTBuilder, Grammar,
    ConfigurableParser, DefaultASTBuilder, DefaultGrammar
)
from shtest_compiler.parser.shtest_ast import ShtestFile, Action, TestStep
from shtest_compiler.parser.lexer import ConfigurableLexer


class TestParseError:
    """Test the ParseError class."""
    
    def test_parse_error_creation(self):
        """Test basic parse error creation."""
        error = ParseError("Test error")
        assert error.message == "Test error"
        assert error.lineno is None
        assert error.column is None
    
    def test_parse_error_with_line_column(self):
        """Test parse error with line and column information."""
        error = ParseError("Test error", lineno=5, column=10)
        assert error.message == "Test error"
        assert error.lineno == 5
        assert error.column == 10
        assert "Line 5" in str(error)
        assert "(col 10)" in str(error)


class TestDefaultASTBuilder:
    """Test the DefaultASTBuilder class."""
    
    def test_default_ast_builder_creation(self):
        """Test default AST builder creation."""
        builder = DefaultASTBuilder()
        assert builder is not None
    
    def test_build_empty_tokens(self):
        """Test building AST from empty token list."""
        builder = DefaultASTBuilder()
        tokens = []
        ast = builder.build(tokens)
        
        assert isinstance(ast, ShtestFile)
        assert len(ast.steps) == 0
    
    def test_build_step_token(self):
        """Test building AST with step token."""
        builder = DefaultASTBuilder()
        
        # Create a mock token
        class MockToken:
            def __init__(self):
                self.kind = "STEP"
                self.value = "Test Step"
                self.lineno = 1
                self.result = None
                self.original = "Step: Test Step"
        
        tokens = [MockToken()]
        ast = builder.build(tokens)
        
        assert len(ast.steps) == 1
        assert ast.steps[0].name == "Test Step"
        assert ast.steps[0].lineno == 1
    
    def test_build_action_result_token(self):
        """Test building AST with action_result token."""
        builder = DefaultASTBuilder()
        
        # Create a mock step token
        class MockStepToken:
            def __init__(self):
                self.kind = "STEP"
                self.value = "Test Step"
                self.lineno = 1
                self.result = None
                self.original = "Step: Test Step"
        
        # Create a mock action_result token
        class MockActionToken:
            def __init__(self):
                self.kind = "ACTION_RESULT"
                self.value = "echo hello"
                self.lineno = 2
                self.result = "hello"
                self.original = "Action: echo hello ; Résultat: hello"
        
        tokens = [MockStepToken(), MockActionToken()]
        ast = builder.build(tokens)
        
        assert len(ast.steps) == 1
        assert len(ast.steps[0].actions) == 1
        assert ast.steps[0].actions[0].command == "echo hello"
        assert ast.steps[0].actions[0].result_expr == "hello"
    
    def test_build_action_only_token(self):
        """Test building AST with action_only token."""
        builder = DefaultASTBuilder()
        
        # Create a mock step token
        class MockStepToken:
            def __init__(self):
                self.kind = "STEP"
                self.value = "Test Step"
                self.lineno = 1
                self.result = None
                self.original = "Step: Test Step"
        
        # Create a mock action_only token
        class MockActionToken:
            def __init__(self):
                self.kind = "ACTION_ONLY"
                self.value = "echo hello"
                self.lineno = 2
                self.result = None
                self.original = "Action: echo hello"
        
        tokens = [MockStepToken(), MockActionToken()]
        ast = builder.build(tokens)
        
        assert len(ast.steps) == 1
        assert len(ast.steps[0].actions) == 1
        assert ast.steps[0].actions[0].command == "echo hello"
        assert ast.steps[0].actions[0].result_expr is None
    
    def test_build_result_only_token(self):
        """Test building AST with result_only token."""
        builder = DefaultASTBuilder()
        
        # Create a mock step token
        class MockStepToken:
            def __init__(self):
                self.kind = "STEP"
                self.value = "Test Step"
                self.lineno = 1
                self.result = None
                self.original = "Step: Test Step"
        
        # Create a mock result_only token
        class MockResultToken:
            def __init__(self):
                self.kind = "RESULT_ONLY"
                self.value = "hello"
                self.lineno = 2
                self.result = "hello"
                self.original = "Résultat: hello"
        
        tokens = [MockStepToken(), MockResultToken()]
        ast = builder.build(tokens)
        
        assert len(ast.steps) == 1
        assert len(ast.steps[0].actions) == 1
        assert ast.steps[0].actions[0].command is None
        assert ast.steps[0].actions[0].result_expr == "hello"
    
    def test_build_with_path(self):
        """Test building AST with file path."""
        builder = DefaultASTBuilder()
        tokens = []
        ast = builder.build(tokens, path="/test/path.shtest")
        
        assert ast.path == "/test/path.shtest"


class TestDefaultGrammar:
    """Test the DefaultGrammar class."""
    
    def test_default_grammar_creation(self):
        """Test default grammar creation."""
        grammar = DefaultGrammar()
        assert grammar is not None
    
    def test_match_passes_through_tokens(self):
        """Test that default grammar passes tokens through unchanged."""
        grammar = DefaultGrammar()
        
        # Create mock tokens
        class MockToken:
            def __init__(self, kind, value):
                self.kind = kind
                self.value = value
                self.lineno = 1
                self.result = None
                self.original = value
        
        tokens = [MockToken("STEP", "Test"), MockToken("ACTION", "echo")]
        result = grammar.match(tokens)
        
        assert result == tokens


class TestConfigurableParser:
    """Test the ConfigurableParser class."""
    
    def test_configurable_parser_creation(self):
        """Test configurable parser creation."""
        parser = ConfigurableParser()
        assert parser.lexer is not None
        assert parser.grammar is not None
        assert parser.ast_builder is not None
        assert parser.debug is False
    
    def test_configurable_parser_with_custom_components(self):
        """Test configurable parser with custom components."""
        lexer = ConfigurableLexer()
        grammar = DefaultGrammar()
        ast_builder = DefaultASTBuilder()
        
        parser = ConfigurableParser(
            lexer=lexer,
            grammar=grammar,
            ast_builder=ast_builder,
            debug=True
        )
        
        assert parser.lexer == lexer
        assert parser.grammar == grammar
        assert parser.ast_builder == ast_builder
        assert parser.debug is True
    
    def test_parse_simple_text(self):
        """Test parsing simple text."""
        parser = ConfigurableParser()
        text = "Step: Test\nAction: echo hello"
        
        ast = parser.parse(text)
        
        assert isinstance(ast, ShtestFile)
        assert len(ast.steps) == 1
        assert ast.steps[0].name == "Test"
        assert len(ast.steps[0].actions) == 1
        assert ast.steps[0].actions[0].command == "echo hello"
    
    def test_parse_with_path(self):
        """Test parsing with file path."""
        parser = ConfigurableParser()
        text = "Step: Test"
        
        ast = parser.parse(text, path="/test/path.shtest")
        
        assert ast.path == "/test/path.shtest"
    
    def test_parse_file(self):
        """Test parsing a file."""
        parser = ConfigurableParser()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.shtest') as f:
            f.write("Step: Test\nAction: echo hello")
            temp_file = f.name
        
        try:
            ast = parser.parse_file(temp_file)
            
            assert isinstance(ast, ShtestFile)
            assert ast.path == temp_file
            assert len(ast.steps) == 1
            assert ast.steps[0].name == "Test"
        finally:
            os.unlink(temp_file)
    
    def test_parse_file_not_found(self):
        """Test parsing non-existent file."""
        parser = ConfigurableParser()
        
        with pytest.raises(ParseError, match="Parser error in file"):
            parser.parse_file("nonexistent.shtest")
    
    def test_parse_debug_mode(self):
        """Test parsing in debug mode."""
        parser = ConfigurableParser(debug=True)
        text = "Step: Test\nAction: echo hello"
        
        # Should not raise an exception
        ast = parser.parse(text)
        assert isinstance(ast, ShtestFile)


class TestBackwardCompatibility:
    """Test backward compatibility with the old parser interface."""
    
    def test_old_parser_interface(self):
        """Test that the old parser interface still works."""
        from shtest_compiler.parser.parser import Parser
        
        parser = Parser()
        text = "Step: Test\nAction: echo hello"
        
        ast = parser.parse(text)
        
        assert isinstance(ast, ShtestFile)
        assert len(ast.steps) == 1
        assert ast.steps[0].name == "Test"
        assert len(ast.steps[0].actions) == 1
        assert ast.steps[0].actions[0].command == "echo hello"
    
    def test_old_parser_with_legacy_rules(self):
        """Test that legacy rule matching still works."""
        from shtest_compiler.parser.parser import Parser
        
        parser = Parser()
        text = "Step: Test\nAction: echo hello ; Résultat: hello"
        
        ast = parser.parse(text)
        
        assert isinstance(ast, ShtestFile)
        # Legacy rules should still be applied
        assert hasattr(parser, 'rules')


class TestIntegration:
    """Test integration between parser components."""
    
    def test_full_parsing_pipeline(self):
        """Test the complete parsing pipeline."""
        parser = ConfigurableParser(debug=True)
        text = """
Step: Preparation
Action: mkdir test_dir ; Résultat: directory created
Action: echo "hello world"
Step: Execution
Action: ls test_dir ; Résultat: files listed
"""
        
        ast = parser.parse(text)
        
        assert isinstance(ast, ShtestFile)
        assert len(ast.steps) == 2
        
        # Check first step
        assert ast.steps[0].name == "Preparation"
        assert len(ast.steps[0].actions) == 2
        assert ast.steps[0].actions[0].command == "mkdir test_dir"
        assert ast.steps[0].actions[0].result_expr == "directory created"
        assert ast.steps[0].actions[1].command == 'echo "hello world"'
        
        # Check second step
        assert ast.steps[1].name == "Execution"
        assert len(ast.steps[1].actions) == 1
        assert ast.steps[1].actions[0].command == "ls test_dir"
        assert ast.steps[1].actions[0].result_expr == "files listed" 