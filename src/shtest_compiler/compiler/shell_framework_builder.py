from collections import defaultdict
from typing import Dict, List, Tuple

from shtest_compiler.ast.shell_framework_ast import (InlineShellCode,
                                                     ShellFrameworkAST,
                                                     ShellFunctionCall,
                                                     ShellFunctionDef,
                                                     ShellTestStep,
                                                     ValidationCheck)
from shtest_compiler.parser.shtest_ast import Action, ShtestFile, TestStep

from .argument_extractor import extract_action_args
from .atomic_compiler import compile_atomic

# Helper to create a canonical key for an action/validation
# For now, use command/result_expr as the key; can be improved for argument normalization


def canonical_action_key(action: Action) -> Tuple[str, str]:
    return (action.command or "", action.result_expr or "")


# Helper to extract parameters from command/result_expr
def extract_params(action: Action):
    if not action.command:
        return []

    # Try to extract parameters from the action command
    extracted = extract_action_args(action.command)
    if extracted:
        # Return parameter names in order they appear
        return list(extracted.keys())
    return []


def build_shell_framework_ast(shtest_ast: ShtestFile) -> ShellFrameworkAST:
    # 1. Count occurrences of each unique action/validation
    occurrence_counter: Dict[Tuple[str, str], int] = defaultdict(int)
    for step in shtest_ast.steps:
        for action in step.actions:
            key = canonical_action_key(action)
            occurrence_counter[key] += 1

    # 2. Assign function names to repeated actions/validations
    helper_names: Dict[Tuple[str, str], str] = {}
    helper_counter = 0
    for key, count in occurrence_counter.items():
        if count > 1:
            helper_counter += 1
            helper_names[key] = f"helper_{helper_counter}"

    # 3. Build helpers and steps
    helpers: List[ShellFunctionDef] = []
    steps: List[ShellTestStep] = []

    # Generate helper function bodies
    for key, name in helper_names.items():
        cmd, res = key
        # Extract parameters from the action command
        params = extract_params(
            Action(command=cmd, result_expr=res, result_ast=None, lineno=0)
        )

        # Use compile_atomic to generate shell code for the validation (if present)
        if res:
            # Translate the action command to shell command
            shell_cmd = translate_command(cmd)
            # Generate action execution first
            action_lines = [f"echo 'Action: {cmd}'", f'run_action "{shell_cmd}"']
            # Then generate validation
            validation_lines = compile_atomic(
                res,
                varname="result",
                last_file_var=None,
                action_context={"command": cmd},
            )
            # Combine action and validation
            all_lines = action_lines + validation_lines
            helpers.append(
                ShellFunctionDef(name=name, params=params, body_lines=all_lines)
            )
        else:
            # For actions, just echo and run the command
            shell_cmd = translate_command(cmd)
            lines = [f"echo 'Action: {cmd}'", f'run_action "{shell_cmd}"']
            helpers.append(ShellFunctionDef(name=name, params=params, body_lines=lines))

    for step in shtest_ast.steps:
        actions = []
        validations = []
        for action in step.actions:
            key = canonical_action_key(action)
            if key in helper_names:
                # Extract arguments from the action for the helper call
                extracted = (
                    extract_action_args(action.command) if action.command else {}
                )
                args = [extracted.get(param, "") for param in extract_params(action)]
                actions.append(ShellFunctionCall(name=helper_names[key], args=args))
            else:
                # Inline code for unique actions/validations
                if action.result_expr:
                    # Translate the action command to shell command
                    shell_cmd = (
                        translate_command(action.command)
                        if action.command
                        else action.command
                    )
                    # Generate action execution first
                    action_lines = [
                        f"echo 'Action: {action.command}'",
                        f'run_action "{shell_cmd}"',
                    ]
                    # Then generate validation
                    validation_lines = compile_atomic(
                        action.result_expr,
                        varname="result",
                        last_file_var=None,
                        action_context={"command": action.command},
                    )
                    # Combine action and validation
                    all_lines = action_lines + validation_lines
                    actions.append(InlineShellCode(code_lines=all_lines))
                else:
                    shell_cmd = (
                        translate_command(action.command)
                        if action.command
                        else action.command
                    )
                    lines = [
                        f"echo 'Action: {action.command}'",
                        f'run_action "{shell_cmd}"',
                    ]
                    actions.append(InlineShellCode(code_lines=lines))
        steps.append(
            ShellTestStep(name=step.name, actions=actions, validations=validations)
        )

    # Add a standard shell prologue to global_code
    global_code = [
        "#!/bin/bash",
        "",
        "# Generated shell script from .shtest file",
        "",
        "run_action() {",
        '    local cmd="$1"',
        '    stdout=""',
        '    stderr=""',
        "    last_ret=0",
        '    stdout=$(eval "$cmd" 2>stderr.log)',
        "    last_ret=$?",
        "    if [ -s stderr.log ]; then",
        "        stderr=$(cat stderr.log)",
        "    else",
        '        stderr=""',
        "    fi",
        "}",
        "",
        "log_diff() {",
        '    local expected="$1"',
        '    local actual="$2"',
        '    if [ "$expected" != "$actual" ]; then',
        '        echo "Expected: $expected"',
        '        echo "Actual:   $actual"',
        "    fi",
        "}",
        "",
    ]

    return ShellFrameworkAST(helpers=helpers, steps=steps, global_code=global_code)
