#!/usr/bin/env python3
"""
Test for lifting functionality.
"""

from shtest_compiler.parser.shtest_ast import ShtestFile, TestStep, Action
from shtest_compiler.ast.shtest_to_shellframework_visitor import (
    ShtestToShellFrameworkVisitor,
)
from shtest_compiler.ast.shell_framework_binder import ShellFrameworkLifter
from shtest_compiler.ast.shellframework_to_shellscript_visitor import (
    ShellFrameworkToShellScriptVisitor,
)


def test_lifting():
    print("=== Testing Lifting Functionality ===\n")

    # Create a test AST
    test_ast = ShtestFile(
        steps=[
            TestStep(
                name="Test Step",
                actions=[
                    Action(
                        command="touch /tmp/test.txt",
                        result_expr="Le fichier /tmp/test.txt est présent",
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

    print("=== Lifting Functionality Tests Complete ===")


if __name__ == "__main__":
    test_lifting()
