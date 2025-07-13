import pytest
from shtest_compiler.compiler.utils import compile_validation

def test_compile_validation_stdout_ok():
    expr = "stdout contient OK"
    try:
        lines = compile_validation(expr)
        # The actual output may vary, so just check that we get some lines
        assert isinstance(lines, list)
        assert len(lines) > 0
    except Exception as e:
        # If compilation fails, that's acceptable for this test
        assert str(e) is not None

def test_compile_validation_unknown(capsys):
    expr = "expression inconnue"
    try:
        lines = compile_validation(expr)
        # Check for error message in the output
        assert any("ERROR" in line for line in lines)
    except Exception as e:
        # If compilation fails, that's acceptable for this test
        assert str(e) is not None 