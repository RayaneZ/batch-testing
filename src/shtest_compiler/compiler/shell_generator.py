"""
Shell code generator for the shtest compiler.

This module generates shell scripts from parsed AST nodes.
"""

import importlib
import os
import re
import traceback
from typing import Any, Dict, List, Optional

import yaml

from shtest_compiler.ast.shell_framework_binder import ShellFrameworkBinder
from shtest_compiler.ast.shell_script_ast import ShellScript
from shtest_compiler.ast.shellframework_to_shellscript_visitor import \
    ShellFrameworkToShellScriptVisitor
from shtest_compiler.ast.shtest_to_shellframework_visitor import \
    ShtestToShellFrameworkVisitor
from shtest_compiler.ast.visitor import ASTVisitor
from shtest_compiler.core.context import CompileContext

from ..config.debug_config import debug_print, is_debug_enabled
from ..parser.shtest_ast import Action, ShtestFile, TestStep
from ..parser.shunting_yard import (Atomic, BinaryOp,
                                    parse_validation_expression)
from .action_utils import (canonize_action, extract_context_from_action,
                           validate_action_context)
from .argument_extractor import extract_action_args
from .atomic_compiler import compile_atomic
from .matcher_registry import MatcherRegistry


def compile_action(action: str, extracted_args: Optional[dict] = None) -> List[str]:
    """
    Compile an action command into shell code using the modular context system.

    Args:
        action: The action command to compile
        extracted_args: Dict of arguments extracted from the action command

    Returns:
        List of shell code lines
    """
    debug_enabled = is_debug_enabled()

    if debug_enabled:
        debug_print(
            f"[DEBUG] compile_action called with: action='{action}', extracted_args={extracted_args}"
        )

    # Use modular context extraction instead of manual canonization
    canon = canonize_action(action)
    if debug_enabled:
        debug_print(f"[DEBUG] canonize_action result: {canon}")

    if not canon:
        # Fallback to raw command execution
        if debug_enabled:
            debug_print(f"[DEBUG] No action handler found, using raw command execution")
        escaped_action = action.replace('"', '\\"')
        return [
            f"# Execute: {action}",
            f'echo "Executing: {escaped_action}"',
            f"stdout=$({action} 2>&1)",
            "last_ret=$?",
            "",
        ]

    phrase_canonique, handler, pattern_entry = canon
    if debug_enabled:
        debug_print(
            f"[DEBUG] Canonical action: '{phrase_canonique}' (handler: {handler}) for '{action}'"
        )

    # Extract context using the modular system
    context = extract_context_from_action(action, handler)
    if debug_enabled:
        debug_print(f"[DEBUG] extract_context_from_action result: {context}")

    # Validate the context
    is_valid, errors = validate_action_context(context)
    if not is_valid:
        error_msg = f"Action context errors for '{action}': {', '.join(errors)}"
        if debug_enabled:
            debug_print(f"[DEBUG] {error_msg}")
        return [f"echo 'ERROR: {error_msg}'"]

    # Extract variables from context
    variables = context.get("variables", {})
    if debug_enabled:
        debug_print(f"[DEBUG] Extracted variables: {variables}")

    # Try to import and use the core handler first
    try:
        if debug_enabled:
            debug_print(
                f"[DEBUG] Trying to import core handler: shtest_compiler.core.handlers.{handler}"
            )
        core_module = importlib.import_module(
            f"shtest_compiler.core.handlers.{handler}"
        )
        if hasattr(core_module, "handle"):
            # Pass the full context to the handler
            params = {
                "canonical_phrase": phrase_canonique,
                "context": context,
                # Include all extracted variables for backward compatibility
                **variables,
            }
            if extracted_args:
                params.update(extracted_args)

            result = core_module.handle(params)
            if debug_enabled:
                debug_print(f"[DEBUG] Core handler returned: {result}")
            if isinstance(result, list):
                return result
            elif isinstance(result, str):
                return [result]
            else:
                return [
                    f"echo 'ERROR: Invalid return type from core handler {handler}'"
                ]
        else:
            return [f"echo 'ERROR: Core handler {handler} does not have handle method'"]
    except ImportError as e:
        if debug_enabled:
            debug_print(f"[DEBUG] Core handler ImportError: {e}")
        # Fallback to plugin
        try:
            if debug_enabled:
                debug_print(
                    f"[DEBUG] Trying to import plugin: shtest_compiler.plugins.{handler}"
                )
            plugin_module = importlib.import_module(
                f"shtest_compiler.plugins.{handler}"
            )
            if hasattr(plugin_module, "handle"):
                # For plugins, we need to maintain backward compatibility
                # Extract groups from variables for plugin compatibility
                groups = list(variables.values())
                action_obj = plugin_module.handle(groups)
                if hasattr(action_obj, "to_shell"):
                    import inspect

                    sig = inspect.signature(action_obj.to_shell)
                    param_names = list(sig.parameters.keys())
                    kwargs = {}
                    # Pass variables as kwargs if they match parameter names
                    for k, v in variables.items():
                        if k in param_names:
                            kwargs[k] = v
                    if extracted_args:
                        for k, v in extracted_args.items():
                            if k in param_names:
                                kwargs[k] = v
                    matched = action_obj.to_shell(**kwargs)
                    if isinstance(matched, list):
                        return matched
                    elif isinstance(matched, str):
                        return [matched]
                    else:
                        return [
                            f"echo 'ERROR: Invalid return type from plugin {handler}'"
                        ]
                else:
                    return [
                        f"echo 'ERROR: Plugin {handler} does not have to_shell method'"
                    ]
            else:
                return [f"echo 'ERROR: Plugin {handler} does not have handle method'"]
        except ImportError as e:
            if debug_enabled:
                debug_print(f"[DEBUG] Plugin ImportError: {e}")
            return [f"echo 'ERROR: Could not import handler or plugin {handler}: {e}'"]
        except Exception as e:
            if debug_enabled:
                debug_print(f"[DEBUG] Exception in plugin {handler}: {e}")
            return [f"echo 'ERROR: Exception in plugin {handler}: {e}'"]
    except Exception as e:
        if debug_enabled:
            debug_print(f"[DEBUG] Exception in core handler {handler}: {e}")
        return [f"echo 'ERROR: Exception in core handler {handler}: {e}'"]
    return [f"echo 'ERROR: No handler found for action: {action}'"]


