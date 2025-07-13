"""
Compilation context for sharing state across visitors.
"""

from typing import Dict, Any, List, Optional


class CompileContext:
    """Context for sharing compilation state across visitors."""
    
    def __init__(self, counter: Optional[List[int]] = None, 
                 last_file_var: Optional[List[str]] = None, 
                 verbose: bool = False):
        self.counter = counter or [0]
        self.last_file_var = last_file_var or [None]
        self.verbose = verbose
        self.variables: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
    
    def reset(self):
        """Reset the context for a new compilation."""
        self.counter = [0]
        self.last_file_var = [None]
        self.variables.clear()
        self.metadata.clear()
    
    def get_counter(self) -> int:
        """Get the current counter value."""
        return self.counter[0]
    
    def increment_counter(self) -> int:
        """Increment the counter and return the new value."""
        self.counter[0] += 1
        return self.counter[0]
    
    def set_last_file_var(self, value: str):
        """Set the last file variable."""
        self.last_file_var[0] = value
    
    def get_last_file_var(self) -> Optional[str]:
        """Get the last file variable."""
        return self.last_file_var[0]
    
    def set_variable(self, name: str, value: Any):
        """Set a variable in the context."""
        self.variables[name] = value
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """Get a variable from the context."""
        return self.variables.get(name, default)
    
    def set_metadata(self, key: str, value: Any):
        """Set metadata in the context."""
        self.metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata from the context."""
        return self.metadata.get(key, default) 

    def get_condition_var(self) -> str:
        """Generate and return a unique condition variable name."""
        var = f"cond{self.counter[0]}"
        self.counter[0] += 1
        return var 