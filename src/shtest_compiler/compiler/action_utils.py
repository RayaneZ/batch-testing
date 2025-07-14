import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from shtest_compiler.config.debug_config import debug_print, is_debug_enabled

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def get_config_path(config_file: str) -> str:
    return os.path.join(os.path.dirname(__file__), "../config", config_file)


def load_yaml_config(config_file: str) -> Dict[str, Any]:
    config_path = get_config_path(config_file)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_handler_name(handler_name: str) -> bool:
    """
    Validate if a handler name is valid by checking handler_requirements.yml.
    """
    try:
        requirements_data = load_yaml_config("handler_requirements.yml")
        return handler_name in requirements_data.get("handlers", {})
    except Exception:
        return False


def get_handler_category(handler_name: str) -> Optional[str]:
    """
    Get the category of a handler from handler_requirements.yml.
    """
    try:
        requirements_data = load_yaml_config("handler_requirements.yml")
        handler_config = requirements_data.get("handlers", {}).get(handler_name, {})
        return handler_config.get("category")
    except Exception:
        return None


def get_all_handlers() -> List[str]:
    """
    Get a list of all available handlers from handler_requirements.yml.
    """
    try:
        requirements_data = load_yaml_config("handler_requirements.yml")
        return list(requirements_data.get("handlers", {}).keys())
    except Exception:
        return []


def get_handlers_by_category(category: str) -> List[str]:
    """
    Get handlers for a specific category from handler_requirements.yml.
    """
    try:
        requirements_data = load_yaml_config("handler_requirements.yml")
        return [
            h
            for h, v in requirements_data.get("handlers", {}).items()
            if v.get("category") == category
        ]
    except Exception:
        return []


def normalize_path(path: str) -> str:
    return os.path.normpath(path.strip())


def is_absolute_path(path: str) -> bool:
    return os.path.isabs(normalize_path(path))


def extract_variables_from_pattern(pattern: str) -> List[str]:
    variables = []
    for match in re.finditer(r"\{([^}]+)\}", pattern):
        variables.append(match.group(1))
    return variables


def build_regex_from_pattern(pattern: str, case_sensitive: bool = False) -> str:
    """
    Convert a pattern with placeholders to a regex pattern.
    Uses variable placeholders from patterns_actions.yml and patterns_validations.yml.
    """
    import re

    # Split the pattern into text and placeholders
    regex_parts = []
    pos = 0
    for match in re.finditer(r"\{(\w+)\}", pattern):
        start, end = match.span()
        # Escape the text before the placeholder
        if start > pos:
            regex_parts.append(re.escape(pattern[pos:start]))
        # Replace placeholder with a capturing group
        regex_parts.append(r"(.+)")
        pos = end
    # Add the remaining text after the last placeholder
    if pos < len(pattern):
        regex_parts.append(re.escape(pattern[pos:]))
    # Join and anchor the regex
    regex_pattern = "^" + "".join(regex_parts) + "$"
    # Add case insensitive flag if needed
    if not case_sensitive:
        regex_pattern = f"(?i){regex_pattern}"
    return regex_pattern


def match_pattern_with_variables(
    pattern: str, text: str, case_sensitive: bool = False
) -> Optional[Dict[str, str]]:
    regex_pattern = build_regex_from_pattern(pattern, case_sensitive)
    match = re.match(regex_pattern, text)

    if not match:
        return None

    # Extract variable names from pattern
    variables = extract_variables_from_pattern(pattern)

    # Map variables to captured groups
    result = {}
    for i, var_name in enumerate(variables):
        if i < len(match.groups()):
            result[var_name] = match.group(i + 1)

    return result


# ============================================================================
# CORE FUNCTIONS (existing, enhanced)
# ============================================================================


