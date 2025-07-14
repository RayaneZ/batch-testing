"""
Shell code generation visitor.
Generates shell script code from AST nodes.
"""

from typing import Any, List, Tuple

from shtest_compiler.ast.visitor import ASTVisitor
from shtest_compiler.core.ast import ASTNode
from shtest_compiler.core.context import CompileContext
from shtest_compiler.parser.shunting_yard import (Atomic, BinaryOp,
                                                  FileContains, FileEmpty,
                                                  FileEquals, FileExists,
                                                  FileLineCount, FileSizeCheck,
                                                  SQLScriptExecution,
                                                  StderrContains,
                                                  StdoutContains, VarEquals)


class ShellVisitor(ASTVisitor[Tuple[List[str], str]]):
    """
    Visitor for generating shell script code from AST nodes.
    Returns (shell_lines, condition_variable_name)
    """

    def __init__(self, context: CompileContext):
        self.context = context

    def visit_atomic(self, node: Atomic) -> Tuple[List[str], str]:
        """Visit atomic validation node"""
        from shtest_compiler.compiler.atomic_compiler import compile_atomic

        var = self.context.get_condition_var()
        if node.value.strip().lower() == "true":
            return [f"{var}=1"], var
        lines = compile_atomic(
            node.value, var, self.context.last_file_var, context=self.context
        )

        if self.context.verbose:
            print(f"[SHELL] {var} := atomic({node.value})")

        return lines, var

    def visit_binary_op(self, node: BinaryOp) -> Tuple[List[str], str]:
        """Visit binary operation node"""
        left_lines, left_var = node.left.accept(self)
        right_lines, right_var = node.right.accept(self)

        var = self.context.get_condition_var()
        op = "&&" if node.op == "et" else "||"
        logic = f"if [ ${{{left_var}}} -eq 1 ] {op} [ ${{{right_var}}} -eq 1 ]; then {var}=1; else {var}=0; fi"

        if self.context.verbose:
            print(f"[SHELL] {var} := ({left_var} {op} {right_var})")

        return left_lines + right_lines + [logic], var

    def visit_stdout_contains(self, node: StdoutContains) -> Tuple[List[str], str]:
        """Visit stdout contains validation"""
        var = self.context.get_condition_var()
        lines = [
            f'echo "$last_stdout" | grep -q "{node.expected}" && {var}=1 || {var}=0'
        ]

        if self.context.verbose:
            print(f"[SHELL] {var} := stdout contient {node.expected}")

        return lines, var

    def visit_stderr_contains(self, node: StderrContains) -> Tuple[List[str], str]:
        """Visit stderr contains validation"""
        var = self.context.get_condition_var()
        lines = [
            f'echo "$last_stderr" | grep -q "{node.expected}" && {var}=1 || {var}=0'
        ]

        if self.context.verbose:
            print(f"[SHELL] {var} := stderr contient {node.expected}")

        return lines, var

    def visit_file_contains(self, node: FileContains) -> Tuple[List[str], str]:
        """Visit file contains validation"""
        var = self.context.get_condition_var()
        lines = [f'grep -q "{node.expected}" "{node.path}" && {var}=1 || {var}=0']

        if self.context.verbose:
            print(f"[SHELL] {var} := fichier {node.path} contient {node.expected}")

        return lines, var

    def visit_file_exists(self, node: FileExists) -> Tuple[List[str], str]:
        """Visit file exists validation"""
        var = self.context.get_condition_var()
        lines = [f'test -f "{node.path}" && {var}=1 || {var}=0']

        if self.context.verbose:
            print(f"[SHELL] {var} := fichier {node.path} existe")

        return lines, var

    def visit_file_empty(self, node: FileEmpty) -> Tuple[List[str], str]:
        """Visit file empty validation"""
        var = self.context.get_condition_var()
        lines = [f'[ ! -s "{node.path}" ] && {var}=1 || {var}=0']

        if self.context.verbose:
            print(f"[SHELL] {var} := fichier {node.path} est vide")

        return lines, var

    def visit_var_equals(self, node: VarEquals) -> Tuple[List[str], str]:
        """Visit variable equals validation"""
        var = self.context.get_condition_var()
        lines = [f'[ "${{{node.name}}}" = "{node.value}" ] && {var}=1 || {var}=0']

        if self.context.verbose:
            print(f"[SHELL] {var} := variable {node.name} vaut {node.value}")

        return lines, var

    def visit_file_equals(self, node: FileEquals) -> Tuple[List[str], str]:
        """Visit file equals validation"""
        var = self.context.get_condition_var()
        lines = [
            f'diff -q "{node.path1}" "{node.path2}" >/dev/null && {var}=1 || {var}=0'
        ]

        if self.context.verbose:
            print(f"[SHELL] {var} := fichier {node.path1} est identique à {node.path2}")

        return lines, var

    def visit_file_size_check(self, node: FileSizeCheck) -> Tuple[List[str], str]:
        """Visit file size check validation"""
        var = self.context.get_condition_var()
        op = node.operator
        size = node.size
        lines = [f'[ $(stat -c%s "{node.path}") {op} {size} ] && {var}=1 || {var}=0']

        if self.context.verbose:
            print(f"[SHELL] {var} := taille {node.path} {op} {size}")

        return lines, var

    def visit_file_line_count(self, node: FileLineCount) -> Tuple[List[str], str]:
        """Visit file line count validation"""
        var = self.context.get_condition_var()
        op = node.operator
        count = node.count
        lines = [f'[ $(wc -l < "{node.path}") {op} {count} ] && {var}=1 || {var}=0']

        if self.context.verbose:
            print(f"[SHELL] {var} := lignes {node.path} {op} {count}")

        return lines, var

    def visit_sql_script_execution(
        self, node: SQLScriptExecution
    ) -> Tuple[List[str], str]:
        """Visit SQL script execution"""
        from shtest_compiler.compiler.sql_drivers import get_sql_command

        var = self.context.get_condition_var()
        cmd = get_sql_command(
            script=node.script, conn=node.connection, driver=node.driver
        )
        line = f'run_cmd "{cmd}"'

        if self.context.verbose:
            print(f"[SHELL] {var} := SQL {node.script} via {node.driver}")

        return [line], var

    def generic_visit(self, node: ASTNode) -> Tuple[List[str], str]:
        """Handle unrecognized node types"""
        error_msg = f"No shell generation implemented for {type(node).__name__}"
        self.context.add_error(error_msg)

        # Return a fallback that will fail at runtime
        var = self.context.get_condition_var()
        lines = [f"# {error_msg}", f'echo "{error_msg}" 1>&2', f"{var}=0"]

        return lines, var
