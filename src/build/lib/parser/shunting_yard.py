from dataclasses import dataclass
from typing import List, Protocol
import re

__all__ = [
    "ASTNode", "Atomic", "BinaryOp",
    "VarEquals", "StdoutContains", "StderrContains",
    "SQLScriptExecution", "FileExists", "FileEmpty",
    "FileEquals", "FileSizeCheck", "FileLineCount", "FileContains"
]

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
    op: str
    left: ASTNode
    right: ASTNode
    def accept(self, visitor: ASTVisitor):
        return visitor.visit_binary_op(self)

@dataclass
class VarEquals(ASTNode):
    variable: str
    expected: str
    def accept(self, visitor: ASTVisitor):
        return visitor.visit_var_equals(self)

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
class SQLScriptExecution(ASTNode):
    script: str
    connection: str = ""
    driver: str = ""
    def accept(self, visitor: ASTVisitor):
        return visitor.visit_sql_script_execution(self)

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
class FileContains(ASTNode):
    path: str
    expected: str
    def accept(self, visitor: ASTVisitor):
        return visitor.visit_file_contains(self)