def canonize_action(action: str) -> Optional[tuple]:
    """
    Canonicalize an action command to find the appropriate handler.
    Returns (canonical_phrase, handler_name, pattern_entry) or None if not found
    """
    debug_enabled = is_debug_enabled()

    try:
        data = load_yaml_config("patterns_actions.yml")
        action_patterns = data.get("actions", [])
        if debug_enabled:
            debug_print(
                f"[DEBUG] canonize_action: Loaded {len(action_patterns)} action patterns"
            )
    except (FileNotFoundError, yaml.YAMLError) as e:
        if debug_enabled:
            debug_print(f"[DEBUG] canonize_action: Failed to load patterns: {e}")
        return None

    action_lower = action.lower().strip()
    if debug_enabled:
        debug_print(
            f"[DEBUG] canonize_action: Processing action '{action}' (normalized: '{action_lower}')"
        )

    for pattern_entry in action_patterns:
        phrase = pattern_entry["phrase"]
        handler = pattern_entry["handler"]
        if debug_enabled:
            debug_print(
                f"[DEBUG] canonize_action: Checking pattern '{phrase}' with handler '{handler}'"
            )

        # If the phrase contains {var}, treat as pattern
        if "{" in phrase and "}" in phrase:
            # Convert to regex
            regex_pattern = build_regex_from_pattern(phrase)
            if debug_enabled:
                debug_print(
                    f"[DEBUG] canonize_action: Testing regex pattern '{regex_pattern}'"
                )
            match = re.match(regex_pattern, action, re.IGNORECASE)
            if match:
                if debug_enabled:
                    debug_print(
                        f"[DEBUG] canonize_action: Found match with pattern '{phrase}'"
                    )
                return (
                    pattern_entry["phrase"],
                    pattern_entry["handler"],
                    pattern_entry,
                )
        # Check exact phrase match
        if phrase.lower() == action_lower:
            if debug_enabled:
                debug_print(
                    f"[DEBUG] canonize_action: Found exact match with pattern '{phrase}'"
                )
            return (pattern_entry["phrase"], pattern_entry["handler"], pattern_entry)
        # Check aliases
        for alias in pattern_entry.get("aliases", []):
            if not isinstance(alias, str):
                continue
            if debug_enabled:
                debug_print(f"[DEBUG] canonize_action: Checking alias '{alias}'")
            # If alias contains {var}, treat as pattern
            if "{" in alias and "}" in alias:
                regex_pattern = build_regex_from_pattern(alias)
                if debug_enabled:
                    debug_print(
                        f"[DEBUG] canonize_action: Testing alias regex '{regex_pattern}'"
                    )
                match = re.match(regex_pattern, action, re.IGNORECASE)
                if match:
                    if debug_enabled:
                        debug_print(
                            f"[DEBUG] canonize_action: Found match with alias '{alias}'"
                        )
                    return (
                        pattern_entry["phrase"],
                        pattern_entry["handler"],
                        pattern_entry,
                    )
            # Exact match
            if alias.lower() == action_lower:
                if debug_enabled:
                    debug_print(
                        f"[DEBUG] canonize_action: Found exact match with alias '{alias}'"
                    )
                return (
                    pattern_entry["phrase"],
                    pattern_entry["handler"],
                    pattern_entry,
                )
            # Regex alias
            if alias.startswith("^") and alias.endswith("$"):
                try:
                    if debug_enabled:
                        debug_print(
                            f"[DEBUG] canonize_action: Testing regex alias '{alias}'"
                        )
                    if re.match(alias, action_lower, re.IGNORECASE):
                        if debug_enabled:
                            debug_print(
                                f"[DEBUG] canonize_action: Found match with regex alias '{alias}'"
                            )
                        return (
                            pattern_entry["phrase"],
                            pattern_entry["handler"],
                            pattern_entry,
                        )
                except re.error:
                    continue

    if debug_enabled:
        debug_print(f"[DEBUG] canonize_action: No match found for action '{action}'")
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
    regex_pattern = build_regex_from_pattern(pattern)

    # Try to match the action against the pattern
    match = re.match(regex_pattern, action, re.IGNORECASE)
    if match:
        return list(match.groups())
    return []


def canonize_validation(validation: str) -> Optional[tuple]:
    """
    Canonicalize a validation command to find the appropriate handler.
    Returns (canonical_phrase, handler_name, pattern_entry) or None if not found
    """
    try:
        data = load_yaml_config("patterns_validations.yml")
        validation_patterns = data.get("validations", [])
    except (FileNotFoundError, yaml.YAMLError):
        return None

    validation_lower = validation.lower().strip()

    for pattern_entry in validation_patterns:
        # Check exact phrase match
        if pattern_entry["phrase"].lower() == validation_lower:
            return (pattern_entry["phrase"], pattern_entry["handler"], pattern_entry)

        # Check aliases
        for alias in pattern_entry.get("aliases", []):
            # Skip if alias is not a string
            if not isinstance(alias, str):
                continue

            if alias.lower() == validation_lower:
                return (
                    pattern_entry["phrase"],
                    pattern_entry["handler"],
                    pattern_entry,
                )

            # Handle regex patterns
            if alias.startswith("^") and alias.endswith("$"):
                try:
                    if re.match(alias, validation_lower, re.IGNORECASE):
                        return (
                            pattern_entry["phrase"],
                            pattern_entry["handler"],
                            pattern_entry,
                        )
                except re.error:
                    continue

    return None


