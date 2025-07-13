class FileExistsValidation:
    def __init__(self, groups):
        self.file = groups[0] if groups else None
    def to_shell(self, **kwargs):
        return [f"[ -f '{self.file}' ]"]
def handle(groups, **kwargs):
    return FileExistsValidation(groups) 