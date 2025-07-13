"""
Visitor implementations for the compiler module.
"""

from .shell_visitor import ShellVisitor

# Backward compatibility alias
CompilerVisitor = ShellVisitor

__all__ = ['ShellVisitor', 'CompilerVisitor'] 