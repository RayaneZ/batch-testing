"""
Module de compilation récursive d'un AST (noeuds BinaryOp et Atomic)
vers une suite d'instructions shell conditionnelles.
"""

from typing import List, Tuple

from shtest_compiler.parser.shunting_yard import ASTNode, Atomic, BinaryOp

from .atomic_compiler import compile_atomic
from .compiler import CompileContext


def compile_ast(node: ASTNode, context: CompileContext) -> Tuple[List[str], str]:
    """
    Compile un nœud AST (BinaryOp ou Atomic) en lignes shell + nom de variable résultat.
    Retourne une liste de lignes de shell et le nom de la variable contenant le résultat booléen (0 ou 1).
    """
    if isinstance(node, BinaryOp):
        left_lines, left_var = compile_ast(node.left, context)
        right_lines, right_var = compile_ast(node.right, context)

        context.counter[0] += 1
        var = f"cond{context.counter[0]}"

        op = "&&" if node.op == "et" else "||"
        logic = f"if [ ${{{left_var}}} -eq 1 ] {op} [ ${{{right_var}}} -eq 1 ]; then {var}=1; else {var}=0; fi"

        if context.verbose:
            print(f"[AST] {var} := ({left_var} {op} {right_var})")

        return left_lines + right_lines + [logic], var

    elif isinstance(node, Atomic):
        context.counter[0] += 1
        var = f"cond{context.counter[0]}"
        lines = compile_atomic(node.value, var, context.last_file_var)

        if context.verbose:
            print(f"[AST] {var} := atomic({node.value})")

        return lines, var

    else:
        if context.verbose:
            print(f"[AST] Type inconnu: {type(node)}")
        raise TypeError(f"Unknown AST node type: {type(node)}")
