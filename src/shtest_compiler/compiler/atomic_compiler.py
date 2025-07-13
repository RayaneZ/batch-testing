"""
Atomic compiler for individual validation expressions.

This module provides the core compilation logic for converting validation
expressions into shell code.
"""

import re
import importlib
import os
from typing import List, Optional, Tuple, Any, Union
from ..config.debug_config import is_debug_enabled, debug_print
from shtest_compiler.core.errors import ValidationParseError
import yaml


def compile_atomic(expected: str, varname: str = "result", last_file_var: Optional[str] = None, extracted_args: Optional[dict] = None, action_context: Optional[dict] = None) -> List[str]:
    debug_enabled = is_debug_enabled()
    if debug_enabled:
        debug_print(f"[DEBUG] compile_atomic called with: expected='{expected}', varname='{varname}', last_file_var={last_file_var}, extracted_args={extracted_args}, action_context={action_context}")
    canon = canonize_validation(expected)
    if debug_enabled:
        debug_print(f"[DEBUG] canonize_validation result: {canon}")
    if not canon:
        raise ValidationParseError(f"No matcher found for validation: '{expected}'")
    handler = canon['handler']
    scope = canon['scope']
    params = canon['params']
    
    # Fill in missing parameters from action_context if available
    if action_context and action_context.get('command'):
        from shtest_compiler.compiler.argument_extractor import extract_action_args
        from shtest_compiler.compiler.shell_generator import extract_action_groups, canonize_action
        
        command = action_context['command']
        if debug_enabled:
            debug_print(f"[DEBUG] Trying to extract parameters from action command: '{command}'")
        
        # Try to extract missing parameters from the action command
        for pname, pval in params.items():
            if pval is None:
                if debug_enabled:
                    debug_print(f"[DEBUG] Parameter '{pname}' is None, trying to extract from action")
                # Method 1: Try using extract_action_args
                extracted_args_from_action = extract_action_args(command)
                if debug_enabled:
                    debug_print(f"[DEBUG] extract_action_args result: {extracted_args_from_action}")
                if extracted_args_from_action and pname in extracted_args_from_action:
                    params[pname] = extracted_args_from_action[pname]
                    if debug_enabled:
                        debug_print(f"[DEBUG] Found '{pname}' in extracted_args: {extracted_args_from_action[pname]}")
                    continue
                elif debug_enabled:
                    debug_print(f"[DEBUG] extract_action_args returned None or missing '{pname}'")
                
                # Method 2: Try using canonize_action + extract_action_groups
                canon_action = canonize_action(command)
                if debug_enabled:
                    debug_print(f"[DEBUG] canonize_action result: {canon_action}")
                if canon_action:
                    phrase_canonique, handler_name, pattern_entry = canon_action
                    # Find matching pattern
                    matched_pattern = None
                    for alias in [pattern_entry["phrase"]] + pattern_entry.get("aliases", []):
                        if not isinstance(alias, str):
                            continue
                        if alias.lower() == command.lower().strip():
                            matched_pattern = alias
                            break
                        if alias.startswith("^") and alias.endswith("$"):
                            try:
                                if re.match(alias, command.lower().strip(), re.IGNORECASE):
                                    matched_pattern = alias
                                    break
                            except re.error:
                                continue
                    
                    if debug_enabled:
                        debug_print(f"[DEBUG] Matched pattern: {matched_pattern}")
                    if matched_pattern:
                        groups = extract_action_groups(command, matched_pattern)
                        if debug_enabled:
                            debug_print(f"[DEBUG] extract_action_groups result: {groups}")
                        # Extract parameter names from the pattern
                        param_names = re.findall(r'\{(\w+)\}', matched_pattern)
                        if debug_enabled:
                            debug_print(f"[DEBUG] Parameter names from pattern: {param_names}")
                        # Map parameter names to groups
                        for i, param_name in enumerate(param_names):
                            if param_name == pname and i < len(groups):
                                params[pname] = groups[i]
                                if debug_enabled:
                                    debug_print(f"[DEBUG] Mapped '{param_name}' to '{groups[i]}'")
                                break
                        # Also try to map common parameter name variations
                        if pname == 'file' and 'path' in param_names:
                            path_idx = param_names.index('path')
                            if path_idx < len(groups):
                                params[pname] = groups[path_idx]
                                if debug_enabled:
                                    debug_print(f"[DEBUG] Mapped 'file' to 'path' value: {groups[path_idx]}")
                        elif pname == 'date' and 'timestamp' in param_names:
                            timestamp_idx = param_names.index('timestamp')
                            if timestamp_idx < len(groups):
                                params[pname] = groups[timestamp_idx]
                                if debug_enabled:
                                    debug_print(f"[DEBUG] Mapped 'date' to 'timestamp' value: {groups[timestamp_idx]}")
    
    # Add extra context
    params['scope'] = scope
    params['canonical_phrase'] = canon['phrase']
    params['varname'] = varname
    params['last_file_var'] = last_file_var
    if extracted_args:
        params.update(extracted_args)
    # Try to import and use the core handler first
    try:
        if debug_enabled:
            debug_print(f"[DEBUG] Trying to import core handler: shtest_compiler.core.handlers.{handler}")
        core_module = importlib.import_module(f"shtest_compiler.core.handlers.{handler}")
        if hasattr(core_module, 'handle'):
            result = core_module.handle(params)
            if debug_enabled:
                debug_print(f"[DEBUG] Core handler returned: {result}")
            if hasattr(result, 'expected') and hasattr(result, 'actual_cmd'):
                # It's a ValidationCheck, let the emitter handle it
                return [result]
            elif isinstance(result, list):
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
        return [f"echo 'ERROR: Could not import handler {handler}: {e}'"]
    except Exception as e:
        if debug_enabled:
            debug_print(f"[DEBUG] Exception in core handler {handler}: {e}")
        return [f"echo 'ERROR: Exception in core handler {handler}: {e}'"]
    return [f"echo 'ERROR: No handler found for validation: {expected}'"]


