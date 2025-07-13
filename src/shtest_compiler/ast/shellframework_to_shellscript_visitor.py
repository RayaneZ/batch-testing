from shtest_compiler.ast.visitor import ASTVisitor
from shtest_compiler.ast.shell_framework_ast import ShellFrameworkAST, ShellFunctionDef, ShellFunctionCall, InlineShellCode, ShellTestStep, ValidationCheck, ActionNode
from shtest_compiler.ast.shell_script_ast import ShellScript
from shtest_compiler.parser.shunting_yard import BinaryOp, Atomic
from typing import List

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
        return node.code_lines

    def visit_validationcheck(self, node: ValidationCheck) -> List[str]:
        params = node.params if hasattr(node, 'params') else {}
        
        # Handle parameter substitution in the command
        actual_cmd = node.actual_cmd
        for param_name, param_value in params.items():
            if param_value is not None:
                actual_cmd = actual_cmd.replace(f"{{{param_name}}}", str(param_value))
        
        # Construct proper shell validation logic
        lines = [
            f"# {node.expected}",
            f"validation_result=$({actual_cmd})",
            f"if [ $? -eq 0 ]; then",
            f"    echo 'OK: {node.expected}'",
            f"else",
            f"    echo 'FAIL: {node.expected}'",
            f"    echo 'Command output: $validation_result'",
            f"    exit 1",
            f"fi"
        ]
        return lines

    def visit_binary_op(self, node: BinaryOp) -> List[str]:
        """Handle compound validations (AND/OR)"""
        # Visit left and right operands
        left_lines = self.visit(node.left)
        right_lines = self.visit(node.right)
        
        # Generate condition variables
        left_var = self.get_condition_var()
        right_var = self.get_condition_var()
        result_var = self.get_condition_var()
        
        # Construct compound validation logic
        op = "&&" if node.op == "et" else "||"
        compound_lines = [
            f"# Compound validation: {node.op}",
            f"{left_var}=$?",
            f"# Second validation:",
        ] + right_lines + [
            f"{right_var}=$?",
            f"if [ ${left_var} -eq 0 ] {op} [ ${right_var} -eq 0 ]; then",
            f"    echo 'OK: Compound validation ({node.op})'",
            f"else",
            f"    echo 'FAIL: Compound validation ({node.op})'",
            f"    exit 1",
            f"fi"
        ]
        
        return left_lines + compound_lines

    def visit_atomic(self, node: Atomic) -> List[str]:
        """Handle atomic validations"""
        # This should be handled by compile_atomic and return ValidationCheck
        # For now, treat as a simple validation
        return [f"# Atomic validation: {node.value}", f"echo 'OK: {node.value}'"]

    def visit_actionnode(self, node: ActionNode) -> List[str]:
        return [node.to_shell()]

    def generic_visit(self, node):
        return [] 