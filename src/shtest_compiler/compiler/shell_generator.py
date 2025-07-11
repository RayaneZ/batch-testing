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
    
    def visit_action(self, node: Action):
        """Visit an Action node."""
        if node.command:
            # Translate the command from natural language to shell command
            translated_command = translate_command(node.command)
            
            # Handle special cases
            if "SQL" in node.command.upper() and ".sql" in node.command:
                # Handle SQL commands specifically
                scripts = re.findall(r"\S+\.sql", node.command, re.IGNORECASE)
                if scripts:
                    for script in scripts:
                        cmd = get_sql_command(
                            script=script,
                            conn="${SQL_CONN:-user/password@db}",
                            driver=self.current_driver
                        )
                        self.lines.append(f"run_cmd \"{cmd}\"")
                else:
                    self.lines.append(f"run_cmd \"{translated_command}\"")
            else:
                # Use the translated command
                self.lines.append(f"run_cmd \"{translated_command}\"")
        
        if node.result_expr:
            # Handle validation
            validation_lines = compile_validation(node.result_expr, self.counter)
            self.lines.extend(validation_lines)
    
    def generic_visit(self, node: ASTNode) -> str:
        """Handle unrecognized node types."""
        return f"# Unhandled node type: {type(node).__name__}"

