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
        """Accept a visitor and return the result"""
        method_name = f"visit_{type(self).__name__.lower()}"
        visitor_method = getattr(visitor, method_name, visitor.generic_visit)
        return visitor_method(self)


@runtime_checkable
class ASTVisitor(Protocol[T]):
    """
    Protocol for AST visitors.
    All visitors must implement this protocol.
    """

    def visit(self, node: ASTNode) -> T:
        """
        Generic visit method that dispatches to specific visit methods.
        """
        method_name = f"visit_{type(node).__name__.lower()}"
        visitor_method = getattr(self, method_name, self.generic_visit)
        return visitor_method(node)

    def generic_visit(self, node: ASTNode) -> T:
        """
        Default method for unrecognized node types.
        Must be implemented by all visitors.
        """
        raise NotImplementedError(
            f"No visitor method implemented for {type(node).__name__}"
        )


class BaseVisitor(ABC, Generic[T]):
    """
    Abstract base class for AST visitors.
    Provides common functionality and enforces visitor pattern.
    """

    def visit(self, node: ASTNode) -> T:
        """
        Generic visit method that dispatches to specific visit methods.
        """
        method_name = f"visit_{type(node).__name__.lower()}"
        visitor_method = getattr(self, method_name, self.generic_visit)
        return visitor_method(node)

    @abstractmethod
    def generic_visit(self, node: ASTNode) -> T:
        """
        Default method for unrecognized node types.
        Must be implemented by concrete visitors.
        """
        pass


class CompositeVisitor(BaseVisitor[T]):
    """
    Visitor that can compose multiple visitors.
    Useful for complex transformations that require multiple passes.
    """

    def __init__(self, visitors: list[BaseVisitor]):
        self.visitors = visitors

    def visit(self, node: ASTNode) -> T:
        """
        Visit with all composed visitors in sequence.
        """
        result = None
        for visitor in self.visitors:
            result = visitor.visit(node)
        return result

    def generic_visit(self, node: ASTNode) -> T:
        """
        Delegate to the first visitor's generic_visit.
        """
        return self.visitors[0].generic_visit(node)
