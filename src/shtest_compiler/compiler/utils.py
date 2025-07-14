"""
Utility functions for the compiler module.
"""

from typing import List, Union

from shtest_compiler.compiler.visitors import CompilerVisitor
from shtest_compiler.core.context import CompileContext
from shtest_compiler.parser.shunting_yard import parse_validation_expression


def compile_validation(
    expr: str, counter=None, last_file_var=None, verbose=False
) -> List[str]:
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


def shell_condition(
    success_val: str, fail_val: str, scope: str = "global"
) -> List[str]:
    """Return shell instructions validating that the last command succeeded.
    The scope can be 'global' or 'last_action' to determine the context of the validation.
    """
    # Pour l'instant, on utilise le même comportement pour tous les scopes
    # Mais on pourrait adapter le code shell selon le scope si nécessaire
    return [
        f'if [ $last_ret -eq 0 ]; then actual="{success_val}"; else actual="{fail_val}"; fi',
        f'expected="{success_val}"',
    ]


def retcode_condition(code: Union[int, str], scope: str = "global") -> List[str]:
    """Return instructions checking that ``$last_ret`` matches *code*.
    The scope can be 'global' or 'last_action' to determine the context of the validation.
    """
    code = int(code)
    # Pour l'instant, on utilise le même comportement pour tous les scopes
    # Mais on pourrait adapter le code shell selon le scope si nécessaire
    return [
        f'if [ $last_ret -eq {code} ]; then actual="retour {code}"; else actual="retour $last_ret"; fi',
        f'expected="retour {code}"',
    ]
