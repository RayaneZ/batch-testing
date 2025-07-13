"""
Shell code generator for the shtest compiler.

This module generates shell scripts from parsed AST nodes.
"""

from typing import List, Optional, Dict, Any
from shtest_compiler.ast.visitor import ASTVisitor
from shtest_compiler.ast.shtest_to_shellframework_visitor import ShtestToShellFrameworkVisitor
from shtest_compiler.ast.shell_framework_binder import ShellFrameworkBinder
from shtest_compiler.ast.shellframework_to_shellscript_visitor import ShellFrameworkToShellScriptVisitor
from shtest_compiler.ast.shell_script_ast import ShellScript
from shtest_compiler.core.context import CompileContext
from ..parser.shtest_ast import ShtestFile, Action, TestStep
from .atomic_compiler import compile_atomic
from .matcher_registry import MatcherRegistry
from ..config.debug_config import is_debug_enabled, debug_print
import re
import yaml
import os
import importlib
from .argument_extractor import extract_action_args
from ..parser.shunting_yard import parse_validation_expression, Atomic, BinaryOp
import traceback


def canonize_action(action: str) -> Optional[tuple]:
    """
    Canonicalize an action command to find the appropriate handler.
    Returns (canonical_phrase, handler_name, pattern_entry) or None if not found
    """
    patterns_path = os.path.join(os.path.dirname(__file__), "../config/patterns_actions.yml")
    if not os.path.exists(patterns_path):
        return None
    
    with open(patterns_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
        action_patterns = data.get("actions", [])
    
    action_lower = action.lower().strip()
    
    for pattern_entry in action_patterns:
        # Check exact phrase match
        if pattern_entry["phrase"].lower() == action_lower:
            return (
                pattern_entry["phrase"],
                pattern_entry["handler"],
                pattern_entry
            )
        # Check aliases
        for alias in pattern_entry.get("aliases", []):
            # Skip if alias is not a string
            if not isinstance(alias, str):
                continue
            if alias.lower() == action_lower:
                return (
                    pattern_entry["phrase"],
                    pattern_entry["handler"],
                    pattern_entry
                )
            # Handle regex patterns
            if alias.startswith("^") and alias.endswith("$"):
                try:
                    if re.match(alias, action_lower, re.IGNORECASE):
                        return (
                            pattern_entry["phrase"],
                            pattern_entry["handler"],
                            pattern_entry
                        )
                except re.error:
                    continue
    
    return None


def canonize_validation(validation: str) -> Optional[tuple]:
    """
    Canonicalize a validation expression to find the appropriate matcher.
    Returns (canonical_phrase, handler_name, scope, pattern_entry, groups) or None if not found.
    """
    patterns_path = os.path.join(os.path.dirname(__file__), "../config/patterns_validations.yml")
    if not os.path.exists(patterns_path):
        return None
    
    with open(patterns_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
        validation_patterns = data.get("validations", [])
    
    validation_lower = validation.lower().strip()
    
    for pattern_entry in validation_patterns:
        # Check exact phrase match
        if pattern_entry["phrase"].lower() == validation_lower:
            return (
                pattern_entry["phrase"],
                pattern_entry["handler"],
                pattern_entry.get("scope", "global"),
                pattern_entry,
                [] # Groups will be extracted later
            )
        # Check aliases
        for alias in pattern_entry.get("aliases", []):
            # Skip if alias is not a string
            if not isinstance(alias, str):
                continue
            if alias.lower() == validation_lower:
                return (
                    pattern_entry["phrase"],
                    pattern_entry["handler"],
                    pattern_entry.get("scope", "global"),
                    pattern_entry,
                    [] # Groups will be extracted later
                )
            # Handle regex patterns
            if alias.startswith("^") and alias.endswith("$"):
                try:
                    if re.match(alias, validation_lower, re.IGNORECASE):
                        return (
                            pattern_entry["phrase"],
                            pattern_entry["handler"],
                            pattern_entry.get("scope", "global"),
                            pattern_entry,
                            [] # Groups will be extracted later
                        )
                except re.error:
                    continue
    
    return None


def extract_action_groups(action: str, pattern: str) -> List[str]:
    """
    Extract groups from action command using the pattern.
    
    Args:
        action: The action command
        pattern: The regex pattern to match against
        
    Returns:
        List of extracted groups
    """
    # Convert YAML pattern placeholders to regex
    regex_pattern = pattern
    regex_pattern = regex_pattern.replace("{path}", r"(.+)")
    regex_pattern = regex_pattern.replace("{src}", r"(.+)")
    regex_pattern = regex_pattern.replace("{dest}", r"(.+)")
    regex_pattern = regex_pattern.replace("{script}", r"(.+)")
    regex_pattern = regex_pattern.replace("{query}", r"(.+)")
    regex_pattern = regex_pattern.replace("{output}", r"(.+)")
    regex_pattern = regex_pattern.replace("{query1}", r"(.+)")
    regex_pattern = regex_pattern.replace("{query2}", r"(.+)")
    regex_pattern = regex_pattern.replace("{file1}", r"(.+)")
    regex_pattern = regex_pattern.replace("{file2}", r"(.+)")
    regex_pattern = regex_pattern.replace("{var}", r"(.+)")
    regex_pattern = regex_pattern.replace("{value}", r"(.+)")
    regex_pattern = regex_pattern.replace("{timestamp}", r"(.+)")
    regex_pattern = regex_pattern.replace("{mode}", r"(.+)")
    
    # Try to match the action against the pattern
    match = re.match(regex_pattern, action, re.IGNORECASE)
    if match:
        return list(match.groups())
    return []


def compile_action(action: str, extracted_args: Optional[dict] = None) -> List[str]:
    """
    Compile an action command into shell code using the plugin system.
    
    Args:
        action: The action command to compile
        extracted_args: Dict of arguments extracted from the action command
        
    Returns:
        List of shell code lines
    """
    debug_enabled = is_debug_enabled()
    
    if debug_enabled:
        debug_print(f"[DEBUG] compile_action called with: action='{action}', extracted_args={extracted_args}")
    
    # Canonicalize the action command
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
        debug_print(f"[DEBUG] Canonical action: '{phrase_canonique}' (handler: {handler}) for '{action}'")
    
    # Find matching action pattern
    matched_pattern = None
    for alias in [pattern_entry["phrase"]] + pattern_entry.get("aliases", []):
        # Skip if alias is not a string
        if not isinstance(alias, str):
            continue
        if alias.lower() == action.lower().strip():
            matched_pattern = alias
            break
        # Handle regex patterns
        if alias.startswith("^") and alias.endswith("$"):
            try:
                if re.match(alias, action.lower().strip(), re.IGNORECASE):
                    matched_pattern = alias
                    break
            except re.error:
                continue
    
    if not matched_pattern:
        # Fallback to raw command execution
        if debug_enabled:
            debug_print(f"[DEBUG] No action pattern matched, using raw command execution")
        escaped_action = action.replace('"', '\\"')
        return [
            f"# Execute: {action}",
            f'echo "Executing: {escaped_action}"',
            f"stdout=$({action} 2>&1)",
            "last_ret=$?",
            "",
        ]
    
    # Extract action groups from the matched pattern
    groups = extract_action_groups(action, matched_pattern)
    if debug_enabled:
        debug_print(f"[DEBUG] extract_action_groups result: {groups}")
    
    # Try to import and use the core handler first
    try:
        if debug_enabled:
            debug_print(f"[DEBUG] Trying to import core handler: shtest_compiler.core.handlers.{handler}")
        core_module = importlib.import_module(f"shtest_compiler.core.handlers.{handler}")
        if hasattr(core_module, 'handle'):
            params = {
                'groups': groups,
                'canonical_phrase': phrase_canonique
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
                return [f"echo 'ERROR: Invalid return type from core handler {handler}'"]
        else:
            return [f"echo 'ERROR: Core handler {handler} does not have handle method'"]
    except ImportError as e:
        if debug_enabled:
            debug_print(f"[DEBUG] Core handler ImportError: {e}")
        # Fallback to plugin
        try:
            if debug_enabled:
                debug_print(f"[DEBUG] Trying to import plugin: shtest_compiler.plugins.{handler}")
            plugin_module = importlib.import_module(f"shtest_compiler.plugins.{handler}")
            if hasattr(plugin_module, 'handle'):
                action_obj = plugin_module.handle(groups)
                if hasattr(action_obj, 'to_shell'):
                    import inspect
                    sig = inspect.signature(action_obj.to_shell)
                    param_names = list(sig.parameters.keys())
                    kwargs = {}
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
                        return [f"echo 'ERROR: Invalid return type from plugin {handler}'"]
                else:
                    return [f"echo 'ERROR: Plugin {handler} does not have to_shell method'"]
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
            # Step 2: Bind helpers and calls
            shellframework_ast = ShellFrameworkBinder(shellframework_ast).bind()
            # Step 3: ShellFrameworkAST -> ShellScript
            shellscript_ast = ShellFrameworkToShellScriptVisitor().visit(shellframework_ast)
            # Step 4: Emit shell script
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
        raise NotImplementedError(f"No visit_{type(node).__name__} method implemented in ShellGenerator")

