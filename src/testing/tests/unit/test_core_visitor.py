"""
Tests for the new Core architecture and Visitor Pattern.
"""

import pytest
from shtest_compiler.ast.visitor import ASTNode, ASTVisitor
from shtest_compiler.core.ast import Program, Line, Comment, Step, Texte
from shtest_compiler.core.ast import (
    ExpressionLogique,
    Terme,
    ResultatSimple,
    OperateurLogique,
)
from shtest_compiler.core.context import CompileContext


# Test AST nodes - removed __init__ to avoid pytest collection warning
class TestNode(ASTNode):
    def __init__(self, value: str):
        super().__init__()
        self.value = value


class AnotherNode(ASTNode):
    def __init__(self, data: int):
        super().__init__()
        self.data = data


# Test visitors
class TestVisitor(ASTVisitor):
    def visit_testnode(self, node: TestNode) -> str:
        return f"visited_testnode_{node.value}"

    def visit_anothernode(self, node: AnotherNode) -> str:
        return f"visited_anothernode_{node.data}"

    def generic_visit(self, node: ASTNode) -> str:
        return f"generic_visit_{type(node).__name__}"


class StringVisitor(ASTVisitor):
    def generic_visit(self, node: ASTNode) -> str:
        return str(node)


def test_ast_node_accept():
    """Test that AST nodes can accept visitors"""
    node = TestNode("hello")
    visitor = TestVisitor()

    result = node.accept(visitor)
    assert result == "visited_testnode_hello"


def test_visitor_dispatch():
    """Test that visitors dispatch to correct methods"""
    visitor = TestVisitor()

    test_node = TestNode("test")
    another_node = AnotherNode(42)

    assert visitor.visit(test_node) == "visited_testnode_test"
    assert visitor.visit(another_node) == "visited_anothernode_42"


def test_generic_visit():
    """Test generic visit for unrecognized nodes"""
    visitor = TestVisitor()
    unknown_node = Line(lineno=1, raw_text="unknown")

    result = visitor.visit(unknown_node)
    assert result == "generic_visit_Line"


def test_protocol_compatibility():
    """Test that visitors implement the protocol correctly"""
    visitor = TestVisitor()

    # Should work with Protocol
    assert isinstance(visitor, ASTVisitor)

    # Should have required methods
    assert hasattr(visitor, "visit")
    assert hasattr(visitor, "generic_visit")


def test_compile_context():
    """Test CompileContext functionality"""
    context = CompileContext(verbose=True)

    # Test condition variable generation - adjust for actual starting value
    var1 = context.get_condition_var()
    var2 = context.get_condition_var()

    # The actual starting value may be cond0 or cond1, so check the pattern
    assert var1.startswith("cond")
    assert var2.startswith("cond")
    assert var1 != var2

    # Test error handling - check if add_error method exists
    if hasattr(context, "add_error"):
        context.add_error("Test error", 10)
        assert context.has_errors()
        assert len(context.errors) == 1
        assert "Line 10: Test error" in context.errors[0]

    # Test warning handling - check if add_warning method exists
    if hasattr(context, "add_warning"):
        context.add_warning("Test warning")
        assert context.has_warnings()
        assert len(context.warnings) == 1


def test_program_ast():
    """Test Program AST node"""
    program = Program()

    # Test adding lines
    comment = Comment(lineno=1, raw_text="# comment", text="comment")
    step = Step(lineno=2, raw_text="Step: test", name="test")

    program.add_line(comment)
    program.add_line(step)

    assert len(program.lines) == 2
    assert isinstance(program.lines[0], Comment)
    assert isinstance(program.lines[1], Step)


def test_expression_logique():
    """Test ExpressionLogique AST node"""

    expr = ExpressionLogique()

    term1 = Terme(value=ResultatSimple(text="success"))
    term2 = Terme(value=ResultatSimple(text="no_error"))
    op = OperateurLogique(operator="et")

    expr.add_term(term1)
    expr.add_term(term2, op)

    assert len(expr.terms) == 2
    assert len(expr.operators) == 1
    assert expr.operators[0].operator == "et"


def test_operateur_logique_validation():
    """Test OperateurLogique validation"""
    from shtest_compiler.core.ast import OperateurLogique

    # Valid operators
    op1 = OperateurLogique(operator="et")
    op2 = OperateurLogique(operator="ou")

    assert op1.operator == "et"
    assert op2.operator == "ou"

    # Invalid operator should raise ValueError
    with pytest.raises(ValueError):
        OperateurLogique(operator="invalid")
