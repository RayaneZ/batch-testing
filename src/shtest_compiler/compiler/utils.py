"""
Utility functions for the compiler module.
"""

from shtest_compiler.parser.shunting_yard import parse_validation_expression
from shtest_compiler.core.context import CompileContext
from shtest_compiler.compiler.visitors import CompilerVisitor

def compile_validation(expr: str, counter=None, last_file_var=None, verbose=False) -> list[str]:
    context = CompileContext(counter, last_file_var, verbose)
    ast = parse_validation_expression(expr)
    if verbose:
        print(f"[COMPILE] AST: {ast}")
    compiler = CompilerVisitor(context)
    lines, _ = ast.accept(compiler)
    if verbose:
        print("[COMPILE] Shell lines:")
        for line in lines:
            print("  " + line)
    return lines

import unicodedata


def strip_accents(text: str) -> str:
    """Normalize *text* by removing accents for lenient comparisons."""
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )


def shell_condition(success_val: str, fail_val: str, expected_val: str | None = None) -> list[str]:
    """Return shell instructions validating that the last command succeeded."""
    if expected_val is None:
        expected_val = success_val
    return [
        f"if [ $last_ret -eq 0 ]; then actual=\"{success_val}\"; else actual=\"{fail_val}\"; fi",
        f"expected=\"{expected_val}\"",
    ]


def retcode_condition(code: int | str) -> list[str]:
    """Return instructions checking that ``$last_ret`` matches *code*."""
    code = int(code)
    return [
        f"if [ $last_ret -eq {code} ]; then actual=\"retour {code}\"; else actual=\"retour $last_ret\"; fi",
        f"expected=\"retour {code}\"",
    ]
