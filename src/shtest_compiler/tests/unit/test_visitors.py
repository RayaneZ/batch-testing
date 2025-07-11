import pytest
from shtest_compiler.compiler.visitors import CompilerVisitor
from shtest_compiler.compiler.context import CompileContext

class DummyNode:
    pass

def test_generic_visit_raises():
    visitor = CompilerVisitor(CompileContext())
    node = DummyNode()
    with pytest.raises(NotImplementedError):
        visitor.generic_visit(node) 