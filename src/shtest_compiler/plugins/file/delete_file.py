class DeleteFileAction:
    def __init__(self, groups):
        self.path = groups[0] if groups else None
    def to_shell(self, **kwargs):
        return [f"rm '{self.path}'"]
def handle(groups, **kwargs):
    return DeleteFileAction(groups) 