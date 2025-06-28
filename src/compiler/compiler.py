from .ast_compiler import compile_ast
from parser.shunting_yard import parse_validation_expression

def compile_validation(expression: str):
    ast = parse_validation_expression(expression)
    counter = [0]
    last_file_var = [None]
    lines, final_var = compile_ast(ast, counter, last_file_var)

    lines.extend([
        f"if [ ${{{final_var}}} -eq 1 ]; then actual=\"OK\"; else actual=\"KO\"; fi",
        "expected=\"OK\"",
        "log_diff \"$expected\" \"$actual\""
    ])
    return lines