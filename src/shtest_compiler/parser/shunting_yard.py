import importlib
import os
import re
import unicodedata
from dataclasses import dataclass
from typing import List, Protocol

import yaml

# Ajout : chargement des patterns de validation
RESULT_PATTERNS_PATH = os.path.join(os.path.dirname(__file__), "../result_patterns.yml")
with open(RESULT_PATTERNS_PATH, encoding="utf-8") as f:
    RESULT_PATTERNS = yaml.safe_load(f)


def _normalize_atom(atom: str) -> str:
    atom = atom.strip().lower().rstrip(".;")
    atom = "".join(
        c for c in unicodedata.normalize("NFD", atom) if unicodedata.category(c) != "Mn"
    )
    return atom


def result_atom_to_ast(atom: str):
    norm_atom = _normalize_atom(atom)
    for entry in RESULT_PATTERNS:
        m = re.match(entry["pattern"], norm_atom, re.IGNORECASE)
        if m:
            plugin = importlib.import_module(f"shtest_compiler.plugins.{entry['type']}")
            # On transmet le scope au plugin (si accepté)
            if "scope" in entry:
                return plugin.handle(m.groups(), scope=entry["scope"])
            else:
                return plugin.handle(m.groups())
    raise ValueError(f"Aucune règle de validation ne correspond à : {atom}")


# -------- VISITEUR AST --------


class ASTVisitor(Protocol):
    def visit_sql_script_execution(self, node: "SQLScriptExecution"): ...
    def visit_file_equals(self, node: "FileEquals"): ...
    def visit_file_size_check(self, node: "FileSizeCheck"): ...
    def visit_file_line_count(self, node: "FileLineCount"): ...
    def visit_var_equals(self, node: "VarEquals"): ...
    def visit_file_empty(self, node: "FileEmpty"): ...
    def visit_file_exists(self, node: "FileExists"): ...
    def visit_file_contains(self, node: "FileContains"): ...
    def visit_stdout_contains(self, node: "StdoutContains"): ...
    def visit_stderr_contains(self, node: "StderrContains"): ...
    def visit_atomic(self, node: "Atomic"): ...
    def visit_binary_op(self, node: "BinaryOp"): ...


# -------- BASE AST --------


@dataclass
class ASTNode:
    def accept(self, visitor: ASTVisitor):
        raise NotImplementedError()


@dataclass
class Atomic(ASTNode):
    value: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_atomic(self)

    def to_shell(self, var):
        # Utilise le pipeline plugin pour la feuille atomique
        plugin_ast = result_atom_to_ast(self.value)
        return plugin_ast.to_shell(var)


@dataclass
class BinaryOp(ASTNode):
    op: str  # 'et' or 'ou'
    left: ASTNode
    right: ASTNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_binary_op(self)

    def to_shell(self, var):
        # Génère le shell récursivement pour AND/OR
        left_var = f"{var}_l"
        right_var = f"{var}_r"
        left_shell = self.left.to_shell(left_var)
        right_shell = self.right.to_shell(right_var)
        if self.op == "et":
            logic = f"if [ ${{{left_var}}} -eq 1 ] && [ ${{{right_var}}} -eq 1 ]; then {var}=1; else {var}=0; fi"
        else:
            logic = f"if [ ${{{left_var}}} -eq 1 ] || [ ${{{right_var}}} -eq 1 ]; then {var}=1; else {var}=0; fi"
        return f"{left_shell}\n{right_shell}\n{logic}"


# -------- VALIDATION NODES --------


@dataclass
class StdoutContains(ASTNode):
    expected: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_stdout_contains(self)


@dataclass
class StderrContains(ASTNode):
    expected: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_stderr_contains(self)


@dataclass
class FileContains(ASTNode):
    path: str
    expected: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_file_contains(self)


@dataclass
class FileExists(ASTNode):
    path: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_file_exists(self)


@dataclass
class FileEmpty(ASTNode):
    path: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_file_empty(self)


@dataclass
class VarEquals(ASTNode):
    name: str
    value: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_var_equals(self)


@dataclass
class FileEquals(ASTNode):
    path1: str
    path2: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_file_equals(self)


@dataclass
class FileSizeCheck(ASTNode):
    path: str
    operator: str
    size: int

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_file_size_check(self)


@dataclass
class FileLineCount(ASTNode):
    path: str
    operator: str
    count: int

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_file_line_count(self)


@dataclass
class SQLScriptExecution(ASTNode):
    script: str
    connection: str
    driver: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_sql_script_execution(self)


# -------- PARSE LOGIQUE --------


def _tokenize_expression(expr: str) -> List[str]:
    return [t.strip() for t in re.split(r"(\bet\b|\bou\b|\(|\))", expr) if t.strip()]


def _to_postfix(tokens: List[str]) -> List[str]:
    precedence = {"et": 2, "ou": 1}
    output: List[str] = []
    stack: List[str] = []

    for tok in tokens:
        ltok = tok.lower()
        if ltok in precedence:
            while (
                stack
                and stack[-1].lower() in precedence
                and precedence[stack[-1].lower()] >= precedence[ltok]
            ):
                output.append(stack.pop())
            stack.append(ltok)
        elif tok == "(":
            stack.append(tok)
        elif tok == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if stack and stack[-1] == "(":
                stack.pop()
        else:
            output.append(tok)

    while stack:
        output.append(stack.pop())

    return output


def parse_validation_expression(expression: str) -> ASTNode:
    tokens = _tokenize_expression(expression)
    postfix = _to_postfix(tokens)
    stack: List[ASTNode] = []
    for tok in postfix:
        if tok in ("et", "ou"):
            right = stack.pop()
            left = stack.pop()
            stack.append(BinaryOp(tok, left, right))
        else:
            stack.append(Atomic(tok))
    ast = stack[0]
    # If the AST is a single Atomic, wrap it as BinaryOp('et', Atomic, Atomic('true'))
    if isinstance(ast, Atomic):
        ast = BinaryOp("et", ast, Atomic("true"))
    return ast


__all__ = ["VarEquals"]
