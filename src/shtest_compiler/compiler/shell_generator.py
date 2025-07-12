"""
Shell code generation visitor.
Generates shell script code from AST nodes.
"""

import os
import re
from typing import List, Tuple, Any
from shtest_compiler.core.visitor import BaseVisitor
from shtest_compiler.core.ast import ASTNode
from shtest_compiler.core.context import CompileContext
from shtest_compiler.parser.shtest_ast import ShtestFile, TestStep, Action
from shtest_compiler.compiler.utils import compile_validation
from shtest_compiler.compiler.sql_drivers import get_sql_command
from shtest_compiler.compiler.command_translator import translate_command
from shtest_compiler.command_loader import action_to_ast
from shtest_compiler.ast_to_shell import ast_to_shell
from shtest_compiler.parser.shunting_yard import parse_validation_expression, Atomic, BinaryOp


class ShellGenerator(BaseVisitor[str]):
    """
    Visitor for generating shell script code from AST nodes.
    """
    
    def __init__(self):
        self.lines = []
        self.counter = [0]
        self.current_driver = os.environ.get("SQL_DRIVER", "oracle")
    
    def visit(self, node):
        """Visit a node and return shell code."""
        if isinstance(node, ShtestFile):
            return self.visit_shtest_file(node)
        elif isinstance(node, TestStep):
            return self.visit_test_step(node)
        elif isinstance(node, Action):
            return self.visit_action(node)
        else:
            return self.generic_visit(node)
    
    def visit_shtest_file(self, node: ShtestFile):
        """Visit a ShtestFile node."""
        # Initialize shell script
        self.lines = [
            "#!/bin/sh",
            "set -e",
            "",
            "run_cmd() {",
            "  local _stdout=$(mktemp)",
            "  local _stderr=$(mktemp)",
            "  /bin/sh -c \"$1\" >\"$_stdout\" 2>\"$_stderr\"",
            "  last_ret=$?",
            "  last_stdout=$(cat \"$_stdout\")",
            "  last_stderr=$(cat \"$_stderr\")",
            "  rm -f \"$_stdout\" \"_stderr\"",
            "  if [ $last_ret -ne 0 ]; then",
            "    echo \"STDERR: $last_stderr\"",
            "  fi",
            "}",
            "",
            "log_diff() {",
            "  expected=\"$1\"",
            "  actual=\"$2\"",
            "  if [ \"$expected\" != \"$actual\" ]; then",
            "    echo 'Différence détectée :'",
            "    echo \"- Attendu : $expected\"",
            "    echo \"- Obtenu : $actual\"",
            "  fi",
            "}",
            ""
        ]
        
        # Visit all steps
        for step in node.steps:
            self.visit(step)
        
        return "\n\n".join(self.lines)
    
    def visit_test_step(self, node: TestStep):
        """Visit a TestStep node."""
        self.lines.append(f"# ---- {node.name} ----")
        
        # Visit all actions in the step
        for action in node.actions:
            self.visit(action)
    
    def collect_validations_by_scope(self, node):
        """
        Collect validation nodes by their scope (last_action vs global).
        Returns (last_action_nodes, global_nodes)
        """
        last_action_nodes = []
        global_nodes = []
        
        def collect_recursive(ast_node):
            if isinstance(ast_node, Atomic):
                # Atomic nodes use the plugin system which has scope info
                try:
                    from shtest_compiler.parser.shunting_yard import result_atom_to_ast
                    plugin_ast = result_atom_to_ast(ast_node.value)
                    if hasattr(plugin_ast, 'scope'):
                        if plugin_ast.scope == 'last_action':
                            last_action_nodes.append(plugin_ast)
                        else:
                            global_nodes.append(plugin_ast)
                    else:
                        # Default to global if no scope specified
                        global_nodes.append(plugin_ast)
                except Exception:
                    # Fallback: treat as global
                    global_nodes.append(ast_node)
                    
            elif isinstance(ast_node, BinaryOp):
                # Recursively collect from left and right branches
                collect_recursive(ast_node.left)
                collect_recursive(ast_node.right)
            else:
                # Unknown node type, treat as global
                global_nodes.append(ast_node)
        
        collect_recursive(node)
        return last_action_nodes, global_nodes
    
    def generate_validation_shell(self, validation_nodes, prefix=""):
        """
        Generate shell code for a list of validation nodes.
        Returns list of shell lines.
        """
        lines = []
        for node in validation_nodes:
            var = f"cond{self.counter[0]}"
            self.counter[0] += 1
            if hasattr(node, 'to_shell'):
                shell_code = node.to_shell(var)
                lines.extend(shell_code.split('\n'))
            else:
                # Fallback for nodes without to_shell method
                lines.append(f"# {prefix}Validation: {type(node).__name__}")
                lines.append(f"{var}=0")
        return lines
    
    def visit_action(self, node: Action):
        """Visit an Action node."""
        # Si c'est une affectation de SQL_DRIVER, on met à jour self.current_driver mais on ne génère rien
        m = re.match(r"^définir la variable sql_driver\s*=\s*(\w+)", node.command or "", re.IGNORECASE)
        if m:
            self.current_driver = m.group(1).lower()
            return  # Ne génère pas de ligne shell pour cette action

        if node.command:
            # Nouveau pipeline plugin+YAML+AST
            ast = action_to_ast(node.command)
            if ast:
                shell_cmd = ast_to_shell(ast)
                self.lines.append(f'{shell_cmd}')
            else:
                # Fallback : ancienne traduction directe
                translated_command = translate_command(node.command)
                self.lines.append(f'run_cmd "{translated_command}"')
        
        if node.result_expr:
            # Parse validation expression and organize by scope
            try:
                validation_ast = parse_validation_expression(node.result_expr)
                last_action_valids, global_valids = self.collect_validations_by_scope(validation_ast)
                
                # Generate shell for last_action validations (immediately after action)
                if last_action_valids:
                    self.lines.append("# Validations liées à la dernière action:")
                    last_action_lines = self.generate_validation_shell(last_action_valids, "last_action_")
                    self.lines.extend(last_action_lines)
                
                # Generate shell for global validations (can be executed anytime)
                if global_valids:
                    self.lines.append("# Validations globales:")
                    global_lines = self.generate_validation_shell(global_valids, "global_")
                    self.lines.extend(global_lines)
                    
            except Exception as e:
                # Fallback to original behavior if parsing fails
                self.lines.append(f"# Erreur parsing validation: {e}")
            validation_lines = compile_validation(node.result_expr, self.counter)
            self.lines.extend(validation_lines)
    
    def generic_visit(self, node: ASTNode) -> str:
        """Handle unrecognized node types."""
        return f"# Unhandled node type: {type(node).__name__}"