def canonize_validation(validation: str):
    patterns_path = os.path.join(os.path.dirname(__file__), "../config/patterns_validations.yml")
    if not os.path.exists(patterns_path):
        return None
    with open(patterns_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
        validation_patterns = data.get("validations", [])
    validation_lower = validation.lower().strip()
    for pattern_entry in validation_patterns:
        phrase = pattern_entry["phrase"]
        # Extract parameter names from phrase
        param_names = re.findall(r"\{([^}]+)\}", phrase)
        # Placeholder regex for phrase
        if param_names:
            placeholder_regex = "^" + re.sub(r"\{[^}]+\}", r"(.+)", phrase) + "$"
            match = re.match(placeholder_regex, validation_lower)
            if match:
                groups = list(match.groups())
                params = dict(zip(param_names, groups))
                return {
                    'phrase': phrase,
                    'handler': pattern_entry["handler"],
                    'scope': pattern_entry.get("scope", "global"),
                    'pattern_entry': pattern_entry,
                    'params': params
                }
        # Exact match
        if phrase.lower() == validation_lower:
            return {
                'phrase': phrase,
                'handler': pattern_entry["handler"],
                'scope': pattern_entry.get("scope", "global"),
                'pattern_entry': pattern_entry,
                'params': {}
            }
        # Aliases
        for alias in pattern_entry.get("aliases", []):
            if alias.lower() == validation_lower:
                return {
                    'phrase': alias,
                    'handler': pattern_entry["handler"],
                    'scope': pattern_entry.get("scope", "global"),
                    'pattern_entry': pattern_entry,
                    'params': {}
                }
            # Regex alias
            if alias.startswith("^") and alias.endswith("$"):
                regex = alias
                match = re.match(regex, validation_lower)
                if match:
                    groups = list(match.groups()) if match else []
                    # Try to extract param names from alias if possible
                    params = dict(zip(param_names, groups)) if param_names else {}
                    return {
                        'phrase': alias,
                        'handler': pattern_entry["handler"],
                        'scope': pattern_entry.get("scope", "global"),
                        'pattern_entry': pattern_entry,
                        'params': params
                    }
    return None


def extract_validation_groups(validation: str, pattern: str) -> List[str]:
    """
    Extract groups from validation expression using the pattern.
    
    Args:
        validation: The validation expression
        pattern: The regex pattern to match against
        
    Returns:
        List of extracted groups
    """
    # Convert YAML pattern placeholders to regex
    regex_pattern = pattern
    regex_pattern = regex_pattern.replace("{code}", r"([0-9]+)")
    regex_pattern = regex_pattern.replace("{text}", r"(.+)")
    regex_pattern = regex_pattern.replace("{file}", r"(.+)")
    
    # Try to match the validation against the pattern
    match = re.match(regex_pattern, validation, re.IGNORECASE)
    if match:
        return list(match.groups())
    
    # If no match, try to extract text from common patterns
    # For stdout contains patterns
    stdout_match = re.match(r'stdout\s+contient\s+"([^"]+)"', validation, re.IGNORECASE)
    if stdout_match:
        return [stdout_match.group(1)]
    
    # For stderr contains patterns
    stderr_match = re.match(r'stderr\s+contient\s+"([^"]+)"', validation, re.IGNORECASE)
    if stderr_match:
        return [stderr_match.group(1)]
    
    # For return code patterns
    return_match = re.match(r'retour\s+(\d+)', validation, re.IGNORECASE)
    if return_match:
        return [return_match.group(1)]
    
    return []


def debug_msg(msg: str) -> None:
    """Print debug message if debug mode is enabled."""
    debug_print(f"[DEBUG] {msg}")


def compile_validation_with_debug(validation: str, varname: str = "result", last_file_var: Optional[str] = None) -> List[str]:
    """
    Compile validation with debug output.
    
    Args:
        validation: The validation expression to compile
        varname: Variable name to use for the result
        last_file_var: Last file variable from previous action
        
    Returns:
        List of shell code lines
    """
    lines = compile_atomic(validation, varname, last_file_var)
    if is_debug_enabled():
        debug_print(f"[DEBUG] compile_atomic returning lines: {lines}")
    return lines
