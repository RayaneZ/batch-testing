"""
Atomic compiler for individual validation expressions.

This module provides the core compilation logic for converting validation
expressions into shell code.
"""

import re
import importlib
from typing import List, Optional, Tuple, Any, Union
from ..config.debug_config import is_debug_enabled, debug_print
from .matcher_registry import MatcherRegistry


def compile_atomic(expected: str, varname: str = "result", last_file_var: Optional[str] = None, extracted_args: Optional[dict] = None) -> List[str]:
    """
    Compile a single validation expression into shell code.
    
    Args:
        expected: The validation expression to compile
        varname: Variable name to use for the result
        last_file_var: Last file variable from previous action
        extracted_args: Dict of arguments extracted from the action command
        
    Returns:
        List of shell code lines
    """
    # Use global debug configuration
    debug_enabled = is_debug_enabled()
    
    if debug_enabled:
        debug_print(f"[DEBUG] compile_atomic called with: expected='{expected}', varname='{varname}', last_file_var={last_file_var}, extracted_args={extracted_args}")
    
    # Canonicalize the validation expression
    canon = canonize_validation(expected)
    if debug_enabled:
        debug_print(f"[DEBUG] canonize_validation result: {canon}")
    
    if not canon:
        return [f"echo 'ERROR: No matcher found for validation: {expected}'"]
    
    phrase_canonique, handler, scope, pattern_entry = canon
    # Check for negation/opposite
    if 'opposite' in pattern_entry:
        opp = pattern_entry['opposite']
        # If the expected matches the opposite phrase or any of its aliases, use the opposite handler
        opp_phrase = opp.get('phrase', '').lower().strip()
        if expected.lower().strip() == opp_phrase:
            handler = opp.get('handler', handler)
            phrase_canonique = opp_phrase
    if debug_enabled:
        debug_print(f"[DEBUG] Canonical validation: '{phrase_canonique}' (handler: {handler}, scope: {scope}) for '{expected}'")
    
    # Find matching validation pattern
    matcher_registry = MatcherRegistry()
    matched_pattern = matcher_registry.find_matcher(expected, scope=scope)
    if debug_enabled:
        debug_print(f"[DEBUG] find_matcher result: {matched_pattern}")
    
    if not matched_pattern:
        return [f"echo 'ERROR: No matcher found for validation: {expected}'"]
    
    # Extract validation groups from the matched pattern
    groups = extract_validation_groups(expected, matched_pattern)
    if debug_enabled:
        debug_print(f"[DEBUG] extract_validation_groups result: {groups}")
    
    # Try to import and use the validation plugin
    try:
        if debug_enabled:
            debug_print(f"[DEBUG] Trying to import plugin: shtest_compiler.plugins.{handler}")
        
        plugin_module = importlib.import_module(f"shtest_compiler.plugins.{handler}")
        if debug_enabled:
            debug_print(f"[DEBUG] Plugin imported successfully: {plugin_module}")
        
        # Check if plugin has handle method
        if hasattr(plugin_module, 'handle'):
            if debug_enabled:
                debug_print(f"[DEBUG] Plugin has handle method, calling with groups={groups}, scope={scope}")
            
            validation_obj = plugin_module.handle(groups, scope=scope)
            if debug_enabled:
                debug_print(f"[DEBUG] Plugin handle returned: {validation_obj}")
            
            # Check if validation object has to_shell method
            if hasattr(validation_obj, 'to_shell'):
                import inspect
                sig = inspect.signature(validation_obj.to_shell)
                param_names = list(sig.parameters.keys())
                if debug_enabled:
                    debug_print(f"[DEBUG] to_shell signature: {sig}, param_names: {param_names}")
                
                # Prepare arguments for to_shell
                kwargs = {}
                if 'varname' in param_names:
                    kwargs['varname'] = varname
                if 'last_file_var' in param_names:
                    kwargs['last_file_var'] = last_file_var
                # Pass extracted_args if plugin expects them
                if extracted_args:
                    for k, v in extracted_args.items():
                        if k in param_names:
                            kwargs[k] = v
                # Call to_shell with appropriate parameters
                matched = validation_obj.to_shell(**kwargs)
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
        return [f"echo 'ERROR: Could not import plugin {handler}: {e}'"]
    except Exception as e:
        if debug_enabled:
            debug_print(f"[DEBUG] Exception in plugin {handler}: {e}")
        return [f"echo 'ERROR: Exception in plugin {handler}: {e}'"]
    
    # If we get here, we found a matcher but couldn't use the plugin
    if debug_enabled:
        debug_print(f"[DEBUG] Matcher found for: '{expected}' (scope: {scope})")
    
    return [f"echo 'ERROR: No handler found for validation: {expected}'"]


def canonize_validation(validation: str) -> Optional[Tuple[str, str, str, dict]]:
    """
    Canonicalize a validation expression to find the appropriate handler.
    Returns (canonical_phrase, handler_name, scope, pattern_entry) or None if not found
    """
    import yaml
    import os
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
                pattern_entry
            )
        # Check aliases
        for alias in pattern_entry.get("aliases", []):
            if alias.lower() == validation_lower:
                return (
                    pattern_entry["phrase"],
                    pattern_entry["handler"],
                    pattern_entry.get("scope", "global"),
                    pattern_entry
                )
            if alias.startswith("^") and alias.endswith("$"):
                try:
                    if re.match(alias, validation_lower, re.IGNORECASE):
                        return (
                            pattern_entry["phrase"],
                            pattern_entry["handler"],
                            pattern_entry.get("scope", "global"),
                            pattern_entry
                        )
                except re.error:
                    continue
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