def extract_validation_groups(validation: str, pattern: str) -> List[str]:
    """
    Extract groups from validation command using the pattern.
    Args:
        validation: The validation command
        pattern: The regex pattern to match against
    Returns:
        List of extracted groups
    """
    # Convert YAML pattern placeholders to regex
    regex_pattern = build_regex_from_pattern(pattern)

    # Try to match the validation against the pattern
    match = re.match(regex_pattern, validation, re.IGNORECASE)
    if match:
        return list(match.groups())
    return []


# ============================================================================
# ADVANCED UTILITY FUNCTIONS
# ============================================================================


def get_handler_patterns(handler_name: str) -> List[Dict[str, Any]]:
    """
    Get all patterns associated with a handler from configuration files.

    Args:
        handler_name: Name of the handler

    Returns:
        List of pattern configurations for the handler
    """
    patterns = []

    # Load action patterns
    try:
        action_data = load_yaml_config("patterns_actions.yml")
        for action in action_data.get("actions", []):
            if action.get("handler") == handler_name:
                patterns.append(
                    {
                        "type": "action",
                        "phrase": action.get("phrase", ""),
                        "aliases": action.get("aliases", []),
                        "handler": handler_name,
                    }
                )
    except (FileNotFoundError, yaml.YAMLError):
        pass

    # Load validation patterns
    try:
        validation_data = load_yaml_config("patterns_validations.yml")
        for validation in validation_data.get("validations", []):
            if validation.get("handler") == handler_name:
                patterns.append(
                    {
                        "type": "validation",
                        "phrase": validation.get("phrase", ""),
                        "aliases": validation.get("aliases", []),
                        "handler": handler_name,
                        "scope": validation.get("scope", "global"),
                    }
                )
    except (FileNotFoundError, yaml.YAMLError):
        pass

    return patterns


def extract_variables_from_command(command: str, handler_name: str) -> Dict[str, str]:
    """
    Extract variables from a command using handler-specific patterns.

    Args:
        command: The command to parse
        handler_name: Name of the handler

    Returns:
        Dictionary mapping variable names to extracted values
    """
    variables = {}
    patterns = get_handler_patterns(handler_name)

    for pattern_config in patterns:
        # Try the main phrase
        phrase = pattern_config.get("phrase", "")
        if phrase:
            extracted = match_pattern_with_variables(
                phrase, command, case_sensitive=False
            )
            if extracted:
                variables.update(extracted)
                break

        # Try aliases
        for alias in pattern_config.get("aliases", []):
            if isinstance(alias, str):
                extracted = match_pattern_with_variables(
                    alias, command, case_sensitive=False
                )
                if extracted:
                    variables.update(extracted)
                    break

        if variables:  # Found a match
            break

    return variables


def get_handler_requirements(handler_name: str) -> Dict[str, Any]:
    """
    Get the requirements for a handler from configuration file.

    Args:
        handler_name: Name of the handler

    Returns:
        Dictionary containing handler requirements
    """
    try:
        requirements_data = load_yaml_config("handler_requirements.yml")
        handler_config = requirements_data.get("handlers", {}).get(handler_name, {})

        if handler_config:
            return {
                "required_variables": handler_config.get("required_variables", []),
                "optional_variables": handler_config.get("optional_variables", []),
                "scope": handler_config.get("scope", "global"),
                "description": handler_config.get("description", ""),
                "category": handler_config.get("category", "unknown"),
                "validation_rules": handler_config.get("validation_rules", {}),
            }
    except (FileNotFoundError, yaml.YAMLError):
        pass

    # Fallback to empty requirements if config file is not available
    return {
        "required_variables": [],
        "optional_variables": [],
        "scope": "global",
        "description": "",
        "category": get_handler_category(handler_name),
        "validation_rules": {},
    }


def extract_context_from_action(action: str, handler_name: str) -> Dict[str, Any]:
    """
    Extract context information from an action command using modular pattern matching.

    Args:
        action: The action command
        handler_name: Name of the handler

    Returns:
        Dictionary containing extracted context information
    """
    context = {
        "action": action,
        "handler": handler_name,
        "category": get_handler_category(handler_name),
        "variables": {},
        "requirements": {},
        "patterns_matched": [],
    }

    # Get handler requirements
    requirements = get_handler_requirements(handler_name)
    context["requirements"] = requirements

    # Extract variables using pattern matching
    extracted_vars = extract_variables_from_command(action, handler_name)
    context["variables"] = extracted_vars

    # Determine scope based on extracted variables and requirements
    scope = requirements.get("scope", "global")
    if scope == "last_action" and not extracted_vars:
        # If no variables extracted and scope is last_action,
        # it means the validation depends on the last action's context
        context["scope"] = "last_action"
    else:
        context["scope"] = scope

    # Track which patterns were matched
    patterns = get_handler_patterns(handler_name)
    for pattern_config in patterns:
        phrase = pattern_config.get("phrase", "")
        if phrase and match_pattern_with_variables(
            phrase, action, case_sensitive=False
        ):
            context["patterns_matched"].append(
                {"type": "phrase", "pattern": phrase, "config": pattern_config}
            )
            break

        for alias in pattern_config.get("aliases", []):
            if isinstance(alias, str) and match_pattern_with_variables(
                alias, action, case_sensitive=False
            ):
                context["patterns_matched"].append(
                    {"type": "alias", "pattern": alias, "config": pattern_config}
                )
                break

        if context["patterns_matched"]:
            break

    return context