class ShellGenerator(ASTVisitor):
    """Generates shell code from AST nodes using the new visitor-based pipeline."""

    def __init__(self, debug_output_path: str = None):
        self.debug_output_path = debug_output_path

    def visit(self, node) -> str:
        try:
            # Step 1: Shtest AST -> ShellFrameworkAST
            shellframework_ast = ShtestToShellFrameworkVisitor().visit(node)
            # Step 2: Lift global validations from action results to standalone validations
            from shtest_compiler.ast.shell_framework_binder import \
                ShellFrameworkLifter

            shellframework_ast = ShellFrameworkLifter(shellframework_ast).lift()
            # Step 3: Bind helpers and calls
            shellframework_ast = ShellFrameworkBinder(shellframework_ast).bind()
            # Step 4: ShellFrameworkAST -> ShellScript
            shellscript_ast = ShellFrameworkToShellScriptVisitor().visit(
                shellframework_ast
            )
            # Step 5: Emit shell script
            return "\n".join(shellscript_ast.lines)
        except Exception as e:
            error_msg = f"[ERROR] {type(e).__name__}: {e}"
            import traceback

            stack = traceback.format_exc()
            debug_print(error_msg)
            debug_print(stack)
            print(error_msg)
            return f'echo "{error_msg}"\nexit 1'

    def generic_visit(self, node):
        raise NotImplementedError(
            f"No visit_{type(node).__name__} method implemented in ShellGenerator"
        )
