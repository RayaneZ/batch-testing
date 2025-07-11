"""
Enhanced modular AST builder system for parsing .shtest files.

This module provides a flexible AST builder system that can be extended
with custom builders, validators, and transformers.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable
from .core import TokenLike, ASTBuilder
from .shtest_ast import ShtestFile, Action, TestStep


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
                    errors.append(f"Action {i+1} in step '{step.name}' has neither command nor result")
        return errors
    
    def _normalize_step_names(self, ast: ShtestFile) -> ShtestFile:
        """Normalize step names (trim whitespace, etc.)."""
        for step in ast.steps:
            step.name = step.name.strip()
        return ast
    
    def _add_default_actions(self, ast: ShtestFile) -> ShtestFile:
        """Add default actions if steps are empty."""
        for step in ast.steps:
            if not step.actions:
                # Add a default "echo" action
                default_action = Action(
                    command="echo 'Step completed'",
                    result_expr=None,
                    result_ast=None,
                    lineno=step.lineno,
                    raw_line="Action: echo 'Step completed'"
                )
                step.actions.append(default_action)
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
            # For now, just print warnings. In the future, this could raise exceptions
            print("AST validation warnings:")
            for error in errors:
                print(f"  - {error}")
        
        return ast
    
    def _build_basic_ast(self, tokens: List[TokenLike], path: Optional[str] = None) -> ShtestFile:
        """Build the basic AST structure from tokens."""
        shtest = ShtestFile(path=path)
        current_step = None

        for token in tokens:
            if token.kind == "STEP":
                current_step = shtest.add_step(token.value.strip(), lineno=token.lineno)
                continue

            if token.kind == "ACTION_RESULT":
                command = token.value.rstrip(" ;")
                result = token.result.rstrip(".;").strip() if token.result else None
                action = Action(
                    command=command, 
                    result_expr=result, 
                    result_ast=None, 
                    lineno=token.lineno, 
                    raw_line=token.original
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
                    raw_line=token.original
                )
                if current_step:
                    current_step.actions.append(action)
                continue

            if token.kind == "RESULT_ONLY":
                result = token.result.rstrip(".;").strip() if token.result else None
                action = Action(
                    command=None, 
                    result_expr=result, 
                    result_ast=None, 
                    lineno=token.lineno, 
                    raw_line=token.original
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
    
    def __init__(self, validators: Optional[List[Callable]] = None, 
                 transformers: Optional[List[Callable]] = None):
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