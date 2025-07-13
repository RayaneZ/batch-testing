class CatFileAction:
    def __init__(self, groups):
        self.path = groups[0] if groups else None
    def to_shell(self, **kwargs):
        return [f"cat '{self.path}'"]
def handle(groups, **kwargs):
    return CatFileAction(groups) 