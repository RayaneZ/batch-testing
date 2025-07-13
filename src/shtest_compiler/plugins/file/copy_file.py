class CopyFileAction:
    def __init__(self, groups):
        self.src = groups[0] if len(groups) > 0 else None
        self.dest = groups[1] if len(groups) > 1 else None
    def to_shell(self, **kwargs):
        return [f"cp '{self.src}' '{self.dest}'"]
def handle(groups, **kwargs):
    return CopyFileAction(groups) 