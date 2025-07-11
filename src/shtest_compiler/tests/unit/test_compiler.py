import pytest
from shtest_compiler.compiler.compiler import compile_validation

def test_compile_validation_stdout_ok():
    expr = "stdout contient OK"
    lines = compile_validation(expr)
    assert any("grep -q" in line for line in lines)
    assert any("OK" in line for line in lines)

def test_compile_validation_unknown(capsys):
    expr = "expression inconnue"
    lines = compile_validation(expr)
    assert any("non vérifié" in line for line in lines) 