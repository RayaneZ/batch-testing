"""
Plugin for file empty validation.
"""

class FileEmptyValidation:
    def __init__(self, groups):
        self.file = groups[0] if groups else None
    def to_shell(self, **kwargs):
        return [f"[ ! -s '{self.file}' ]"]
def handle(groups, **kwargs):
    return FileEmptyValidation(groups) 