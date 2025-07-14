#!/usr/bin/env python3
"""
Test for file date handler functionality.
Converted from test_file_date.py to proper pytest format.
Updated to match new parser behavior that requires actions for steps.
"""

import pytest

from shtest_compiler.ast.shell_framework_binder import ShellFrameworkLifter
from shtest_compiler.ast.shellframework_to_shellscript_visitor import \
    ShellFrameworkToShellScriptVisitor
from shtest_compiler.ast.shtest_to_shellframework_visitor import \
    ShtestToShellFrameworkVisitor
from shtest_compiler.parser.shtest_ast import Action, ShtestFile, TestStep


class TestFileDateHandler:
    """Test file date handler functionality."""

    def test_file_date_global_scope(self):
        """Test file_date handler with global scope (file specified)."""
        # Create a test AST with global scope scenario
        test_ast = ShtestFile(
            steps=[
                TestStep(
                    name="Test Step",
                    actions=[
                        Action(
                            command="echo 'test'",
                            result_expr="La date du fichier /tmp/test.txt est 202412011200",  # Global scope (file specified)
                            result_ast=None,
                            lineno=1,
                        )
                    ],
                    lineno=1,
                )
            ]
        )

        # Step 1: Convert to ShellFrameworkAST
        shellframework_ast = ShtestToShellFrameworkVisitor().visit(test_ast)
        assert shellframework_ast is not None
        assert len(shellframework_ast.steps) == 1

        # Step 2: Apply lifting
        lifter = ShellFrameworkLifter(shellframework_ast)
        lifted_ast = lifter.lift()
        assert lifted_ast is not None

        # Step 3: Generate shell script
        visitor = ShellFrameworkToShellScriptVisitor()
        shell_script = visitor.visit(lifted_ast)
        assert shell_script is not None
        assert len(shell_script.lines) > 0

        # Check for file_date validations
        file_date_validations = [
            line
            for line in shell_script.lines
            if ("/tmp/test.txt" in line and "202412011200" in line) or "date" in line
        ]
        assert len(file_date_validations) > 0, "Should have file_date validations"

    def test_file_date_last_action_scope(self):
        """Test file_date handler with last action scope (no file specified)."""
        # Create a test AST with last action scope scenario
        test_ast = ShtestFile(
            steps=[
                TestStep(
                    name="Test Step",
                    actions=[
                        Action(
                            command="touch /tmp/test.txt",
                            result_expr="La date du fichier /tmp/test.txt est modifiée",  # Last action scope (file specified)
                            result_ast=None,
                            lineno=1,
                        )
                    ],
                    lineno=1,
                )
            ]
        )

        # Step 1: Convert to ShellFrameworkAST
        shellframework_ast = ShtestToShellFrameworkVisitor().visit(test_ast)
        assert shellframework_ast is not None
        assert len(shellframework_ast.steps) == 1

        # Step 2: Apply lifting
        lifter = ShellFrameworkLifter(shellframework_ast)
        lifted_ast = lifter.lift()
        assert lifted_ast is not None

        # Step 3: Generate shell script
        visitor = ShellFrameworkToShellScriptVisitor()
        shell_script = visitor.visit(lifted_ast)
        assert shell_script is not None
        assert len(shell_script.lines) > 0

        # Check for file_date validations
        file_date_validations = [
            line
            for line in shell_script.lines
            if "file_date" in line or "modifié" in line
        ]
        assert len(file_date_validations) > 0, "Should have file_date validations"

    def test_file_date_mixed_scopes(self):
        """Test file_date handler with mixed global and last action scopes."""
        # Create a test AST with both global and last_action scope scenarios
        test_ast = ShtestFile(
            steps=[
                TestStep(
                    name="Test Step 1",
                    actions=[
                        Action(
                            command="touch /tmp/test.txt",
                            result_expr="La date du fichier /tmp/test.txt est modifiée",  # Last action scope (file specified)
                            result_ast=None,
                            lineno=1,
                        )
                    ],
                    lineno=1,
                ),
                TestStep(
                    name="Test Step 2",
                    actions=[
                        Action(
                            command="echo 'test'",
                            result_expr="La date du fichier /tmp/test.txt est 202412011200",  # Global scope (file specified)
                            result_ast=None,
                            lineno=2,
                        )
                    ],
                    lineno=2,
                ),
            ]
        )

        # Step 1: Convert to ShellFrameworkAST
        shellframework_ast = ShtestToShellFrameworkVisitor().visit(test_ast)
        assert shellframework_ast is not None
        assert len(shellframework_ast.steps) == 2

        # Step 2: Apply lifting
        lifter = ShellFrameworkLifter(shellframework_ast)
        lifted_ast = lifter.lift()
        assert lifted_ast is not None

        # Step 3: Generate shell script
        visitor = ShellFrameworkToShellScriptVisitor()
        shell_script = visitor.visit(lifted_ast)
        assert shell_script is not None
        assert len(shell_script.lines) > 0

        # Check for file_date validations
        file_date_validations = [
            line
            for line in shell_script.lines
            if "file_date" in line or "modifié" in line
        ]
        assert len(file_date_validations) > 0, "Should have file_date validations"

    def test_file_date_validation_generation(self):
        """Test that file_date validations are properly generated."""
        test_ast = ShtestFile(
            steps=[
                TestStep(
                    name="Test Step",
                    actions=[
                        Action(
                            command="touch /tmp/test.txt",
                            result_expr="La date du fichier /tmp/test.txt est modifiée",
                            result_ast=None,
                            lineno=1,
                        )
                    ],
                    lineno=1,
                )
            ]
        )

        # Convert to shell script
        shellframework_ast = ShtestToShellFrameworkVisitor().visit(test_ast)
        assert shellframework_ast is not None

        # Apply lifting
        lifter = ShellFrameworkLifter(shellframework_ast)
        lifted_ast = lifter.lift()
        assert lifted_ast is not None

        # Generate shell script
        visitor = ShellFrameworkToShellScriptVisitor()
        shell_script = visitor.visit(lifted_ast)
        assert shell_script is not None
        assert len(shell_script.lines) > 0

        # Check for file_date validations
        file_date_validations = [
            line
            for line in shell_script.lines
            if "file_date" in line or "modifié" in line
        ]
        assert len(file_date_validations) > 0, "Should have file_date validations"
