class DeleteDirAction:
    def __init__(self, groups):
        self.path = groups[0] if groups else None
    def to_shell(self, **kwargs):
        return [f"rm -rf '{self.path}'"]
def handle(groups, **kwargs):
    return DeleteDirAction(groups) 