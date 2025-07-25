"""
Atomic compiler for individual validation expressions.

This module provides the core compilation logic for converting validation
expressions into shell code.
"""

import os
import re
from typing import Any, List, Optional, Tuple, Union

import yaml

from shtest_compiler.compiler.action_utils import (
    canonize_validation,
    extract_context_from_action,
    validate_action_context,
)
from shtest_compiler.core.errors import ValidationParseError
from shtest_compiler.utils.shell_utils import shell_escape
from shtest_compiler.command_loader import build_registry

from ..utils.logger import debug_log, is_debug_enabled


def compile_atomic(
    expected: str,
    varname: str = "result",
    last_file_var: Optional[str] = None,
    extracted_args: Optional[dict] = None,
    action_context: Optional[dict] = None,
) -> List[str]:
    debug_enabled = is_debug_enabled()
    if debug_enabled:
        debug_log(
            f"compile_atomic called with: expected='{expected}', varname='{varname}', last_file_var={last_file_var}, extracted_args={extracted_args}, action_context={action_context}"
        )
    # Add debug output for alias matching
    if debug_enabled:
        debug_log(
            f"compile_atomic: Trying to canonize validation: '{expected}'"
        )
    # Use modular context extraction instead of manual canonization and argument extraction
    canon = canonize_validation(expected)
    if debug_enabled:
        debug_log(
            f"compile_atomic: canonize_validation('{expected}') result: {canon}"
        )
    if not canon:
        raise ValidationParseError(f"No matcher found for validation: '{expected}'")

    handler = canon["handler"]
    phrase = canon["phrase"]
    params = canon.get("params", {}).copy()
    # Patch: inject code=0 for 'Le script s'execute avec succès' and its aliases
    if handler == "return_code" and (
        phrase.lower().strip() == "le script s'execute avec succès"
        or phrase.lower().strip() == "le script a réussi"
        or phrase.lower().strip() == "le script a reussi"
        or phrase.lower().strip() == "le script retourne un code 0"
        or phrase.lower().strip() == "le script s'est exécuté sans erreur"
        or phrase.lower().strip() == "le script s'est execute sans erreur"
        or phrase.lower().strip() == "le script s'est exécuté avec succès"
        or phrase.lower().strip() == "le script s'est execute avec succes"
    ):
        params["code"] = "0"

    # Extract context using the modular system
    context = extract_context_from_action(expected, handler)
    if debug_enabled:
        debug_log(f"extract_context_from_action result: {context}")

    # Merge injected params into context variables
    context_vars = context.get("variables", {}).copy()
    context_vars.update(params)
    context["variables"] = context_vars
    # Validate the context
    is_valid, errors = validate_action_context(context)
    if not is_valid:
        error_msg = f"Validation context errors for '{expected}': {', '.join(errors)}"
        if debug_enabled:
            debug_log(f"{error_msg}")
        raise ValidationParseError(error_msg)

    # Add extra context for backward compatibility
    params.update(context.get("variables", {}))

    # Add any additional extracted args
    if extracted_args:
        params.update(extracted_args)

    if debug_enabled:
        debug_log(f"Final params for handler: {params}")

    handler_registry, _, _ = build_registry()
    handler_func = handler_registry.get(handler)
    if handler_func:
        try:
            result = handler_func(params)
            if debug_enabled:
                debug_log(f"Handler registry returned: {result}")
            if hasattr(result, "expected") and hasattr(result, "actual_cmd"):
                return [result]
            elif isinstance(result, list):
                return result
            elif isinstance(result, str):
                return [result]
            else:
                return [f"echo 'ERROR: Invalid return type from handler {handler}'"]
        except Exception as e:
            import traceback
            from shtest_compiler.utils.logger import log_pipeline_error
            stack = traceback.format_exc()
            log_pipeline_error(f"Exception in handler {handler}: {e}\n{stack}")
            if debug_enabled:
                debug_log(f"Exception in handler {handler}: {e}")
            return [f"echo 'ERROR: Exception in handler {handler}: {e}'"]
    else:
        return [f"echo 'ERROR: Handler {handler} not found in registry'"]


def canonize_validation(validation: str):
    patterns_path = os.path.join(
        os.path.dirname(__file__), "../config/patterns_validations.yml"
    )
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
                    "phrase": phrase,
                    "handler": pattern_entry["handler"],
                    "scope": pattern_entry.get("scope", "global"),
                    "pattern_entry": pattern_entry,
                    "params": params,
                }
        # Exact match
        if phrase.lower() == validation_lower:
            return {
                "phrase": phrase,
                "handler": pattern_entry["handler"],
                "scope": pattern_entry.get("scope", "global"),
                "pattern_entry": pattern_entry,
                "params": {},
            }
        # Aliases
        for alias in pattern_entry.get("aliases", []):
            if alias.lower() == validation_lower:
                return {
                    "phrase": alias,
                    "handler": pattern_entry["handler"],
                    "scope": pattern_entry.get("scope", "global"),
                    "pattern_entry": pattern_entry,
                    "params": {},
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
                        "phrase": alias,
                        "handler": pattern_entry["handler"],
                        "scope": pattern_entry.get("scope", "global"),
                        "pattern_entry": pattern_entry,
                        "params": params,
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
    return_match = re.match(r"retour\s+(\d+)", validation, re.IGNORECASE)
    if return_match:
        return [return_match.group(1)]

    return []


def debug_msg(msg: str) -> None:
    """Print debug message if debug mode is enabled."""
    debug_log(f"{msg}")


def compile_validation_with_debug(
    validation: str, varname: str = "result", last_file_var: Optional[str] = None
) -> List[str]:
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
        debug_log(f"compile_atomic returning lines: {lines}")
    return lines
