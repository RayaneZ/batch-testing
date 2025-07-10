from dataclasses import dataclass
from typing import List, Protocol
import re
from shtest_compiler.parser.alias_utils import AliasResolver

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


@dataclass
class BinaryOp(ASTNode):
    op: str  # 'et' or 'ou'
    left: ASTNode
    right: ASTNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_binary_op(self)


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
            while stack and stack[-1].lower() in precedence and precedence[stack[-1].lower()] >= precedence[ltok]:
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
    resolver = AliasResolver()
    tokens = _tokenize_expression(expression)
    tokens = [resolver.resolve(t)[0] if t not in ("et", "ou", "(", ")") else t for t in tokens]
    postfix = _to_postfix(tokens)

    stack: List[ASTNode] = []
    for tok in postfix:
        if tok in ("et", "ou"):
            right = stack.pop()
            left = stack.pop()
            stack.append(BinaryOp(tok, left, right))
        else:
            stack.append(Atomic(tok))

    return stack[0]


__all__ = ["VarEquals"]