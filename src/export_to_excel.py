import argparse
import os
import re
from glob import glob
from openpyxl import Workbook
import configparser
from validation_ast import (
    Atomic,
    BinaryOp,
    parse_validation_expression,
)


_PREC = {"et": 2, "ou": 1}


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.ini")
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

DEFAULT_INPUT_DIR = config.get("application", "input_dir", fallback="src/tests")
DEFAULT_OUTPUT_FILE = "tests_summary.xlsx"


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


def sanitize_action(action: str) -> str:
    """Remove credential-like strings from an action."""
    return re.sub(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[A-Za-z0-9_.-]+",
        "<credentials>",
        action,
    )


def parse_shtest_file(path: str):
    """Parse a ``.shtest`` file and return a list of steps."""

    step_re = re.compile(r"^(?:Étape|Etape|Step)\s*:\s*(.*)", re.IGNORECASE)
    action_re = re.compile(
        r"^Action\s*:\s*(.*?)\s*;\s*(?:Résultat|Resultat)\s*:?\s*(.*)",
        re.IGNORECASE,
    )
    steps = []
    current = {"name": "", "actions": [], "obtained": []}
    step_count = 1
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Lines starting with "Étape:" mark a new logical step
            m = step_re.match(line)
            if m:
                if current["actions"]:
                    if not current["name"]:
                        current["name"] = f"Step {step_count}"
                    steps.append(current)
                    step_count += 1
                current = {
                    "name": m.group(1).strip(),
                    "actions": [],
                    "obtained": [],
                }
                continue
            m = action_re.match(line)
            if m:
                action = sanitize_action(m.group(1).strip())
                current["actions"].append(action)
                result = m.group(2).strip()
                if result:
                    current["obtained"].append(canonicalize_result(result))
    if current["actions"]:
        if not current["name"]:
            current["name"] = f"Step {step_count}"
        steps.append(current)
    return steps


def export_tests_to_excel(input_dir: str, output_file: str) -> None:
    """Generate an Excel summary from all ``.shtest`` files in *input_dir*."""

    wb = Workbook()
    # Remove the automatically created sheet so each test gets its own
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Export .shtest files to an Excel summary"
    )
    parser.add_argument(
        "--input-dir",
        default=DEFAULT_INPUT_DIR,
        help="Directory containing .shtest files",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_FILE,
        help="Path to the output Excel file",
    )
    args = parser.parse_args()

    # Build the workbook from the provided directory
    export_tests_to_excel(args.input_dir, args.output)
