"""
Global debug configuration for the shtest compiler.

This module provides a centralized way to control debug output throughout
the entire shtest compiler system.
"""

import os
from typing import Optional

class DebugConfig:
    """Global debug configuration singleton."""
    
    _instance: Optional['DebugConfig'] = None
    _debug_enabled: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def set_debug(cls, enabled: bool) -> None:
        """Set the global debug flag."""
        cls._debug_enabled = enabled
    
    @classmethod
    def is_debug_enabled(cls) -> bool:
        """Check if debug mode is enabled."""
        return cls._debug_enabled
    
    @classmethod
    def debug_print(cls, *args, **kwargs) -> None:
        """Print debug message only if debug mode is enabled."""
        if cls._debug_enabled:
            print(*args, **kwargs)
    
    @classmethod
    def reset(cls) -> None:
        """Reset debug configuration to defaults."""
        cls._debug_enabled = False


# Global instance
debug_config = DebugConfig()

# Convenience functions
def set_debug(enabled: bool) -> None:
    """Set global debug mode."""
    debug_config.set_debug(enabled)

def is_debug_enabled() -> bool:
    """Check if debug mode is enabled."""
    return debug_config.is_debug_enabled()

def debug_print(*args, **kwargs) -> None:
    """Print debug message only if debug mode is enabled."""
    debug_config.debug_print(*args, **kwargs)

def reset_debug() -> None:
    """Reset debug configuration."""
    debug_config.reset() 