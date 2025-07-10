
from .lexer import lex_file
from .parser import Parser
from .shunting_yard import parse_validation_expression
from .shtest_ast import ShtestFile, TestStep, Action

def parse_shtest_file(path: str) -> ShtestFile:
    parser = Parser()
    steps = []
    current_step = None

    for token in lex_file(path):
        if token.kind == "STEP":
            if current_step:
                steps.append(current_step)
            current_step = TestStep(name=token.value, lineno=token.lineno, actions=[])
        elif token.kind in ("ACTION_RESULT", "ACTION_ONLY", "RESULT_ONLY"):
            if current_step is None:
                raise ValueError(f"{path}:{token.lineno}: action ou résultat sans étape")
            cmd = token.value
            res_expr = token.result if token.kind == "ACTION_RESULT" else (
                token.value if token.kind == "RESULT_ONLY" else None
            )
            res_ast = parse_validation_expression(res_expr) if res_expr else None
            action = Action(
                command=cmd,
                result_expr=res_expr,
                result_ast=res_ast,
                lineno=token.lineno,
                raw_line=token.original
            )
            current_step.actions.append(action)
        elif token.kind == "TEXT":
            raise ValueError(f"{path}:{token.lineno}: ligne non reconnue -> {token.value}")

    if current_step:
        steps.append(current_step)

    return ShtestFile(steps=steps)