def validate_action_context(context: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate the context extracted from an action using configuration-based validation rules.
    Only uses patterns from the YAML config.
    """
    errors = []
    # Check required fields
    required_fields = ["action", "handler"]
    for field in required_fields:
        if field not in context:
            errors.append(f"Missing required field: {field}")
    # Validate handler
    if "handler" in context and not validate_handler_name(context["handler"]):
        errors.append(f"Invalid handler name: {context['handler']}")
    # Validate variables against requirements
    requirements = context.get("requirements", {})
    variables = context.get("variables", {})
    validation_rules = requirements.get("validation_rules", {})
    # Check required variables
    required_vars = requirements.get("required_variables", [])
    for var_name in required_vars:
        if var_name not in variables:
            errors.append(
                f"Handler {context.get('handler', 'unknown')} requires '{var_name}' variable"
            )
    # Validate variable formats using configuration rules (YAML only)
    for var_name, var_value in variables.items():
        if var_name in validation_rules:
            rule = validation_rules[var_name]
            pattern = rule.get("pattern", "")
            # Check if pattern validation is required
            if pattern and not re.match(pattern, var_value):
                errors.append(
                    f"Variable '{var_name}' value '{var_value}' doesn't match pattern '{pattern}'"
                )
    return len(errors) == 0, errors


def get_handler_metadata(handler_name: str) -> Dict[str, Any]:
    """
    Get comprehensive metadata about a handler.

    Args:
        handler_name: Name of the handler

    Returns:
        Dictionary containing handler metadata
    """
    metadata = {
        "name": handler_name,
        "category": get_handler_category(handler_name),
        "patterns": get_handler_patterns(handler_name),
        "requirements": get_handler_requirements(handler_name),
        "description": "",
        "examples": [],
    }

    # Add examples based on patterns
    patterns = metadata["patterns"]
    for pattern_config in patterns:
        phrase = pattern_config.get("phrase", "")
        if phrase:
            # Create example by replacing placeholders with sample values
            example = phrase
            for placeholder in extract_variables_from_pattern(phrase):
                if placeholder == "path":
                    example = example.replace(f"{{{placeholder}}}", "/path/to/file.txt")
                elif placeholder == "file":
                    example = example.replace(f"{{{placeholder}}}", "example.txt")
                elif placeholder == "dir":
                    example = example.replace(f"{{{placeholder}}}", "example_dir")
                elif placeholder == "src":
                    example = example.replace(f"{{{placeholder}}}", "source.txt")
                elif placeholder == "dest":
                    example = example.replace(f"{{{placeholder}}}", "destination.txt")
                elif placeholder == "script":
                    example = example.replace(f"{{{placeholder}}}", "script.sh")
                elif placeholder == "query":
                    example = example.replace(
                        f"{{{placeholder}}}", "SELECT * FROM table"
                    )
                elif placeholder == "text":
                    example = example.replace(f"{{{placeholder}}}", "expected content")
                elif placeholder == "code":
                    example = example.replace(f"{{{placeholder}}}", "0")
                elif placeholder == "mode":
                    example = example.replace(f"{{{placeholder}}}", "644")
                elif placeholder == "date":
                    example = example.replace(f"{{{placeholder}}}", "20231201")
                elif placeholder == "var":
                    example = example.replace(f"{{{placeholder}}}", "VARIABLE_NAME")
                elif placeholder == "value":
                    example = example.replace(f"{{{placeholder}}}", "variable_value")

            metadata["examples"].append(example)

    return metadata


def list_handlers_with_metadata() -> Dict[str, Dict[str, Any]]:
    """
    Get metadata for all available handlers.

    Returns:
        Dictionary mapping handler names to their metadata
    """
    handlers_metadata = {}
    all_handlers = get_all_handlers()

    for handler_name in all_handlers:
        handlers_metadata[handler_name] = get_handler_metadata(handler_name)

    return handlers_metadata
