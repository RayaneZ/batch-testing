from shtest_compiler.ast.visitor import ASTVisitor
from shtest_compiler.parser.shtest_ast import ShtestFile, TestStep, Action
from shtest_compiler.ast.shell_framework_ast import ShellFrameworkAST, ShellTestStep, ShellFunctionDef, ShellFunctionCall, InlineShellCode, ValidationCheck
from shtest_compiler.compiler.atomic_compiler import compile_atomic
from collections import defaultdict
from typing import Dict, Tuple, List

class ShtestToShellFrameworkVisitor(ASTVisitor[ShellFrameworkAST]):
    def __init__(self):
        self.occurrence_counter: Dict[Tuple[str, str], int] = defaultdict(int)
        self.helper_names: Dict[Tuple[str, str], str] = {}
        self.helper_counter = 0
        self.helpers: List[ShellFunctionDef] = []
        self.steps: List[ShellTestStep] = []
        self.global_code: List[str] = []

    def visit_shtestfile(self, node: ShtestFile) -> ShellFrameworkAST:
        # First pass: count occurrences
        for step in node.steps:
            for action in step.actions:
                key = self.canonical_action_key(action)
                self.occurrence_counter[key] += 1
        # Assign helper names
        for key, count in self.occurrence_counter.items():
            if count > 1:
                self.helper_counter += 1
                self.helper_names[key] = f"helper_{self.helper_counter}"
        # Build helpers
        for key, name in self.helper_names.items():
            cmd, res = key
            if res:
                lines = compile_atomic(res, varname="result", last_file_var=None, action_context={'command': cmd})
                params = []
                self.helpers.append(ShellFunctionDef(name=name, params=params, body_lines=lines))
            else:
                lines = [f"echo 'Action: {cmd}'", f"run_action \"{cmd}\""]
                params = []
                self.helpers.append(ShellFunctionDef(name=name, params=params, body_lines=lines))
        # Build steps
        for step in node.steps:
            actions = []
            validations = []
            for action in step.actions:
                key = self.canonical_action_key(action)
                if key in self.helper_names:
                    actions.append(ShellFunctionCall(name=self.helper_names[key], args=[]))
                else:
                    if action.result_expr:
                        lines = compile_atomic(action.result_expr, varname="result", last_file_var=None, action_context={'command': action.command})
                        actions.append(InlineShellCode(code_lines=lines))
                    else:
                        lines = [f"echo 'Action: {action.command}'", f"run_action \"{action.command}\""]
                        actions.append(InlineShellCode(code_lines=lines))
            self.steps.append(ShellTestStep(name=step.name, actions=actions, validations=validations))
        # Add prologue
        self.global_code = [
            "#!/bin/bash",
            "",
            "# Generated shell script from .shtest file",
            "",
            "run_action() {",
            "    local cmd=\"$1\"",
            "    stdout=\"\"",
            "    stderr=\"\"",
            "    last_ret=0",
            "    stdout=$(eval \"$cmd\" 2>stderr.log)",
            "    last_ret=$?",
            "    if [ -s stderr.log ]; then",
            "        stderr=$(cat stderr.log)",
            "    else",
            "        stderr=\"\"",
            "    fi",
            "}",
            "",
            "validate_expect_actual() {",
            "    local expected=\"$1\"",
            "    local actual=\"$2\"",
            "    if [ \"$expected\" != \"$actual\" ]; then",
            "        echo \"Expected: $expected\"",
            "        echo \"Actual:   $actual\"",
            "        return 1",
            "    fi",
            "    return 0",
            "}",
            ""
        ]
        return ShellFrameworkAST(helpers=self.helpers, steps=self.steps, global_code=self.global_code)

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit_{type(node).__name__} method implemented in ShtestToShellFrameworkVisitor")

    def canonical_action_key(self, action: Action) -> Tuple[str, str]:
        return (action.command or "", action.result_expr or "") 