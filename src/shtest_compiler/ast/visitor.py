"""
Visitor Pattern implementation for AST traversal.
Provides both Protocol-based and ABC-based approaches.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable

# Type variable for visitor return type
T = TypeVar("T")


class ASTNode:
    """Base class for all AST nodes"""

    def accept(self, visitor: "ASTVisitor[T]") -> T:
        method_name = f"visit_{type(self).__name__.lower()}"
        visitor_method = getattr(visitor, method_name, visitor.generic_visit)
        return visitor_method(self)


class ASTVisitor(ABC, Generic[T]):
    def visit(self, node: ASTNode) -> T:
        method_name = f"visit_{type(node).__name__.lower()}"
        visitor_method = getattr(self, method_name, self.generic_visit)
        return visitor_method(node)

    @abstractmethod
    def generic_visit(self, node: ASTNode) -> T:
        pass
