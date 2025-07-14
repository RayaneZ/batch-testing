#!/usr/bin/env python3
"""
Test for file date handler functionality.
"""

from shtest_compiler.parser.shtest_ast import ShtestFile, TestStep, Action
from shtest_compiler.ast.shtest_to_shellframework_visitor import (
    ShtestToShellFrameworkVisitor,
)
from shtest_compiler.ast.shell_framework_binder import ShellFrameworkLifter
from shtest_compiler.ast.shellframework_to_shellscript_visitor import (
    ShellFrameworkToShellScriptVisitor,
)


def test_file_date():
    print("=== Testing File Date Handler ===\n")

    # Create a test AST with file date validation
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

    print("Test AST created successfully")
    print(f"Steps: {len(test_ast.steps)}")
    print(f"Actions in first step: {len(test_ast.steps[0].actions)}")
    print()

    # Step 1: Convert to ShellFrameworkAST
    print("Step 1: Converting to ShellFrameworkAST")
    shellframework_ast = ShtestToShellFrameworkVisitor().visit(test_ast)
    print(f"ShellFrameworkAST created: {shellframework_ast is not None}")
    print(f"Steps in ShellFrameworkAST: {len(shellframework_ast.steps)}")
    print()

    # Step 2: Apply lifting
    print("Step 2: Applying lifting")
    lifter = ShellFrameworkLifter(shellframework_ast)
    lifted_ast = lifter.lift()
    print(f"Lifted AST created: {lifted_ast is not None}")
    print(f"Steps in lifted AST: {len(lifted_ast.steps)}")
    print()

    # Step 3: Generate shell script
    print("Step 3: Generating shell script")
    visitor = ShellFrameworkToShellScriptVisitor()
    shell_script = visitor.visit(lifted_ast)
    print(f"Shell script generated: {shell_script is not None}")
    print(f"Number of lines: {len(shell_script.lines)}")
    print()

    # Display the generated script
    print("Generated shell script:")
    for i, line in enumerate(shell_script.lines, 1):
        print(f"  {i:2d}: {line}")
    print()

    # Check for file_date validations
    file_date_validations = [
        line for line in shell_script.lines if "file_date" in line or "modifié" in line
    ]
    print(f"File date validations found: {len(file_date_validations)}")
    for validation in file_date_validations:
        print(f"  - {validation}")
    print()

    print("=== File Date Handler Tests Complete ===")


if __name__ == "__main__":
    test_file_date()
