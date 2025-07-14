from typing import List

from shtest_compiler.ast.shell_framework_ast import (
    InlineShellCode,
    ShellFrameworkAST,
    ShellFunctionCall,
    ShellFunctionDef,
    ShellTestStep,
)


def emit_shell_script(shell_ast: ShellFrameworkAST) -> str:
    lines: List[str] = []
    # Emit global code (e.g., prologue)
    lines.extend(shell_ast.global_code)
    lines.append("")
    # Emit helper functions
    for helper in shell_ast.helpers:
        param_str = " ".join([f"${i+1}" for i in range(len(helper.params))])
        lines.append(f"{helper.name}() {{")
        for body_line in helper.body_lines:
            lines.append(f"    {body_line}")
        lines.append("}")
        lines.append("")
    # Emit test steps
    for step in shell_ast.steps:
        lines.append(f"# Test step: {step.name}")
        for action in step.actions:
            if isinstance(action, ShellFunctionCall):
                arg_str = " ".join([f'"{a}"' for a in action.args])
                lines.append(f"{action.name} {arg_str}")
            elif isinstance(action, InlineShellCode):
                lines.extend(action.code_lines)
        for validation in step.validations:
            if isinstance(validation, ShellFunctionCall):
                arg_str = " ".join([f'"{a}"' for a in validation.args])
                lines.append(f"{validation.name} {arg_str}")
            elif isinstance(validation, InlineShellCode):
                lines.extend(validation.code_lines)
        lines.append("")
    lines.append("echo 'All steps and validations passed.'")
    lines.append("exit 0")
    return "\n".join(lines)
