import os

from shtest_compiler.command_loader import PatternRegistry
from shtest_compiler.compiler.atomic_compiler import compile_atomic
from shtest_compiler.compiler.context import CompileContext
from shtest_compiler.parser.shunting_yard import (ASTVisitor, Atomic, BinaryOp,
                                                  FileContains, FileEmpty,
                                                  FileEquals, FileExists,
                                                  FileLineCount, FileSizeCheck,
                                                  SQLScriptExecution,
                                                  StderrContains,
                                                  StdoutContains, VarEquals)

# Initialisation du PatternRegistry global (à adapter selon l'architecture du projet)
ACTIONS_YML = os.path.join(os.path.dirname(__file__), "../config/patterns_actions.yml")
VALIDATIONS_YML = os.path.join(
    os.path.dirname(__file__), "../config/patterns_validations.yml"
)
pattern_registry = PatternRegistry(ACTIONS_YML, VALIDATIONS_YML)


class CompilerVisitor(ASTVisitor):
    def __init__(self, context: CompileContext):
        self.context = context

    def visit_atomic(self, node: Atomic):
        self.context.counter[0] += 1
        var = f"cond{self.context.counter[0]}"
        # Canonisation de la validation
        canon = pattern_registry.canonize_validation(node.value)
        if canon:
            phrase_canonique, handler, scope = canon
            if self.context.verbose:
                print(
                    f"[CANON] Validation canonique: '{phrase_canonique}' (handler: {handler}, scope: {scope}) pour '{node.value}'"
                )
        else:
            if self.context.verbose:
                print(
                    f"[CANON] Aucune validation canonique trouvée pour '{node.value}'"
                )
        lines = compile_atomic(
            node.value, var, self.context.last_file_var, context=self.context
        )
        if self.context.verbose:
            print(f"[AST] {var} := atomic({node.value})")
        return lines, var

    def visit_binary_op(self, node: BinaryOp):
        left_lines, left_var = node.left.accept(self)
        right_lines, right_var = node.right.accept(self)
        self.context.counter[0] += 1
        var = f"cond{self.context.counter[0]}"
        op = "&&" if node.op == "et" else "||"
        logic = f"if [ ${{{left_var}}} -eq 1 ] {op} [ ${{{right_var}}} -eq 1 ]; then {var}=1; else {var}=0; fi"
        if self.context.verbose:
            print(f"[AST] {var} := ({left_var} {op} {right_var})")
        return left_lines + right_lines + [logic], var

    def visit_stdout_contains(self, node: StdoutContains):
        self.context.counter[0] += 1
        var = f"cond{self.context.counter[0]}"
        lines = [
            f'echo "$last_stdout" | grep -q "{node.expected}" && {var}=1 || {var}=0'
        ]
        if self.context.verbose:
            print(f"[AST] {var} := stdout contient {node.expected}")
        return lines, var

    def visit_stderr_contains(self, node: StderrContains):
        self.context.counter[0] += 1
        var = f"cond{self.context.counter[0]}"
        lines = [
            f'echo "$last_stderr" | grep -q "{node.expected}" && {var}=1 || {var}=0'
        ]
        if self.context.verbose:
            print(f"[AST] {var} := stderr contient {node.expected}")
        return lines, var

    def visit_file_contains(self, node: FileContains):
        self.context.counter[0] += 1
        var = f"cond{self.context.counter[0]}"
        lines = [f'grep -q "{node.expected}" "{node.path}" && {var}=1 || {var}=0']
        if self.context.verbose:
            print(f"[AST] {var} := fichier {node.path} contient {node.expected}")
        return lines, var

    def visit_file_exists(self, node: FileExists):
        self.context.counter[0] += 1
        var = f"cond{self.context.counter[0]}"
        lines = [f'test -f "{node.path}" && {var}=1 || {var}=0']
        if self.context.verbose:
            print(f"[AST] {var} := fichier {node.path} existe")
        return lines, var

    def visit_file_empty(self, node: FileEmpty):
        self.context.counter[0] += 1
        var = f"cond{self.context.counter[0]}"
        lines = [f'[ ! -s "{node.path}" ] && {var}=1 || {var}=0']
        if self.context.verbose:
            print(f"[AST] {var} := fichier {node.path} est vide")
        return lines, var

    def visit_var_equals(self, node: VarEquals):
        self.context.counter[0] += 1
        var = f"cond{self.context.counter[0]}"
        lines = [f'[ "${{{node.name}}}" = "{node.value}" ] && {var}=1 || {var}=0']
        if self.context.verbose:
            print(f"[AST] {var} := variable {node.name} vaut {node.value}")
        return lines, var

    def visit_file_equals(self, node: FileEquals):
        self.context.counter[0] += 1
        var = f"cond{self.context.counter[0]}"
        lines = [
            f'diff -q "{node.path1}" "{node.path2}" >/dev/null && {var}=1 || {var}=0'
        ]
        if self.context.verbose:
            print(f"[AST] {var} := fichier {node.path1} est identique à {node.path2}")
        return lines, var

    def visit_file_size_check(self, node: FileSizeCheck):
        self.context.counter[0] += 1
        var = f"cond{self.context.counter[0]}"
        op = node.operator
        size = node.size
        lines = [f'[ $(stat -c%s "{node.path}") {op} {size} ] && {var}=1 || {var}=0']
        if self.context.verbose:
            print(f"[AST] {var} := taille {node.path} {op} {size}")
        return lines, var

    def visit_file_line_count(self, node: FileLineCount):
        self.context.counter[0] += 1
        var = f"cond{self.context.counter[0]}"
        op = node.operator
        count = node.count
        lines = [f'[ $(wc -l < "{node.path}") {op} {count} ] && {var}=1 || {var}=0']
        if self.context.verbose:
            print(f"[AST] {var} := lignes {node.path} {op} {count}")
        return lines, var

    def visit_sql_script_execution(self, node: SQLScriptExecution):
        from compiler.sql_drivers import get_sql_command

        self.context.counter[0] += 1
        var = f"cond{self.context.counter[0]}"
        cmd = get_sql_command(
            script=node.script, conn=node.connection, driver=node.driver
        )
        line = f'run_cmd "{cmd}"'
        if self.context.verbose:
            print(f"[AST] {var} := SQL {node.script} via {node.driver}")
        return [line], var

    def generic_visit(self, node):
        raise NotImplementedError(
            f"[BUG] No visitor implemented for node type: {type(node).__name__}"
        )
