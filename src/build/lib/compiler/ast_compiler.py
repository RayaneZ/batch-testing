
from .atomic_compiler import compile_atomic
from parser.shunting_yard import ASTNode, Atomic, BinaryOp
from .compiler import CompileContext

def compile_ast(node: ASTNode, context: CompileContext) -> tuple[list[str], str]:
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
        raise TypeError(f"Unknown AST node type: {type(node)}")
