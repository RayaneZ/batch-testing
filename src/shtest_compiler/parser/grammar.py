"""
Enhanced modular grammar system for parsing .shtest files.

This module provides a flexible grammar system that can be extended
with custom rules, transformations, and validation.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

from .core import Grammar, TokenLike
from .lexer.core import Token, TokenType
from shtest_compiler.utils.logger import debug_log, is_debug_enabled


class GrammarRule:
    """A grammar rule that can be applied to tokens."""

    def __init__(self, name: str, pattern: str, handler: Callable, priority: int = 0):
        self.name = name
        self.pattern = pattern
        self.handler = handler
        self.priority = priority

    def __repr__(self):
        return f"GrammarRule('{self.name}', priority={self.priority})"


class GrammarTransformer:
    """Transforms tokens based on grammar rules."""

    def __init__(self):
        self.rules: List[GrammarRule] = []

    def add_rule(self, rule: GrammarRule) -> None:
        """Add a grammar rule."""
        self.rules.append(rule)
        # Sort by priority (higher priority first)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def remove_rule(self, name: str) -> None:
        """Remove a grammar rule by name."""
        self.rules = [r for r in self.rules if r.name != name]

    def transform(self, tokens: List[TokenLike]) -> List[TokenLike]:
        """Apply all grammar rules to transform tokens."""
        result = tokens.copy()

        for rule in self.rules:
            result = rule.handler(result)

        return result


class DefaultGrammar(Grammar):
    """Default grammar implementation that passes tokens through unchanged."""

    def __init__(self):
        self.transformer = GrammarTransformer()
        self._setup_default_rules()

    def _setup_default_rules(self):
        """Setup default grammar rules."""
        # Add merge rule for ACTION_ONLY + RESULT_ONLY
        self.transformer.add_rule(
            GrammarRule(
                "merge_action_result",
                "ACTION_ONLY + RESULT_ONLY",
                self._merge_action_result,
                priority=200,
            )
        )
        # Add basic validation rule
        self.transformer.add_rule(
            GrammarRule(
                "validate_structure", ".*", self._validate_basic_structure, priority=100
            )
        )

    def _validate_basic_structure(self, tokens: List[TokenLike]) -> List[TokenLike]:
        """Validate basic token structure."""
        # Check that we have at least one step
        step_tokens = [t for t in tokens if t.kind == "STEP"]
        if not step_tokens:
            # Add a default step if none exists
            default_step = Token(
                type=TokenType.STEP,
                value="Default Step",
                lineno=1,
                original="Step: Default Step",
            )
            tokens.insert(0, default_step)

        return tokens

    def _merge_action_result(self, tokens: List[TokenLike]) -> List[TokenLike]:
        """Merge ACTION_ONLY followed by RESULT_ONLY into ACTION_RESULT tokens."""
        if not tokens:
            return tokens

        debug_enabled = is_debug_enabled()

        if debug_enabled:
            debug_log(
                f"Grammar: _merge_action_result called with {len(tokens)} tokens"
            )
            for i, t in enumerate(tokens):
                debug_log(
                    f"Grammar: Token {i}: kind={t.kind}, value='{t.value}'"
                )

        merged = []
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if (
                t.kind == "ACTION_ONLY"
                and i + 1 < len(tokens)
                and tokens[i + 1].kind == "RESULT_ONLY"
            ):
                # Merge into ACTION_RESULT
                action_token = t
                result_token = tokens[i + 1]
                if debug_enabled:
                    debug_log(
                        f"Grammar: Merging ACTION_ONLY '{action_token.value}' with RESULT_ONLY '{result_token.value}'"
                    )

                merged_token = type(t)(
                    TokenType.ACTION_RESULT,
                    action_token.value,
                    action_token.lineno,
                    action_token.column,
                    result_token.value,
                    action_token.original + " ; " + result_token.original,
                )
                merged.append(merged_token)
                i += 2
            else:
                merged.append(t)
                i += 1

        if debug_enabled:
            debug_log(
                f"Grammar: _merge_action_result returning {len(merged)} tokens"
            )

        return merged

    def match(self, tokens: List[TokenLike]) -> List[TokenLike]:
        """Apply grammar rules to tokens."""
        return self.transformer.transform(tokens)

    def add_rule(self, rule: GrammarRule) -> None:
        """Add a custom grammar rule."""
        self.transformer.add_rule(rule)

    def remove_rule(self, name: str) -> None:
        """Remove a grammar rule."""
        self.transformer.remove_rule(name)

    def get_rules(self) -> List[GrammarRule]:
        """Get all grammar rules."""
        return self.transformer.rules.copy()


class CustomGrammar(Grammar):
    """Custom grammar that can be configured with specific rules."""

    def __init__(self, rules: Optional[List[GrammarRule]] = None):
        self.transformer = GrammarTransformer()
        if rules:
            for rule in rules:
                self.transformer.add_rule(rule)

    def match(self, tokens: List[TokenLike]) -> List[TokenLike]:
        """Apply grammar rules to tokens."""
        return self.transformer.transform(tokens)

    def add_rule(self, rule: GrammarRule) -> None:
        """Add a grammar rule."""
        self.transformer.add_rule(rule)

    def remove_rule(self, name: str) -> None:
        """Remove a grammar rule."""
        self.transformer.remove_rule(name)

    def get_rules(self) -> List[GrammarRule]:
        """Get all grammar rules."""
        return self.transformer.rules.copy()


# Grammar registry for plugin system
class GrammarRegistry:
    """Registry for managing different grammar implementations."""

    def __init__(self):
        self._grammars: Dict[str, type] = {}
        self._default_grammar = "default"

    def register(self, name: str, grammar_class: type) -> None:
        """Register a grammar class."""
        if not issubclass(grammar_class, Grammar):
            raise ValueError(f"Grammar class must inherit from Grammar")
        self._grammars[name] = grammar_class

    def get(self, name: str) -> type:
        """Get a grammar class by name."""
        if name not in self._grammars:
            raise KeyError(f"Grammar '{name}' not found")
        return self._grammars[name]

    def create(self, name: str, **kwargs) -> Grammar:
        """Create a grammar instance by name."""
        grammar_class = self.get(name)
        return grammar_class(**kwargs)

    def list(self) -> List[str]:
        """List all registered grammar names."""
        return list(self._grammars.keys())

    def set_default(self, name: str) -> None:
        """Set the default grammar."""
        if name not in self._grammars:
            raise KeyError(f"Grammar '{name}' not found")
        self._default_grammar = name

    def get_default(self) -> str:
        """Get the default grammar name."""
        return self._default_grammar


# Global grammar registry
grammar_registry = GrammarRegistry()

# Register default grammars
grammar_registry.register("default", DefaultGrammar)
grammar_registry.register("custom", CustomGrammar)
