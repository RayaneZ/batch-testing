"""
Comprehensive tests for the modular system.

This module tests all components of the new modular architecture:
- Enhanced grammar system
- Enhanced AST builder system
- Compiler integration
- Plugin system
"""

import pytest
import tempfile
import os
from pathlib import Path

from shtest_compiler.parser import (
    ConfigurableParser, grammar_registry, ast_builder_registry,
    GrammarRule, DefaultGrammar, CustomGrammar, DefaultASTBuilder, CustomASTBuilder
)
from shtest_compiler.compiler.compiler import ModularCompiler
from shtest_compiler.plugins import (
    Plugin, GrammarPlugin, ASTBuilderPlugin, MatcherPlugin,
    PluginRegistry, plugin_registry
)
from shtest_compiler.parser.shtest_ast import ShtestFile, Action, TestStep
from shtest_compiler.parser.lexer import Token, TokenType


class TestEnhancedGrammar:
    """Test the enhanced grammar system."""
    
    def test_grammar_rule_creation(self):
        """Test creating grammar rules."""
        def test_handler(tokens):
            return tokens
        
        rule = GrammarRule("test", "pattern", test_handler, priority=10)
        assert rule.name == "test"
        assert rule.pattern == "pattern"
        assert rule.handler == test_handler
        assert rule.priority == 10
    
    def test_grammar_transformer(self):
        """Test the grammar transformer."""
        from shtest_compiler.parser.grammar import GrammarTransformer
        
        transformer = GrammarTransformer()
        
        def test_handler(tokens):
            return tokens
        
        rule = GrammarRule("test", "pattern", test_handler)
        transformer.add_rule(rule)
        
        assert len(transformer.rules) == 1
        assert transformer.rules[0] == rule
    
    def test_default_grammar_with_rules(self):
        """Test default grammar with custom rules."""
        grammar = DefaultGrammar()
        
        def test_handler(tokens):
            # Add a test token
            test_token = Token(TokenType.TEXT, "test", 1, None, "test")
            tokens.append(test_token)
            return tokens
        
        rule = GrammarRule("test_rule", ".*", test_handler)
        grammar.add_rule(rule)
        
        # Create test tokens
        tokens = [Token(TokenType.STEP, "Test", 1, None, "Step: Test")]
        
        result = grammar.match(tokens)
        
        assert len(result) == 2  # Original + test token
        assert result[1].type == TokenType.TEXT
    
    def test_custom_grammar(self):
        """Test custom grammar with specific rules."""
        def test_handler(tokens):
            return tokens
        
        rule = GrammarRule("test", ".*", test_handler)
        grammar = CustomGrammar([rule])
        
        assert len(grammar.get_rules()) == 1
        assert grammar.get_rules()[0] == rule


class TestEnhancedASTBuilder:
    """Test the enhanced AST builder system."""
    
    def test_ast_validator(self):
        """Test the AST validator."""
        from shtest_compiler.parser.ast_builder import ASTValidator
        
        validator = ASTValidator()
        
        def test_validator(ast):
            if len(ast.steps) == 0:
                return ["No steps found"]
            return []
        
        validator.add_validator(test_validator)
        
        # Test with empty AST
        ast = ShtestFile()
        errors = validator.validate(ast)
        assert len(errors) == 1
        assert "No steps found" in errors[0]
        
        # Test with valid AST
        ast.add_step("Test", 1)
        errors = validator.validate(ast)
        assert len(errors) == 0
    
    def test_ast_transformer(self):
        """Test the AST transformer."""
        from shtest_compiler.parser.ast_builder import ASTTransformer
        
        transformer = ASTTransformer()
        
        def test_transformer(ast):
            # Add a default step if none exists
            if len(ast.steps) == 0:
                ast.add_step("Default Step", 1)
            return ast
        
        transformer.add_transformer(test_transformer)
        
        ast = ShtestFile()
        result = transformer.transform(ast)
        
        assert len(result.steps) == 1
        assert result.steps[0].name == "Default Step"
    
    def test_default_ast_builder_validation(self):
        """Test default AST builder with validation."""
        builder = DefaultASTBuilder()
        
        # Create test tokens
        tokens = [Token(TokenType.STEP, "Test", 1, None, "Step: Test")]
        
        ast = builder.build(tokens)
        
        # Should have validation warnings for empty step
        assert len(ast.steps) == 1
        assert ast.steps[0].name == "Test"
    
    def test_custom_ast_builder(self):
        """Test custom AST builder with specific validators and transformers."""
        def test_validator(ast):
            return []
        
        def test_transformer(ast):
            return ast
        
        builder = CustomASTBuilder(
            validators=[test_validator],
            transformers=[test_transformer]
        )
        
        tokens = [Token(TokenType.STEP, "Test", 1, None, "Step: Test")]
        
        ast = builder.build(tokens)
        assert len(ast.steps) == 1


