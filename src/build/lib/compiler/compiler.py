from parser.shunting_yard import SQLScriptExecution, parse_validation_expression
from compiler.context import CompileContext
from compiler.visitors import CompilerVisitor

def compile_validation(expr: str, counter=None, last_file_var=None, verbose=False) -> list[str]:
    context = CompileContext(counter, last_file_var, verbose)
    ast = parse_validation_expression(expr)
    if verbose:
        print(f"[COMPILE] AST: {ast}")
    compiler = CompilerVisitor(context)
    lines, _ = ast.accept(compiler)
    if verbose:
        print("[COMPILE] Shell lines:")
        for l in lines:
            print("  " + l)
    return lines