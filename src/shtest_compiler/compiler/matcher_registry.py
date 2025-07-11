
# matcher_registry.py

matcher_registry = {}

def register_matcher(name):
    """
    Décorateur pour enregistrer une fonction match() sous un nom spécifique.
    """
    def decorator(fn):
        matcher_registry[name] = fn
        return fn
    return decorator

def run_matcher(expected, *args):
    """
    Essaie chaque matcher enregistré jusqu'à ce qu'un résultat non None soit trouvé.
    """
    for name, matcher in matcher_registry.items():
        result = matcher(expected, *args)
        if result is not None:
            return result
    return None


class MatcherRegistry:
    """Registry for managing matchers."""
    
    def __init__(self):
        self.matchers = {}
    
    def register(self, matcher):
        """Register a matcher."""
        if hasattr(matcher, 'name'):
            self.matchers[matcher.name] = matcher
        else:
            # Use class name as fallback
            self.matchers[matcher.__class__.__name__] = matcher
    
    def get(self, name):
        """Get a matcher by name."""
        return self.matchers.get(name)
    
    def list(self):
        """List all registered matchers."""
        return list(self.matchers.keys())
    
    def run_matcher(self, expected, *args):
        """Run all matchers until one returns a non-None result."""
        for name, matcher in self.matchers.items():
            if hasattr(matcher, 'match'):
                result = matcher.match(expected, *args)
                if result is not None:
                    return result
        return None
