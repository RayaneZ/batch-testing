
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

def run_matcher(expected, *args, scope="global"):
    """
    Essaie chaque matcher enregistré jusqu'à ce qu'un résultat non None soit trouvé.
    Transmet le scope aux matchers qui l'acceptent.
    """
    for name, matcher in matcher_registry.items():
        # Vérifier si le matcher accepte le scope
        import inspect
        sig = inspect.signature(matcher)
        if 'scope' in sig.parameters:
            # Créer un dictionnaire d'arguments avec le scope
            kwargs = {'scope': scope}
            # Passer les arguments positionnels et le scope comme argument nommé
            result = matcher(expected, *args, **kwargs)
        else:
            # Matcher qui n'accepte pas le scope
            result = matcher(expected, *args)
        if result is not None:
            return result
    return None


class MatcherRegistry:
    """Registry for managing matchers."""
    
    def __init__(self):
        self.matchers = {}
        self._load_validation_patterns()
    
    def _load_validation_patterns(self):
        """Load validation patterns from YAML configuration."""
        import yaml
        import os
        
        patterns_path = os.path.join(os.path.dirname(__file__), "../config/patterns_validations.yml")
        if os.path.exists(patterns_path):
            with open(patterns_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
                self.validation_patterns = data.get("validations", [])
        else:
            self.validation_patterns = []
    
    def find_matcher(self, validation: str, scope: str = "global") -> str:
        """
        Find a matching validation pattern for the given validation string.
        
        Args:
            validation: The validation expression to match
            scope: The scope to match against
            
        Returns:
            The regex pattern that matches the validation, or None if not found
        """
        validation_lower = validation.lower().strip()
        
        for pattern_entry in self.validation_patterns:
            # Check if scope matches
            pattern_scope = pattern_entry.get("scope", "global")
            if scope != pattern_scope:
                continue
            
            # Check exact phrase match
            if pattern_entry["phrase"].lower() == validation_lower:
                return pattern_entry["phrase"]
            
            # Check aliases
            for alias in pattern_entry.get("aliases", []):
                if alias.lower() == validation_lower:
                    return pattern_entry["phrase"]
                
                # Check regex patterns
                if alias.startswith("^") and alias.endswith("$"):
                    import re
                    try:
                        if re.match(alias, validation_lower, re.IGNORECASE):
                            return pattern_entry["phrase"]
                    except re.error:
                        continue
        
        return None
    
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
