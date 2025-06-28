from .ast_compiler import compile_ast
from parser.shunting_yard import parse_validation_expression

def compile_validation(expression: str, counter=None):
    ast = parse_validation_expression(expression)
    if counter is None:
        counter = [0]
    last_file_var = [None]
    lines, final_var = compile_ast(ast, counter, last_file_var)

    lines.extend([
        f"verdict=\"KO\"",
        f"if [ ${{{final_var}}} -eq 1 ]; then verdict=\"OK\"; fi",
        "expected=\"OK\"",
        "log_diff \"$expected\" \"$verdict\""
    ])
    return lines