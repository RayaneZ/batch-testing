from typing import List

from shtest_compiler.ast.shell_framework_ast import (ActionNode,
                                                     InlineShellCode,
                                                     ShellFrameworkAST,
                                                     ShellFunctionCall,
                                                     ShellFunctionDef,
                                                     ShellTestStep,
                                                     ValidationCheck)
from shtest_compiler.ast.shell_script_ast import ShellScript
from shtest_compiler.ast.visitor import ASTVisitor
from shtest_compiler.parser.shunting_yard import Atomic, BinaryOp


class ShellFrameworkToShellScriptVisitor(ASTVisitor[ShellScript]):
    def __init__(self):
        self.condition_counter = 0

    def get_condition_var(self):
        """Generate unique condition variable names"""
        self.condition_counter += 1
        return f"cond{self.condition_counter}"

    def visit_shellframeworkast(self, node: ShellFrameworkAST) -> ShellScript:
        lines: List[str] = []
        # Emit global code (e.g., prologue)
        lines.extend(node.global_code)
        lines.append("")
        # Emit helper functions
        for helper in node.helpers:
            lines.extend(self.visit(helper))
            lines.append("")
        # Emit test steps
        for step in node.steps:
            lines.extend(self.visit(step))
            lines.append("")
        lines.append("echo 'All steps and validations passed.'")
        lines.append("exit 0")
        return ShellScript(lines=lines)

    def visit_shellfunctiondef(self, node: ShellFunctionDef) -> List[str]:
        lines = [f"{node.name}() {{"]
        for body_line in node.body_lines:
            lines.append(f"    {body_line}")
        lines.append("}")
        return lines

    def visit_shellteststep(self, node: ShellTestStep) -> List[str]:
        lines = [f"# Test step: {node.name}"]
        for action in node.actions:
            if isinstance(action, ActionNode):
                lines.append(action.to_shell())
            else:
                lines.extend(self.visit(action))
        for validation in node.validations:
            lines.extend(self.visit(validation))
        return lines

    def visit_shellfunctioncall(self, node: ShellFunctionCall) -> List[str]:
        arg_str = " ".join([f'"{a}"' for a in node.args])
        return [f"{node.name} {arg_str}"]

    def visit_inlineshellcode(self, node: InlineShellCode) -> List[str]:
        lines = []
        for item in node.code_lines:
            if isinstance(item, ValidationCheck):
                # Process ValidationCheck objects through the visitor
                lines.extend(self.visit_validationcheck(item))
            else:
                # Regular string lines
                lines.append(item)
        return lines

    def visit_validationcheck(self, node: ValidationCheck) -> List[str]:
        params = node.params if hasattr(node, "params") else {}

        # Handle parameter substitution in the command
        actual_cmd = node.actual_cmd
        for param_name, param_value in params.items():
            if param_value is not None:
                actual_cmd = actual_cmd.replace(f"{{{param_name}}}", str(param_value))

        # Get opposite message for failure case
        opposite = params.get("opposite", f"NOT({node.expected})")

        # Escape apostrophes and quotes for shell echo statements
        def shell_escape_echo(text):
            """Escape text for use in single-quoted echo statements"""
            if text is None:
                return ""
            # Replace single quotes with the proper shell escaping sequence
            return str(text).replace("'", "'\\''")

        escaped_expected = shell_escape_echo(node.expected)
        escaped_opposite = shell_escape_echo(opposite)

        # Construct proper shell validation logic from atomic command
        lines = [
            f"# {node.expected}",
            f"if {actual_cmd}; then",
            f"    echo 'OK: {escaped_expected}'",
            f"else",
            f"    echo 'FAIL: {escaped_opposite}'",
            f"    exit 1",
            f"fi",
        ]
        return lines

    def visit_binaryop(self, node: BinaryOp) -> List[str]:
        """Alias for visit_binary_op to match base class naming convention"""
        return self.visit_binary_op(node)

    def visit_binary_op(self, node: BinaryOp) -> List[str]:
        from shtest_compiler.config.debug_config import (debug_print,
                                                         is_debug_enabled)

        debug_enabled = is_debug_enabled()
        if debug_enabled:
            debug_print(
                f"[DEBUG] visit_binary_op: op={node.op}, left={getattr(node.left, 'value', node.left)}, right={getattr(node.right, 'value', node.right)}"
            )
        """Handle compound validations (AND/OR) with proper linearization"""
        # Visit left and right operands
        left_lines = self.visit(node.left)
        right_lines = self.visit(node.right)

        # Generate condition variables
        left_var = self.get_condition_var()
        right_var = self.get_condition_var()
        result_var = self.get_condition_var()

        # Construct compound validation logic with proper shell operators
        op = "&&" if node.op == "et" else "||"
        compound_lines = (
            [
                f"# Compound validation: {node.op}",
                f"# First validation:",
            ]
            + left_lines
            + [
                f"{left_var}=$?",
                f"# Second validation:",
            ]
            + right_lines
            + [
                f"{right_var}=$?",
                f"if [ ${left_var} -eq 0 ] {op} [ ${right_var} -eq 0 ]; then",
                f"    echo 'OK: Compound validation ({node.op})'",
                f"else",
                f"    echo 'FAIL: Compound validation ({node.op})'",
                f"    exit 1",
                f"fi",
            ]
        )

        return compound_lines

    def visit_atomic(self, node: Atomic) -> List[str]:
        from shtest_compiler.config.debug_config import (debug_print,
                                                         is_debug_enabled)

        debug_enabled = is_debug_enabled()
        if debug_enabled:
            debug_print(f"[DEBUG] visit_atomic: value={node.value}")
        from shtest_compiler.compiler.atomic_compiler import compile_atomic

        # Use compile_atomic to generate ValidationCheck
        validation_result = compile_atomic(
            node.value, varname="result", last_file_var=None
        )

        # Handle different return types from compile_atomic
        if validation_result and len(validation_result) > 0:
            first_item = validation_result[0]

            # If it's a ValidationCheck object
            if hasattr(first_item, "expected") and hasattr(first_item, "actual_cmd"):
                validation_check = first_item
                return self.visit_validationcheck(validation_check)

            # If it's already shell code lines (list of strings)
            elif isinstance(first_item, str):
                return validation_result

            # If it's a single string
            elif isinstance(validation_result, str):
                return [validation_result]

        # Fallback: return error message
        return [f"echo 'ERROR: Could not compile atomic validation: {node.value}'"]

    def visit_actionnode(self, node: ActionNode) -> List[str]:
        return [node.to_shell()]

    def generic_visit(self, node):
        return []