class TestGrammarRegistry:
    """Test the grammar registry system."""
    
    def test_grammar_registry_operations(self):
        """Test basic grammar registry operations."""
        # Test registration
        grammar_registry.register("test_grammar", CustomGrammar)
        
        # Test listing
        grammars = grammar_registry.list()
        assert "test_grammar" in grammars
        
        # Test creation
        grammar = grammar_registry.create("test_grammar")
        assert isinstance(grammar, CustomGrammar)
        
        # Test getting
        grammar_class = grammar_registry.get("test_grammar")
        assert grammar_class == CustomGrammar
    
    def test_grammar_registry_errors(self):
        """Test grammar registry error handling."""
        # Test getting non-existent grammar
        with pytest.raises(KeyError):
            grammar_registry.get("non_existent")
        
        # Test creating non-existent grammar
        with pytest.raises(KeyError):
            grammar_registry.create("non_existent")


class TestASTBuilderRegistry:
    """Test the AST builder registry system."""
    
    def test_ast_builder_registry_operations(self):
        """Test basic AST builder registry operations."""
        # Test registration
        ast_builder_registry.register("test_builder", CustomASTBuilder)
        
        # Test listing
        builders = ast_builder_registry.list()
        assert "test_builder" in builders
        
        # Test creation
        builder = ast_builder_registry.create("test_builder")
        assert isinstance(builder, CustomASTBuilder)
        
        # Test getting
        builder_class = ast_builder_registry.get("test_builder")
        assert builder_class == CustomASTBuilder


class TestModularCompiler:
    """Test the modular compiler integration."""
    
    def test_modular_compiler_creation(self):
        """Test creating a modular compiler."""
        compiler = ModularCompiler(
            grammar_name="default",
            ast_builder_name="default",
            debug=True
        )
        
        assert compiler.grammar_name == "default"
        assert compiler.ast_builder_name == "default"
        assert compiler.debug is True
        assert compiler.parser is not None
    
    def test_modular_compiler_compile_text(self):
        """Test compiling text with modular compiler."""
        compiler = ModularCompiler(debug=True)
        
        text = "Step: Test\nAction: echo hello"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as f:
            output_path = f.name
        
        try:
            result_path = compiler.compile_text(text, output_path)
            
            assert result_path == output_path
            assert os.path.exists(result_path)
            
            # Check that the file contains shell script content
            with open(result_path, 'r') as f:
                content = f.read()
                assert "#!/bin/sh" in content
                assert "echo hello" in content
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_modular_compiler_compile_file(self):
        """Test compiling file with modular compiler."""
        compiler = ModularCompiler(debug=True)
        
        # Create a test .shtest file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.shtest') as f:
            f.write("Step: Test\nAction: echo hello")
            input_path = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as f:
            output_path = f.name
        
        try:
            result_path = compiler.compile_file(input_path, output_path)
            
            assert result_path == output_path
            assert os.path.exists(result_path)
        finally:
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_modular_compiler_component_switching(self):
        """Test switching grammars and AST builders."""
        compiler = ModularCompiler()
        
        # Test switching grammar
        compiler.set_grammar("default")
        assert compiler.grammar_name == "default"
        
        # Test switching AST builder
        compiler.set_ast_builder("default")
        assert compiler.ast_builder_name == "default"
    
    def test_modular_compiler_info(self):
        """Test getting compiler information."""
        compiler = ModularCompiler()
        info = compiler.get_parser_info()
        
        assert "grammar" in info
        assert "ast_builder" in info
        assert "debug" in info
        assert "available_grammars" in info
        assert "available_ast_builders" in info


