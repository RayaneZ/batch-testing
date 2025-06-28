from .atomic_compiler import compile_atomic
from parser.shunting_yard import ASTNode, Atomic, BinaryOp

def compile_ast(node: ASTNode, counter: list, last_file_var: list):
    if isinstance(node, BinaryOp):
        left_lines, left_var = compile_ast(node.left, counter, last_file_var)
        right_lines, right_var = compile_ast(node.right, counter, last_file_var)
        counter[0] += 1
        var = f"cond{counter[0]}"
        op = "&&" if node.op == "et" else "||"
        logic = f"if [ ${{{left_var}}} -eq 1 ] {op} [ ${{{right_var}}} -eq 1 ]; then {var}=1; else {var}=0; fi"
        return left_lines + right_lines + [logic], var

    elif isinstance(node, Atomic):
        counter[0] += 1
        var = f"cond{counter[0]}"
        return compile_atomic(node.value, var, last_file_var), var

    else:
        raise TypeError(f"Unknown AST node type: {type(node)}")