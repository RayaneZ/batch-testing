#!/usr/bin/env python3
"""
Test for basic parser functionality.
Converted from simple_test.py to proper pytest format.
"""

import pytest
from shtest_compiler.parser.configurable_parser import ConfigurableParser


class TestSimpleParser:
    """Test basic parser functionality."""
    
    def test_parser_import(self):
        """Test that the parser can be imported successfully."""
        # This test verifies the import works
        assert ConfigurableParser is not None
    
    def test_parser_creation(self):
        """Test that a parser instance can be created."""
        parser = ConfigurableParser(debug=False)
        assert parser is not None
        assert hasattr(parser, 'parse')
    
    def test_simple_parse(self):
        """Test parsing simple content."""
        parser = ConfigurableParser(debug=False)
        content = "Étape: Test\nAction: echo 'test'\nRésultat: stdout contient 'test'"
        
        # This should not raise an exception
        result = parser.parse(content, path="test.shtest")
        assert result is not None
    
    def test_parser_with_debug(self):
        """Test parser with debug mode enabled."""
        parser = ConfigurableParser(debug=True)
        content = "Étape: Test\nAction: echo 'test'"
        
        # This should not raise an exception
        result = parser.parse(content, path="test_debug.shtest")
        assert result is not None
    
    def test_empty_content(self):
        """Test parser with empty content."""
        parser = ConfigurableParser(debug=False)
        content = ""
        
        # This should handle empty content gracefully
        result = parser.parse(content, path="empty_test.shtest")
        assert result is not None
    
    def test_minimal_content(self):
        """Test parser with minimal valid content."""
        parser = ConfigurableParser(debug=False)
        content = "Étape: Test"
        
        # This should parse successfully
        result = parser.parse(content, path="minimal_test.shtest")
        assert result is not None 