class TestPluginSystem:
    """Test the plugin system."""
    
    def test_plugin_base_class(self):
        """Test the base plugin class."""
        class TestPlugin(Plugin):
            def install(self, registry):
                pass
            
            def uninstall(self, registry):
                pass
        
        plugin = TestPlugin("test", "1.0.0")
        assert plugin.name == "test"
        assert plugin.version == "1.0.0"
    
    def test_grammar_plugin(self):
        """Test grammar plugin."""
        plugin = GrammarPlugin("test_grammar", CustomGrammar)
        assert plugin.name == "test_grammar"
        assert plugin.grammar_class == CustomGrammar
    
    def test_ast_builder_plugin(self):
        """Test AST builder plugin."""
        plugin = ASTBuilderPlugin("test_builder", CustomASTBuilder)
        assert plugin.name == "test_builder"
        assert plugin.builder_class == CustomASTBuilder
    
    def test_plugin_registry(self):
        """Test plugin registry operations."""
        registry = PluginRegistry()
        
        class TestPlugin(Plugin):
            def install(self, registry):
                pass
            
            def uninstall(self, registry):
                pass
        
        plugin = TestPlugin("test")
        
        # Test registration
        registry.register(plugin)
        assert "test" in registry.list()
        
        # Test getting
        retrieved_plugin = registry.get("test")
        assert retrieved_plugin == plugin
        
        # Test unregistration
        registry.unregister("test")
        assert "test" not in registry.list()
    
    def test_plugin_loading_from_file(self):
        """Test loading plugins from files."""
        # Create a temporary plugin file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("""
from shtest_compiler.plugins import Plugin

class TestFilePlugin(Plugin):
    def __init__(self):
        super().__init__("test_file_plugin", "1.0.0")
    
    def install(self, registry):
        pass
    
    def uninstall(self, registry):
        pass
""")
            plugin_file = f.name
        
        try:
            registry = PluginRegistry()
            plugin = registry.load_from_file(plugin_file)
            
            assert plugin.name == "test_file_plugin"
            assert "test_file_plugin" in registry.list()
        finally:
            if os.path.exists(plugin_file):
                os.unlink(plugin_file)


class TestIntegration:
    """Test integration between all components."""
    
    def test_full_pipeline_with_custom_components(self):
        """Test the full pipeline with custom grammar and AST builder."""
        # Create custom grammar
        def custom_handler(tokens):
            return tokens
        
        rule = GrammarRule("custom", ".*", custom_handler)
        grammar = CustomGrammar([rule])
        
        # Create custom AST builder
        def custom_validator(ast):
            return []
        
        def custom_transformer(ast):
            return ast
        
        builder = CustomASTBuilder(
            validators=[custom_validator],
            transformers=[custom_transformer]
        )
        
        # Create parser with custom components
        parser = ConfigurableParser(
            grammar=grammar,
            ast_builder=builder,
            debug=True
        )
        
        # Test parsing
        text = "Step: Test\nAction: echo hello"
        ast = parser.parse(text)
        
        assert len(ast.steps) == 1
        assert ast.steps[0].name == "Test"
        assert len(ast.steps[0].actions) == 1
        assert ast.steps[0].actions[0].command == "echo hello"
    
    def test_plugin_integration(self):
        """Test plugin integration with the compiler."""
        # Create a custom grammar plugin
        plugin = GrammarPlugin("test_grammar", CustomGrammar)
        
        # Create compiler
        compiler = ModularCompiler()
        
        # Install plugin
        plugin.install(compiler)
        
        # Verify plugin was installed
        assert "test_grammar" in compiler.list_grammars()
        
        # Test using the custom grammar
        compiler.set_grammar("test_grammar")
        assert compiler.grammar_name == "test_grammar" 