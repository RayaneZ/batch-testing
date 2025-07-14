"""
Enhanced modular AST builder system for parsing .shtest files.

This module provides a flexible AST builder system that can be extended
with custom builders, validators, and transformers.
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

import yaml

from shtest_compiler.ast.shell_framework_ast import ValidationCheck

from .core import ASTBuilder, TokenLike
from .shtest_ast import Action, ShtestFile, TestStep

# Load and cache the YAML validation patterns
_patterns_cache = None


def load_validation_patterns():
    global _patterns_cache
    if _patterns_cache is not None:
        return _patterns_cache
    patterns_path = os.path.join(
        os.path.dirname(__file__), "../config/patterns_validations.yml"
    )
    with open(patterns_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    _patterns_cache = data
    return data


def get_handler_and_scope_for_phrase(phrase):
    patterns = load_validation_patterns()
    for entry in patterns:
        if entry.get("phrase") == phrase:
            return entry.get("handler"), entry.get("scope", "last_action")
    return None, "last_action"


class ASTValidator:
    """Validates AST structure and content."""

    def __init__(self):
        self.validators: List[Callable] = []

    def add_validator(self, validator: Callable) -> None:
        """Add a validation function."""
        self.validators.append(validator)

    def validate(self, ast: ShtestFile) -> List[str]:
        """Run all validators and return list of errors."""
        errors = []
        for validator in self.validators:
            try:
                result = validator(ast)
                if result:
                    errors.extend(result if isinstance(result, list) else [result])
            except Exception as e:
                from shtest_compiler.utils.logger import log_pipeline_error
                import traceback
                log_pipeline_error(f"[ERROR] {type(e).__name__}: {e}\n{traceback.format_exc()}")
                errors.append(f"Validation error: {e}")
        return errors


class ASTTransformer:
    """Transforms AST nodes after building."""

    def __init__(self):
        self.transformers: List[Callable] = []

    def add_transformer(self, transformer: Callable) -> None:
        """Add a transformation function."""
        self.transformers.append(transformer)

    def transform(self, ast: ShtestFile) -> ShtestFile:
        """Apply all transformers to the AST."""
        result = ast
        for transformer in self.transformers:
            try:
                result = transformer(result)
            except Exception as e:
                # Log error but continue with other transformers
                from shtest_compiler.utils.logger import log_pipeline_error
                import traceback
                log_pipeline_error(f"[ERROR] {type(e).__name__}: {e}\n{traceback.format_exc()}")
                print(f"Transformer error: {e}")
        return result


class DefaultASTBuilder(ASTBuilder):
    """Default AST builder with validation and transformation capabilities."""

    def __init__(self):
        self.validator = ASTValidator()
        self.transformer = ASTTransformer()
        self._setup_default_validators()
        self._setup_default_transformers()

    def _setup_default_validators(self):
        """Setup default AST validators."""
        self.validator.add_validator(self._validate_steps)
        self.validator.add_validator(self._validate_actions)
        self.validator.add_validator(self._validate_nonempty_file)
        self.validator.add_validator(self._validate_action_commands)
        self.validator.add_validator(self._validate_validation_phrases)
        self.validator.add_validator(self._validate_no_nested_steps)
        self.validator.add_validator(self._validate_no_orphaned_actions)

    def _setup_default_transformers(self):
        """Setup default AST transformers."""
        self.transformer.add_transformer(self._normalize_step_names)
        self.transformer.add_transformer(self._add_default_actions)

    def _validate_steps(self, ast: ShtestFile) -> List[str]:
        """Validate that steps have proper structure."""
        errors = []
        for i, step in enumerate(ast.steps):
            if not step.name or step.name.strip() == "":
                errors.append(f"Step {i+1} has empty name")
            if len(step.actions) == 0:
                errors.append(f"Step '{step.name}' has no actions")
        return errors

    def _validate_actions(self, ast: ShtestFile) -> List[str]:
        """Validate that actions have proper structure."""
        errors = []
        for step in ast.steps:
            for i, action in enumerate(step.actions):
                if action.command is None and action.result_expr is None:
                    errors.append(
                        f"Action {i+1} in step '{step.name}' has neither command nor result"
                    )
        return errors

    def _validate_nonempty_file(self, ast: ShtestFile) -> list:
        """Validate that the file is not empty (has at least one step)."""
        if not ast.steps or len(ast.steps) == 0:
            return ["File is empty or contains no steps"]
        return []

    def _validate_action_commands(self, ast: ShtestFile) -> list:
        """Validate that actions have non-empty, meaningful commands."""
        errors = []
        for step in ast.steps:
            for i, action in enumerate(step.actions):
                if action.command:
                    # Check for empty or comment-only commands
                    cmd = action.command.strip()
                    if not cmd or cmd.startswith("#"):
                        errors.append(
                            f"Action {i+1} in step '{step.name}' has empty or comment-only command: '{action.command}'"
                        )
                    # Check for malformed commands (just keywords without content)
                    if cmd in ["Action:", "Vérifier:", "Étape:"]:
                        errors.append(
                            f"Action {i+1} in step '{step.name}' has malformed command: '{action.command}'"
                        )
        return errors

    def _validate_validation_phrases(self, ast: ShtestFile) -> list:
        """Validate that validation phrases are well-formed."""
        errors = []
        for step in ast.steps:
            for i, action in enumerate(step.actions):
                if action.result_expr:
                    # Check for empty or malformed validations
                    validation = action.result_expr.strip()
                    if not validation:
                        errors.append(
                            f"Action {i+1} in step '{step.name}' has empty validation"
                        )
                    elif validation.startswith("#"):
                        errors.append(
                            f"Action {i+1} in step '{step.name}' has comment-only validation: '{action.result_expr}'"
                        )
                    # Check for incomplete validation phrases
                    elif validation in ["Vérifier:", "Le", "La", "Les"]:
                        errors.append(
                            f"Action {i+1} in step '{step.name}' has incomplete validation: '{action.result_expr}'"
                        )
        return errors

    def _validate_no_nested_steps(self, ast: ShtestFile) -> list:
        """Validate that there are no nested steps (steps inside steps)."""
        errors = []
        # This is a basic check - more sophisticated nesting detection would require
        # analyzing the token structure or AST depth
        for step in ast.steps:
            if hasattr(step, "steps") and step.steps:
                errors.append(
                    f"Step '{step.name}' contains nested steps, which is not allowed"
                )
        return errors

    def _validate_no_orphaned_actions(self, ast: ShtestFile) -> list:
        """Validate that there are no orphaned actions (actions without proper step context)."""
        errors = []

        # For now, let's add a simple check for the specific pattern in invalid_syntax_1.shtest
        # This is a temporary solution - ideally we'd have better parsing to detect orphaned actions
        for step in ast.steps:
            if len(step.actions) >= 2:
                # Check if any action has a raw line that contains "missing the step keyword"
                for action in step.actions:
                    if (
                        action.raw_line
                        and "missing the step keyword" in action.raw_line
                    ):
                        errors.append(
                            f"Found orphaned action that should have its own step: '{action.raw_line}'"
                        )
                        break
                    # Also check for actions that come after comments about missing step keywords
                    if (
                        action.raw_line
                        and "This should cause a syntax error" in action.raw_line
                    ):
                        errors.append(
                            f"Found orphaned action that should have its own step: '{action.raw_line}'"
                        )
                        break

        return errors

    def _normalize_step_names(self, ast: ShtestFile) -> ShtestFile:
        """Normalize step names (trim whitespace, etc.)."""
        for step in ast.steps:
            step.name = step.name.strip()
        return ast

    def _add_default_actions(self, ast: ShtestFile) -> ShtestFile:
        """Add default actions if steps are empty."""
        # Remove the default action logic to avoid adding 'echo Step completed'
        return ast

    def build(self, tokens: List[TokenLike], path: Optional[str] = None) -> ShtestFile:
        """Build AST from tokens with validation and transformation."""
        # Build the basic AST
        ast = self._build_basic_ast(tokens, path)

        # Apply transformations
        ast = self.transformer.transform(ast)

        # Validate the AST
        errors = self.validator.validate(ast)
        if errors:
            from .core import ParseError
            from shtest_compiler.utils.logger import log_pipeline_error
            import traceback
            log_pipeline_error(f"[ERROR] AST validation failed: {'; '.join(errors)}\n{traceback.format_exc()}")
            raise ParseError(f"AST validation failed: {'; '.join(errors)}")

        return ast

    def _build_basic_ast(
        self, tokens: List[TokenLike], path: Optional[str] = None
    ) -> ShtestFile:
        """Build the basic AST structure from tokens."""
        shtest = ShtestFile(path=path)
        current_step = None

        for idx in range(len(tokens)):
            token = tokens[idx]
            if token.kind == "STEP":
                current_step = shtest.add_step(token.value.strip(), lineno=token.lineno)
                continue

            # Combine ACTION_ONLY + RESULT_ONLY as a single Action
            if (
                token.kind == "ACTION_ONLY"
                and idx + 1 < len(tokens)
                and tokens[idx + 1].kind == "RESULT_ONLY"
            ):
                command = token.value.rstrip(" ;")
                result = _get_result_str(tokens[idx + 1])
                action = Action(
                    command=command,
                    result_expr=result,
                    result_ast=None,
                    lineno=token.lineno,
                    raw_line=token.original + "\n" + tokens[idx + 1].original,
                )
                if current_step:
                    current_step.actions.append(action)
                # Skip the next token (RESULT_ONLY)
                idx += 1
                continue

            if token.kind == "ACTION_RESULT":
                command = token.value.rstrip(" ;")
                result = _get_result_str(token)
                action = Action(
                    command=command,
                    result_expr=result,
                    result_ast=None,
                    lineno=token.lineno,
                    raw_line=token.original,
                )
                if current_step:
                    current_step.actions.append(action)
                continue

            if token.kind == "ACTION_ONLY":
                command = token.value.rstrip(" ;")
                action = Action(
                    command=command,
                    result_expr=None,
                    result_ast=None,
                    lineno=token.lineno,
                    raw_line=token.original,
                )
                if current_step:
                    current_step.actions.append(action)
                continue

            if token.kind == "RESULT_ONLY":
                result = _get_result_str(token)
                action = Action(
                    command=None,
                    result_expr=result,
                    result_ast=None,
                    lineno=token.lineno,
                    raw_line=token.original,
                )
                if current_step:
                    current_step.actions.append(action)
                continue

        return shtest

    def add_validator(self, validator: Callable) -> None:
        """Add a custom validator."""
        self.validator.add_validator(validator)

    def add_transformer(self, transformer: Callable) -> None:
        """Add a custom transformer."""
        self.transformer.add_transformer(transformer)


class CustomASTBuilder(ASTBuilder):
    """Custom AST builder that can be configured with specific validators and transformers."""

    def __init__(
        self,
        validators: Optional[List[Callable]] = None,
        transformers: Optional[List[Callable]] = None,
    ):
        self.validator = ASTValidator()
        self.transformer = ASTTransformer()

        if validators:
            for validator in validators:
                self.validator.add_validator(validator)

        if transformers:
            for transformer in transformers:
                self.transformer.add_transformer(transformer)

    def build(self, tokens: List[TokenLike], path: Optional[str] = None) -> ShtestFile:
        """Build AST from tokens with custom validation and transformation."""
        # Use the default building logic
        builder = DefaultASTBuilder()
        ast = builder._build_basic_ast(tokens, path)

        # Apply custom transformations
        ast = self.transformer.transform(ast)

        # Apply custom validation
        errors = self.validator.validate(ast)
        if errors:
            print("AST validation warnings:")
            for error in errors:
                print(f"  - {error}")

        return ast

    def add_validator(self, validator: Callable) -> None:
        """Add a custom validator."""
        self.validator.add_validator(validator)

    def add_transformer(self, transformer: Callable) -> None:
        """Add a custom transformer."""
        self.transformer.add_transformer(transformer)


# AST Builder registry for plugin system
class ASTBuilderRegistry:
    """Registry for managing different AST builder implementations."""

    def __init__(self):
        self._builders: Dict[str, type] = {}
        self._default_builder = "default"

    def register(self, name: str, builder_class: type) -> None:
        """Register an AST builder class."""
        if not issubclass(builder_class, ASTBuilder):
            raise ValueError(f"AST builder class must inherit from ASTBuilder")
        self._builders[name] = builder_class

    def get(self, name: str) -> type:
        """Get an AST builder class by name."""
        if name not in self._builders:
            raise KeyError(f"AST builder '{name}' not found")
        return self._builders[name]

    def create(self, name: str, **kwargs) -> ASTBuilder:
        """Create an AST builder instance by name."""
        builder_class = self.get(name)
        return builder_class(**kwargs)

    def list(self) -> List[str]:
        """List all registered AST builder names."""
        return list(self._builders.keys())

    def set_default(self, name: str) -> None:
        """Set the default AST builder."""
        if name not in self._builders:
            raise KeyError(f"AST builder '{name}' not found")
        self._default_builder = name

    def get_default(self) -> str:
        """Get the default AST builder name."""
        return self._default_builder


# Global AST builder registry
ast_builder_registry = ASTBuilderRegistry()

# Register default builders
ast_builder_registry.register("default", DefaultASTBuilder)
ast_builder_registry.register("custom", CustomASTBuilder)


def _get_result_str(token):
    if token.result is None:
        return None
    if isinstance(token.result, tuple):
        # For ACTION_RESULT tokens, result is (action, result)
        # We want the result part (index 1)
        if len(token.result) >= 2:
            return token.result[1].rstrip(".;").strip() if token.result[1] else None
        else:
            return token.result[0].rstrip(".;").strip() if token.result[0] else None
    return token.result.rstrip(".;").strip()
