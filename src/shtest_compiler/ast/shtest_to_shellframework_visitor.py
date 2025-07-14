from shtest_compiler.ast.visitor import ASTVisitor
from shtest_compiler.parser.shtest_ast import ShtestFile, TestStep, Action
from shtest_compiler.ast.shell_framework_ast import ShellFrameworkAST, ShellTestStep, ShellFunctionDef, ShellFunctionCall, InlineShellCode, ValidationCheck
from shtest_compiler.compiler.atomic_compiler import compile_atomic
from shtest_compiler.compiler.action_utils import extract_context_from_action, validate_action_context, canonize_action
from shtest_compiler.parser.shunting_yard import parse_validation_expression
from shtest_compiler.ast.shellframework_to_shellscript_visitor import ShellFrameworkToShellScriptVisitor
import importlib
from collections import defaultdict
from typing import Dict, Tuple, List
from shtest_compiler.config.debug_config import is_debug_enabled, debug_print

class ShtestToShellFrameworkVisitor(ASTVisitor[ShellFrameworkAST]):
    def __init__(self):
        self.occurrence_counter: Dict[Tuple[str, str], int] = defaultdict(int)
        self.helper_names: Dict[Tuple[str, str], str] = {}
        self.helper_counter = 0
        self.helpers: List[ShellFunctionDef] = []
        self.steps: List[ShellTestStep] = []
        self.global_code: List[str] = []

    def shell_escape_command(self, cmd):
        """Escape a shell command for use in double-quoted strings"""
        if cmd is None:
            return ''
        # Escape double quotes and backslashes
        return str(cmd).replace('\\', '\\\\').replace('"', '\\"')

    def extract_params(self, action: Action):
        if not action.command:
            return []
        # Use modular context extraction
        context = extract_context_from_action(action.command, self.get_handler_name(action.command))
        variables = context.get('variables', {})
        return list(variables.keys())

    def get_handler_name(self, action_command):
        context = extract_context_from_action(action_command, None)
        return context.get('handler')

    def get_action_shell_command(self, action_command):
        debug_enabled = is_debug_enabled()
        if debug_enabled:
            debug_print(f"[DEBUG] get_action_shell_command called with: '{action_command}'")
        
        # Use canonize_action to get the handler
        canon = canonize_action(action_command)
        if canon is None:
            if debug_enabled:
                debug_print(f"[DEBUG] get_action_shell_command: canonize_action returned None for '{action_command}'")
            return action_command  # fallback: raw command
        phrase, handler, pattern_entry = canon
        if debug_enabled:
            debug_print(f"[DEBUG] get_action_shell_command: canonize_action matched handler '{handler}' for phrase '{phrase}'")
        
        context = extract_context_from_action(action_command, handler)
        if debug_enabled:
            debug_print(f"[DEBUG] get_action_shell_command: context={context}")
        
        is_valid, errors = validate_action_context(context)
        if not is_valid:
            if debug_enabled:
                debug_print(f"[DEBUG] get_action_shell_command: context validation failed: {errors}")
            return action_command  # fallback: raw command
        
        variables = context.get('variables', {})
        if debug_enabled:
            debug_print(f"[DEBUG] get_action_shell_command: handler={handler}, variables={variables}")
        
        try:
            # Try action handlers first (for actions)
            try:
                if debug_enabled:
                    debug_print(f"[DEBUG] get_action_shell_command: Trying action handler: shtest_compiler.core.action_handlers.{handler}")
                core_module = importlib.import_module(f"shtest_compiler.core.action_handlers.{handler}")
                if hasattr(core_module, 'handle'):
                    params = {'context': context, **variables}
                    if debug_enabled:
                        debug_print(f"[DEBUG] get_action_shell_command: Calling action handler with params={params}")
                    result = core_module.handle(params)
                    if debug_enabled:
                        debug_print(f"[DEBUG] get_action_shell_command: Action handler returned={result}")
                    if hasattr(result, 'to_shell'):
                        shell_cmd = result.to_shell()
                        if debug_enabled:
                            debug_print(f"[DEBUG] get_action_shell_command: Generated shell command: {shell_cmd}")
                        return shell_cmd
                    elif isinstance(result, str):
                        if debug_enabled:
                            debug_print(f"[DEBUG] get_action_shell_command: Handler returned string: {result}")
                        return result
                    else:
                        if debug_enabled:
                            debug_print(f"[DEBUG] get_action_shell_command: Invalid return type from action handler")
                        return action_command
            except ImportError as e:
                if debug_enabled:
                    debug_print(f"[DEBUG] get_action_shell_command: Action handler ImportError: {e}")
                # Fallback to validation handlers (for validations)
                try:
                    if debug_enabled:
                        debug_print(f"[DEBUG] get_action_shell_command: Trying validation handler: shtest_compiler.core.handlers.{handler}")
                    core_module = importlib.import_module(f"shtest_compiler.core.handlers.{handler}")
                    if hasattr(core_module, 'handle'):
                        params = {'context': context, **variables}
                        result = core_module.handle(params)
                        if debug_enabled:
                            debug_print(f"[DEBUG] get_action_shell_command: Validation handler returned={result}")
                        if hasattr(result, 'actual_cmd'):
                            return result.actual_cmd
                        elif isinstance(result, str):
                            return result
                        else:
                            return action_command
                except ImportError as e:
                    if debug_enabled:
                        debug_print(f"[DEBUG] get_action_shell_command: Validation handler ImportError: {e}")
                    return action_command
        except Exception as e:
            if debug_enabled:
                debug_print(f"[DEBUG] get_action_shell_command: Exception: {e}")
            return action_command

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
            params = self.extract_params(Action(command=cmd, result_expr=res, result_ast=None, lineno=0))
            if res:
                shell_cmd = self.get_action_shell_command(cmd)
                action_lines = [f"echo 'Action: {cmd}'", f"run_action \"{self.shell_escape_command(shell_cmd)}\""]
                # Use parse_validation_expression for compound validations
                validation_lines = self.compile_validation_expression(res, action_context={'command': cmd})
                all_lines = action_lines + validation_lines
                self.helpers.append(ShellFunctionDef(name=name, params=params, body_lines=all_lines))
            else:
                shell_cmd = self.get_action_shell_command(cmd)
                lines = [f"echo 'Action: {cmd}'", f"run_action \"{self.shell_escape_command(shell_cmd)}\""]
                self.helpers.append(ShellFunctionDef(name=name, params=params, body_lines=lines))
        # Build steps
        for step in node.steps:
            actions = []
            validations = []
            for action in step.actions:
                key = self.canonical_action_key(action)
                if key in self.helper_names:
                    context = extract_context_from_action(action.command, self.get_handler_name(action.command))
                    variables = context.get('variables', {})
                    args = [variables.get(param, "") for param in self.extract_params(action)]
                    actions.append(ShellFunctionCall(name=self.helper_names[key], args=args))
                else:
                    if action.result_expr:
                        shell_cmd = self.get_action_shell_command(action.command) if action.command else action.command
                        action_lines = [f"echo 'Action: {action.command}'", f"run_action \"{self.shell_escape_command(shell_cmd)}\""]
                        # Use parse_validation_expression for compound validations
                        validation_lines = self.compile_validation_expression(action.result_expr, action_context={'command': action.command})
                        all_lines = action_lines + validation_lines
                        actions.append(InlineShellCode(code_lines=all_lines))
                    else:
                        shell_cmd = self.get_action_shell_command(action.command) if action.command else action.command
                        lines = [f"echo 'Action: {action.command}'", f"run_action \"{self.shell_escape_command(shell_cmd)}\""]
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
            "    return $last_ret",
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

    def compile_validation_expression(self, expression: str, action_context: dict = None) -> List[str]:
        """Compile a validation expression, handling both atomic and compound expressions."""
        debug_enabled = is_debug_enabled()
        if debug_enabled:
            debug_print(f"[DEBUG] compile_validation_expression called with: '{expression}'")
        # Check if the expression contains logical operators
        if ' et ' in expression or ' ou ' in expression or '(' in expression or ')' in expression:
            # This is a compound expression, use the shunting yard parser
            if debug_enabled:
                debug_print(f"[DEBUG] compile_validation_expression: Detected compound expression, using parse_validation_expression")
            try:
                ast = parse_validation_expression(expression)
                if debug_enabled:
                    debug_print(f"[DEBUG] compile_validation_expression: AST={ast}")
                visitor = ShellFrameworkToShellScriptVisitor()
                shell_lines = visitor.visit(ast)
                if debug_enabled:
                    debug_print(f"[DEBUG] compile_validation_expression: Generated {len(shell_lines)} shell lines for compound expression")
                return shell_lines
            except Exception as e:
                if debug_enabled:
                    debug_print(f"[DEBUG] compile_validation_expression: Error parsing compound expression: {e}")
                # Fallback to atomic compilation
                return compile_atomic(expression, varname="result", last_file_var=None, action_context=action_context)
        else:
            # This is an atomic expression, use compile_atomic
            if debug_enabled:
                debug_print(f"[DEBUG] compile_validation_expression: Detected atomic expression, using compile_atomic")
            return compile_atomic(expression, varname="result", last_file_var=None, action_context=action_context)

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit_{type(node).__name__} method implemented in ShtestToShellFrameworkVisitor")

    def canonical_action_key(self, action: Action) -> Tuple[str, str]:
        return (action.command or "", action.result_expr or "") 