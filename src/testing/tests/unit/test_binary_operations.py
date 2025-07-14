#!/usr/bin/env python3
"""
Test for binary operations system.
Converted from test_binaryop.py to proper pytest format.
"""

import pytest

from shtest_compiler.ast.shellframework_to_shellscript_visitor import \
    ShellFrameworkToShellScriptVisitor
from shtest_compiler.parser.shunting_yard import (Atomic, BinaryOp,
                                                  parse_validation_expression)


class TestBinaryOperations:
    """Test binary operations system."""

    def test_simple_validation_wrapping(self):
        """Test that simple validations are wrapped in BinaryOp with true."""
        # Test simple validation (should be wrapped in BinaryOp with true)
        ast = parse_validation_expression("Le fichier /tmp/test.txt est présent")

        # Verify it's a BinaryOp
        assert isinstance(ast, BinaryOp), f"Expected BinaryOp, got {type(ast)}"

        # Verify the structure
        assert ast.op == "et", "Should use 'et' operator"
        assert isinstance(ast.left, Atomic), "Left should be Atomic"
        assert isinstance(ast.right, Atomic), "Right should be Atomic"

        # Verify the content
        assert (
            ast.left.value == "Le fichier /tmp/test.txt est présent"
        ), f"Left should be 'Le fichier /tmp/test.txt est présent', got {ast.left.value}"
        assert (
            ast.right.value == "true"
        ), f"Right should be 'true', got {ast.right.value}"

    def test_compound_validation(self):
        """Test compound validation with multiple conditions."""
        # Test compound validation
        ast = parse_validation_expression(
            "Le fichier /tmp/test.txt est présent et Le fichier /tmp/test.txt est vide"
        )

        # Verify it's a BinaryOp
        assert isinstance(ast, BinaryOp), f"Expected BinaryOp, got {type(ast)}"

        # Verify the structure
        assert ast.op == "et", "Should use 'et' operator"

        # Verify left and right are Atomic
        assert isinstance(ast.left, Atomic), "Left should be Atomic"
        assert isinstance(ast.right, Atomic), "Right should be Atomic"

        # Verify the content
        assert (
            ast.left.value == "Le fichier /tmp/test.txt est présent"
        ), f"Left should be 'Le fichier /tmp/test.txt est présent', got {ast.left.value}"
        assert (
            ast.right.value == "Le fichier /tmp/test.txt est vide"
        ), f"Right should be 'Le fichier /tmp/test.txt est vide', got {ast.right.value}"

    def test_simple_validation_shell_generation(self):
        """Test shell code generation for simple validation."""
        # Create simple validation AST
        ast = parse_validation_expression("Le fichier /tmp/test.txt est présent")

        # Generate shell code
        visitor = ShellFrameworkToShellScriptVisitor()
        shell_lines = visitor.visit(ast)

        # Verify shell code is generated
        assert isinstance(shell_lines, list), "Should return list of shell lines"
        assert len(shell_lines) > 0, "Should generate shell code"

        # Verify the generated code contains expected patterns
        shell_text = "\n".join(shell_lines)
        assert "fichier" in shell_text, "Should contain 'fichier'"
        assert (
            "present" in shell_text or "présent" in shell_text or "existe" in shell_text
        ), "Should contain 'present', 'présent', or 'existe'"

    def test_compound_validation_shell_generation(self):
        """Test shell code generation for compound validation."""
        # Create compound validation AST
        ast = parse_validation_expression(
            "Le fichier /tmp/test.txt est présent et Le fichier /tmp/test.txt est vide"
        )

        # Generate shell code
        visitor = ShellFrameworkToShellScriptVisitor()
        shell_lines = visitor.visit(ast)

        # Verify shell code is generated
        assert isinstance(shell_lines, list), "Should return list of shell lines"
        assert len(shell_lines) > 0, "Should generate shell code"

        # Verify the generated code contains expected patterns
        shell_text = "\n".join(shell_lines)
        assert "fichier" in shell_text, "Should contain 'fichier'"
        assert (
            "present" in shell_text or "présent" in shell_text or "existe" in shell_text
        ), "Should contain 'present', 'présent', or 'existe'"
        assert "vide" in shell_text, "Should contain 'vide'"
        assert (
            "&&" in shell_text or "and" in shell_text
        ), "Should contain logical operator"

    def test_complex_validation_expression(self):
        """Test complex validation expression with multiple operators."""
        # Test more complex expression
        ast = parse_validation_expression(
            "Le fichier /tmp/test.txt est présent et Le fichier /tmp/test.txt est vide ou stdout contient 'test'"
        )

        # Verify it's a BinaryOp
        assert isinstance(ast, BinaryOp), f"Expected BinaryOp, got {type(ast)}"

        # Verify the structure
        assert ast.op in ["et", "ou"], f"Should use 'et' or 'ou' operator, got {ast.op}"

        # Verify left and right are properly structured
        assert isinstance(
            ast.left, (Atomic, BinaryOp)
        ), "Left should be Atomic or BinaryOp"
        assert isinstance(
            ast.right, (Atomic, BinaryOp)
        ), "Right should be Atomic or BinaryOp"

    def test_validation_with_quotes(self):
        """Test validation expression with quoted strings."""
        # Test validation with quoted content
        ast = parse_validation_expression("stdout contient 'hello world'")

        # Verify it's a BinaryOp
        assert isinstance(ast, BinaryOp), f"Expected BinaryOp, got {type(ast)}"

        # Verify the structure
        assert ast.op == "et", "Should use 'et' operator"
        assert isinstance(ast.left, Atomic), "Left should be Atomic"
        assert isinstance(ast.right, Atomic), "Right should be Atomic"

        # Verify quoted content is preserved
        assert (
            "'hello world'" in ast.left.value or "'hello world'" in ast.right.value
        ), "Quoted content should be preserved"

    def test_empty_validation_expression(self):
        """Test handling of empty validation expression."""
        # Test empty expression
        import pytest
        with pytest.raises(ValueError, match="Validation expression is empty"):
            parse_validation_expression("")

    def test_single_word_validation(self):
        """Test single word validation expression."""
        # Test single word
        ast = parse_validation_expression("present")

        # Should be wrapped in BinaryOp
        assert isinstance(ast, BinaryOp), f"Expected BinaryOp, got {type(ast)}"
        assert ast.op == "et", "Should use 'et' operator"
        assert isinstance(ast.left, Atomic), "Left should be Atomic"
        assert isinstance(ast.right, Atomic), "Right should be Atomic"
        assert (
            ast.left.value == "present"
        ), f"Left should be 'present', got {ast.left.value}"
        assert (
            ast.right.value == "true"
        ), f"Right should be 'true', got {ast.right.value}"
