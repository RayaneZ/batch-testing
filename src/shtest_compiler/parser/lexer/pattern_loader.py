"""
Pattern loader for configurable lexer patterns.

This module handles loading and compiling regex patterns from YAML configuration files.
"""

import os
import re
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class PatternLoader:
    """Loads and compiles regex patterns from configuration files."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the pattern loader.

        Args:
            config_path: Path to the YAML configuration file. If None, uses default.
        """
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "regex_config.yml"
            )

        self.config_path = Path(config_path)
        self._patterns: Dict[str, re.Pattern] = {}
        self._raw_config: Dict[str, Any] = {}
        self._compiled = False

    def load(self) -> Dict[str, re.Pattern]:
        """Load and compile patterns from the configuration file.

        Returns:
            Dictionary mapping pattern names to compiled regex patterns.

        Raises:
            FileNotFoundError: If the configuration file doesn't exist.
            yaml.YAMLError: If the YAML file is malformed.
            re.error: If any regex pattern is invalid.
        """
        if self._compiled:
            return self._patterns.copy()

        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        # Load raw configuration
        with open(self.config_path, encoding="utf-8") as f:
            self._raw_config = yaml.safe_load(f)

        # Compile patterns
        self._compile_patterns()
        self._compiled = True

        return self._patterns.copy()

    def _compile_patterns(self):
        """Compile regex patterns from the raw configuration."""
        self._patterns.clear()

        # Compile basic patterns
        basic_patterns = [
            "step",
            "action_result",
            "action_only",
            "result_only",
            "comment",
        ]

        for pattern_name in basic_patterns:
            if pattern_name in self._raw_config:
                pattern_str = self._raw_config[pattern_name]
                try:
                    self._patterns[pattern_name] = re.compile(
                        pattern_str, re.IGNORECASE
                    )
                except re.error as e:
                    raise re.error(f"Invalid regex pattern '{pattern_name}': {e}")

        # Compile additional patterns if present
        for key, value in self._raw_config.items():
            if key not in basic_patterns and key not in [
                "line_formats",
                "validation_key",
            ]:
                if isinstance(value, str):
                    try:
                        self._patterns[key] = re.compile(value, re.IGNORECASE)
                    except re.error as e:
                        raise re.error(f"Invalid regex pattern '{key}': {e}")

    def get_pattern(self, name: str) -> Optional[re.Pattern]:
        """Get a specific compiled pattern by name.

        Args:
            name: Name of the pattern to retrieve.

        Returns:
            Compiled regex pattern or None if not found.
        """
        if not self._compiled:
            self.load()

        return self._patterns.get(name)

    def get_raw_config(self) -> Dict[str, Any]:
        """Get the raw configuration dictionary.

        Returns:
            Raw configuration as loaded from YAML.
        """
        if not self._compiled:
            self.load()

        return self._raw_config.copy()

    def reload(self) -> Dict[str, re.Pattern]:
        """Force reload of patterns from the configuration file.

        Returns:
            Dictionary mapping pattern names to compiled regex patterns.
        """
        self._compiled = False
        return self.load()

    def add_pattern(self, name: str, pattern: str) -> re.Pattern:
        """Add a new pattern at runtime.

        Args:
            name: Name for the new pattern.
            pattern: Regex pattern string.

        Returns:
            Compiled regex pattern.

        Raises:
            re.error: If the regex pattern is invalid.
        """
        try:
            compiled = re.compile(pattern, re.IGNORECASE)
            self._patterns[name] = compiled
            self._raw_config[name] = pattern  # Ensure pattern is in raw config too
            self._compiled = True  # Mark as compiled so get_pattern doesn't reload
            return compiled
        except re.error as e:
            raise re.error(f"Invalid regex pattern '{name}': {e}")

    def list_patterns(self) -> list[str]:
        """List all available pattern names.

        Returns:
            List of pattern names.
        """
        if not self._compiled:
            self.load()

        return list(self._patterns.keys())
