#!/usr/bin/env python3
"""
Test for lifting functionality.
Converted from test_lifting.py to proper pytest format.
"""

import pytest
from shtest_compiler.parser.shtest_ast import ShtestFile, TestStep, Action
from shtest_compiler.ast.shtest_to_shellframework_visitor import (
    ShtestToShellFrameworkVisitor,
)
from shtest_compiler.ast.shell_framework_binder import ShellFrameworkLifter
from shtest_compiler.ast.shellframework_to_shellscript_visitor import (
    ShellFrameworkToShellScriptVisitor,
)
from shtest_compiler.ast.shell_framework_ast import InlineShellCode


class TestLiftingFunctionality:
    """Test lifting functionality."""

    def test_lifting_with_mixed_validations(self):
        """Test lifting with mixed global and local validations."""
        # Create a test AST with mixed global and local validations
        test_ast = ShtestFile(
            steps=[
                TestStep(
                    name="Test Step",
                    actions=[
                        Action(
                            command="Executer le script a.sh avec les paramètres a=1",
                            result_expr="Le fichier /tmp/test.txt est présent",
                            result_ast=None,
                            lineno=1,
                        ),
                        Action(
                            command="Executer le script b.sh",
                            result_expr="Le fichier /tmp/test.txt est vide",
                            result_ast=None,
                            lineno=2,
                        ),
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

        # Verify the generated script contains expected patterns
        script_text = "\n".join(shell_script.lines)
        assert "existe" in script_text, "Should contain file existence validation"
        assert "vide" in script_text, "Should contain file_empty validation"

    def test_lifting_validation_scopes(self):
        """Test that lifting properly handles validation scopes."""
        test_ast = ShtestFile(
            steps=[
                TestStep(
                    name="Test Step",
                    actions=[
                        Action(
                            command="touch /tmp/test.txt",
                            result_expr="Le fichier /tmp/test.txt est présent",  # Global scope (file specified)
                            result_ast=None,
                            lineno=1,
                        ),
                        Action(
                            command="echo 'test'",
                            result_expr="Le fichier /tmp/test.txt est vide",  # Global scope (file specified)
                            result_ast=None,
                            lineno=2,
                        ),
                    ],
                    lineno=1,
                )
            ]
        )

        # Convert to ShellFrameworkAST
        shellframework_ast = ShtestToShellFrameworkVisitor().visit(test_ast)
        assert shellframework_ast is not None
        assert len(shellframework_ast.steps) == 1

        # Apply lifting
        lifter = ShellFrameworkLifter(shellframework_ast)
        lifted_ast = lifter.lift()
        assert lifted_ast is not None

        # Generate shell script
        visitor = ShellFrameworkToShellScriptVisitor()
        shell_script = visitor.visit(lifted_ast)
        assert shell_script is not None
        assert len(shell_script.lines) > 0

        # Verify the generated script contains expected patterns
        script_text = "\n".join(shell_script.lines)
        assert "existe" in script_text, "Should contain file existence validation"
        assert "vide" in script_text, "Should contain file_empty validation"

    def test_lifting_inline_shell_code(self):
        """Test that lifting properly handles InlineShellCode."""
        test_ast = ShtestFile(
            steps=[
                TestStep(
                    name="Test Step",
                    actions=[
                        Action(
                            command="echo 'test'",
                            result_expr="stdout contient 'test'",
                            result_ast=None,
                            lineno=1,
                        )
                    ],
                    lineno=1,
                )
            ]
        )

        # Convert to ShellFrameworkAST
        shellframework_ast = ShtestToShellFrameworkVisitor().visit(test_ast)
        lifter = ShellFrameworkLifter(shellframework_ast)
        lifted_ast = lifter.lift()

        # Verify InlineShellCode is preserved
        inline_actions = [
            action
            for action in lifted_ast.steps[0].actions
            if isinstance(action, InlineShellCode)
        ]
        assert len(inline_actions) > 0, "Should preserve InlineShellCode"

        # Verify code lines are present
        for action in inline_actions:
            assert hasattr(
                action, "code_lines"
            ), "InlineShellCode should have code_lines"
            assert len(action.code_lines) > 0, "Should have code lines"

    def test_lifting_multiple_steps(self):
        """Test lifting with multiple steps."""
        test_ast = ShtestFile(
            steps=[
                TestStep(
                    name="Step 1",
                    actions=[
                        Action(
                            command="touch /tmp/file1.txt",
                            result_expr="Le fichier /tmp/file1.txt est présent",
                            result_ast=None,
                            lineno=1,
                        )
                    ],
                    lineno=1,
                ),
                TestStep(
                    name="Step 2",
                    actions=[
                        Action(
                            command="touch /tmp/file2.txt",
                            result_expr="Le fichier /tmp/file2.txt est présent",
                            result_ast=None,
                            lineno=2,
                        )
                    ],
                    lineno=2,
                ),
            ]
        )

        # Convert to ShellFrameworkAST
        shellframework_ast = ShtestToShellFrameworkVisitor().visit(test_ast)
        assert shellframework_ast is not None
        assert len(shellframework_ast.steps) == 2

        # Apply lifting
        lifter = ShellFrameworkLifter(shellframework_ast)
        lifted_ast = lifter.lift()
        assert lifted_ast is not None

        # Generate shell script
        visitor = ShellFrameworkToShellScriptVisitor()
        shell_script = visitor.visit(lifted_ast)
        assert shell_script is not None
        assert len(shell_script.lines) > 0

        # Verify the generated script contains expected patterns
        script_text = "\n".join(shell_script.lines)
        assert "existe" in script_text, "Should contain file existence validation"
        assert "file1.txt" in script_text, "Should contain file1.txt"
        assert "file2.txt" in script_text, "Should contain file2.txt"

    def test_lifting_empty_actions(self):
        """Test lifting with empty actions."""
        test_ast = ShtestFile(steps=[TestStep(name="Test Step", actions=[], lineno=1)])

        # Convert to ShellFrameworkAST
        shellframework_ast = ShtestToShellFrameworkVisitor().visit(test_ast)
        lifter = ShellFrameworkLifter(shellframework_ast)
        lifted_ast = lifter.lift()

        # Verify empty step is handled gracefully
        assert len(lifted_ast.steps) == 1
        assert len(lifted_ast.steps[0].actions) == 0
