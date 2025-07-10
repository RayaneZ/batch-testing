import os
import re
from glob import glob
from openpyxl import Workbook
from src.shtest_compiler.parser.lexer import lex_file
from shtest_compiler.parser.shunting_yard import Atomic, BinaryOp, parse_validation_expression

_PREC = {"et": 2, "ou": 1}

def _ast_to_str(node: BinaryOp | Atomic, parent_op: str | None = None) -> str:
    if isinstance(node, Atomic):
        return node.value
    if isinstance(node, BinaryOp):
        left = _ast_to_str(node.left, node.op)
        right = _ast_to_str(node.right, node.op)
        expr = f"{left} {node.op} {right}"
        if parent_op and _PREC[node.op] < _PREC[parent_op]:
            return f"({expr})"
        return expr
    return ""

def canonicalize_result(result: str) -> str:
    ast = parse_validation_expression(result.rstrip('.;').strip())
    return _ast_to_str(ast)

def sanitize_action(action: str) -> str:
    return re.sub(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[A-Za-z0-9_.-]+",
        "<credentials>",
        action,
    )

def parse_shtest_file(path: str):
    steps = []
    current = {"name": "", "actions": [], "obtained": []}
    step_count = 1
    for token in lex_file(path):
        if token.kind == "STEP":
            if current["actions"]:
                if not current["name"]:
                    current["name"] = f"Step {step_count}"
                steps.append(current)
                step_count += 1
            current = {"name": token.value, "actions": [], "obtained": []}
        elif token.kind in ("ACTION_RESULT", "ACTION_ONLY"):
            action = sanitize_action(token.value)
            current["actions"].append(action)
            if token.kind == "ACTION_RESULT" and token.result:
                current["obtained"].append(canonicalize_result(token.result))
    if current["actions"]:
        if not current["name"]:
            current["name"] = f"Step {step_count}"
        steps.append(current)
    return steps

def export_tests_to_excel(input_dir: str, output_file: str) -> None:
    wb = Workbook()
    wb.remove(wb.active)
    for path in sorted(glob(os.path.join(input_dir, "*.shtest"))):
        test_name = os.path.splitext(os.path.basename(path))[0]
        ws = wb.create_sheet(title=test_name)
        ws.append(["Step", "Actions", "Actual Results"])
        for step in parse_shtest_file(path):
            actions = "\n".join(step["actions"])
            obtained = "\n".join(step["obtained"])
            ws.append([step["name"], actions, obtained])
    wb.save(output_file)
