class ValidationParseError(Exception):
    """Raised when a validation phrase cannot be matched or parsed."""
    pass

class HandlerNotFoundError(Exception):
    """Raised when a handler (plugin or core) cannot be found."""
    pass

class ParameterExtractionError(Exception):
    """Raised when parameters cannot be extracted from a phrase or alias."""
    pass 