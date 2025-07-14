def shell_escape(value):
    """Escape a string for safe use in single-quoted shell strings."""
    if value is None:
        return ""
    return "'" + str(value).replace("'", "'\\''") + "'" 