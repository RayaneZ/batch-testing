import argparse
import os
import re
from glob import glob
from openpyxl import Workbook
from validation_ast import (
    Atomic,
    BinaryOp,
    parse_validation_expression,
)


_PREC = {"et": 2, "ou": 1}


def _ast_to_str(node: BinaryOp | Atomic, parent_op: str | None = None) -> str:
    """Return a canonical string representation of a validation AST node."""
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
    """Convert a result expression to its alias-only canonical form."""
    ast = parse_validation_expression(result.rstrip('.;').strip())
    return _ast_to_str(ast)

# This script reads all ``.shtest`` files in a directory and produces an
# Excel workbook summarising each test case.


def parse_shtest_file(path: str):
    """Parse a ``.shtest`` file and return a list of steps."""

    step_re = re.compile(r"^(?:Étape|Etape|Step)\s*:\s*(.*)", re.IGNORECASE)
    action_re = re.compile(
        r"^Action\s*:\s*(.*?)\s*;\s*(?:Résultat|Resultat)\s*:?\s*(.*)",
        re.IGNORECASE,
    )
    steps = []
    current = {"name": "", "actions": [], "expected": [], "obtained": []}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Lines starting with "Étape:" mark a new logical step
            m = step_re.match(line)
            if m:
                if current["actions"] or current["expected"]:
                    steps.append(current)
                current = {
                    "name": m.group(1).strip(),
                    "actions": [],
                    "expected": [],
                    "obtained": [],
                }
                continue
            m = action_re.match(line)
            if m:
                current["actions"].append(m.group(1).strip())
                result = canonicalize_result(m.group(2).strip())
                current["expected"].append(result)
    if current["actions"] or current["expected"]:
        steps.append(current)
    return steps


def export_tests_to_excel(input_dir: str, output_file: str) -> None:
    """Generate an Excel summary from all ``.shtest`` files in *input_dir*."""

    wb = Workbook()
    ws = wb.active
    ws.title = "Tests"
    ws.append(["Test Name", "Actions", "Expected Results", "Actual Results"])

    for path in glob(os.path.join(input_dir, "*.shtest")):
        test_name = os.path.splitext(os.path.basename(path))[0]
        for step in parse_shtest_file(path):
            actions = "\n".join(step["actions"])
            if step["name"]:
                # Prepend the step name when available
                actions = f"Step: {step['name']}\n" + actions
            expected = "\n".join(step["expected"])
            obtained = "\n".join(step["obtained"])
            ws.append([test_name, actions, expected, obtained])

    wb.save(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Export .shtest files to an Excel summary"
    )
    parser.add_argument(
        "--input-dir", default="tests", help="Directory containing .shtest files"
    )
    parser.add_argument(
        "--output", default="tests_summary.xlsx", help="Path to the output Excel file"
    )
    args = parser.parse_args()

    # Build the workbook from the provided directory
    export_tests_to_excel(args.input_dir, args.output)
