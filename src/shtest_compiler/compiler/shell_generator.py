"""
Shell code generator for the shtest compiler.

This module generates shell scripts from parsed AST nodes.
"""

from typing import List, Optional, Dict, Any
from ..core.visitor import ASTVisitor
from ..core.context import CompileContext
from ..parser.shtest_ast import ShtestFile, Action, TestStep
from .atomic_compiler import compile_atomic
from .matcher_registry import MatcherRegistry
from ..config.debug_config import is_debug_enabled, debug_print
import re
import yaml
import os
import importlib
from .argument_extractor import extract_action_args


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
        return [
            f"# Execute: {action}",
            f'echo "Executing: {action}"',
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
        return [
            f"# Execute: {action}",
            f'echo "Executing: {action}"',
            f"stdout=$({action} 2>&1)",
            "last_ret=$?",
            "",
        ]
    
    # Extract action groups from the matched pattern
    groups = extract_action_groups(action, matched_pattern)
    if debug_enabled:
        debug_print(f"[DEBUG] extract_action_groups result: {groups}")
    
    # Try to import and use the action plugin
    try:
        if debug_enabled:
            debug_print(f"[DEBUG] Trying to import plugin: shtest_compiler.plugins.{handler}")
        
        plugin_module = importlib.import_module(f"shtest_compiler.plugins.{handler}")
        if debug_enabled:
            debug_print(f"[DEBUG] Plugin imported successfully: {plugin_module}")
        
        # Check if plugin has handle method
        if hasattr(plugin_module, 'handle'):
            if debug_enabled:
                debug_print(f"[DEBUG] Plugin has handle method, calling with groups={groups}")
            
            action_obj = plugin_module.handle(groups)
            if debug_enabled:
                debug_print(f"[DEBUG] Plugin handle returned: {action_obj}")
            
            # Check if action object has to_shell method
            if hasattr(action_obj, 'to_shell'):
                import inspect
                sig = inspect.signature(action_obj.to_shell)
                param_names = list(sig.parameters.keys())
                if debug_enabled:
                    debug_print(f"[DEBUG] to_shell signature: {sig}, param_names: {param_names}")
                
                # Prepare arguments for to_shell
                kwargs = {}
                # Pass extracted_args if plugin expects them
                if extracted_args:
                    for k, v in extracted_args.items():
                        if k in param_names:
                            kwargs[k] = v
                
                # Call to_shell with appropriate parameters
                matched = action_obj.to_shell(**kwargs)
                if debug_enabled:
                    debug_print(f"[DEBUG] Generated shell code: {matched}")
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
            debug_print(f"[DEBUG] ImportError: {e}")
        # Fallback to raw command execution
        return [
            f"# Execute: {action}",
            f'echo "Executing: {action}"',
            f"stdout=$({action} 2>&1)",
            "last_ret=$?",
            "",
        ]
    except Exception as e:
        if debug_enabled:
            debug_print(f"[DEBUG] Exception in plugin {handler}: {e}")
        # Fallback to raw command execution
        return [
            f"# Execute: {action}",
            f'echo "Executing: {action}"',
            f"stdout=$({action} 2>&1)",
            "last_ret=$?",
            "",
        ]


class ShellGenerator(ASTVisitor):
    """Generates shell code from AST nodes."""
    
    def __init__(self):
        """Initialize the shell generator."""
        self.context = CompileContext()
        self.matcher_registry = MatcherRegistry()
        self.last_file_var = None
        self.last_action_valids = []
        self.global_valids = []
    
    def visit(self, node) -> str:
        """Visit a node and generate shell code."""
        if isinstance(node, ShtestFile):
            return self.visit_shtest_file(node)
        elif isinstance(node, TestStep):
            return self.visit_test_step(node)
        elif isinstance(node, Action):
            return self.visit_action(node)
        else:
            return f"# Unknown node type: {type(node).__name__}"
    
    def visit_shtest_file(self, node: ShtestFile) -> str:
        """Generate shell code for a shtest file."""
        lines = [
            "#!/bin/bash",
            "",
            "# Generated shell script from .shtest file",
            "",
            "# Function to log differences",
            "log_diff() {",
            "    local expected=\"$1\"",
            "    local actual=\"$2\"",
            "    if [ \"$expected\" != \"$actual\" ]; then",
            "        echo \"Expected: $expected\"",
            "        echo \"Actual: $actual\"",
            "    fi",
            "}",
            "",
            "# Initialize variables",
            "last_ret=0",
            "test_passed=true",
            "",
        ]
        
        # Process test steps
        for step in node.steps:
            step_code = self.visit_test_step(step)
            lines.extend(step_code.split('\n'))
            lines.append("")
        
        # Add final result check
        lines.extend([
            "# Final result",
            "if [ \"$test_passed\" = true ]; then",
            "    echo \"Test passed\"",
            "    exit 0",
            "else",
            "    echo \"Test failed\"",
            "    exit 1",
            "fi",
        ])
        
        return '\n'.join(lines)
    
    def visit_test_step(self, node: TestStep) -> str:
        """Generate shell code for a test step."""
        if is_debug_enabled():
            debug_print(f"[DEBUG] Shell generator: Visiting test step: {node.name}")
        
        lines = [
            f"# Test step: {node.name}",
        ]
        
        # Process actions in the test step
        for action in node.actions:
            if is_debug_enabled():
                debug_print(f"[DEBUG] Shell generator: Visiting action: command='{action.command}', result_expr='{action.result_expr}'")
            
            action_code = self.visit_action(action)
            lines.extend(action_code)
            lines.append("")
        
        return '\n'.join(lines)
    
    def visit_action(self, action: Action) -> List[str]:
        """Visit an action node and generate shell code."""
        if is_debug_enabled():
            debug_print(f"[DEBUG] Shell generator: visit_action called with command='{action.command}', result_expr='{action.result_expr}'")
        
        lines = []
        extracted_args = None
        
        # Generate command execution using plugin system
        if action.command:
            # Extract arguments from the action command
            extracted_args = extract_action_args(action.command)
            if is_debug_enabled():
                debug_print(f"[DEBUG] Extracted arguments from action: {extracted_args}")
            
            # Compile action using plugin system
            action_lines = compile_action(action.command, extracted_args)
            lines.extend(action_lines)
        
        # Generate validation if present
        if action.result_expr:
            validation_lines = self._generate_validation(action, extracted_args)
            lines.extend(validation_lines)
        
        return lines
    
    def _generate_validation(self, node: Action, extracted_args=None) -> List[str]:
        """Generate validation code for an action."""
        if is_debug_enabled():
            debug_print(f"[DEBUG] Shell generator: Processing result_expr: '{node.result_expr}'")
        
        lines = []
        try:
            # Parse validation expression
            validation_ast = self._parse_validation(node.result_expr)
            if is_debug_enabled():
                debug_print(f"[DEBUG] Shell generator: validation_ast = {validation_ast}")
            
            # Get validation expressions
            last_action_valids = self.last_action_valids
            global_valids = self.global_valids
            if is_debug_enabled():
                debug_print(f"[DEBUG] Shell generator: last_action_valids = {last_action_valids}, global_valids = {global_valids}")
            
            # Combine all validations
            all_validations = []
            if validation_ast:
                all_validations.extend(validation_ast)
            all_validations.extend(last_action_valids)
            all_validations.extend(global_valids)
            
            # Generate validation code for each expression
            for i, validation in enumerate(all_validations):
                if is_debug_enabled():
                    debug_print(f"[DEBUG] Shell generator: Compiling validation: '{validation}'")
                    debug_print(f"[DEBUG] Shell generator: last_file_var = {self.last_file_var}")
                # Pass extracted_args to compile_atomic
                validation_lines = compile_atomic(validation, f"result_{i}", self.last_file_var, extracted_args=extracted_args)
                if is_debug_enabled():
                    debug_print(f"[DEBUG] Shell generator: Generated validation lines: {validation_lines}")
                
                lines.extend(validation_lines)
                # Always display expected/actual
                lines.extend([
                    'echo "Expected: $expected"',
                    'echo "Actual:   $actual"',
                ])
                # Add result check, fail fast
                lines.extend([
                    f"if [ $result_{i} -eq 0 ]; then",
                    f"    echo '❌ Validation failed: {validation}'",
                    f"    exit 1",
                    "else",
                    f"    echo '✅ Validation passed: {validation}'",
                    "fi",
                    "",
                ])
        except Exception as e:
            if is_debug_enabled():
                debug_print(f"[DEBUG] Shell generator: Exception in validation parsing: {e}")
            lines.extend([
                f"echo \"ERROR: Failed to parse validation: {node.result_expr}\"",
                "test_passed=false",
                "",
            ])
        return lines
    
    def _parse_validation(self, validation_expr: str) -> List[str]:
        """Parse validation expression into individual validations."""
        if not validation_expr:
            return []
        
        # Use word boundaries to avoid splitting on substrings
        
        # Split by 'et' and 'ou' with word boundaries
        parts = re.split(r'\b(?:et|ou)\b', validation_expr, flags=re.IGNORECASE)
        
        validations = []
        for part in parts:
            validation = part.strip()
            if validation:
                # Clean up the validation
                validation = validation.strip('.;')
                if validation:
                    validations.append(validation)
        
        return validations
    
    def set_last_file_var(self, file_var: str) -> None:
        """Set the last file variable for context."""
        self.last_file_var = file_var
    
    def add_action_validation(self, validation: str) -> None:
        """Add a validation for the current action."""
        self.last_action_valids.append(validation)
    
    def add_global_validation(self, validation: str) -> None:
        """Add a global validation."""
        self.global_valids.append(validation)
    
    def clear_action_validations(self) -> None:
        """Clear action-specific validations."""
        self.last_action_valids = []

