class RunScriptAction:
    def __init__(self, groups):
        self.script = groups[0] if groups else None
    def to_shell(self, **kwargs):
        return [f"sh '{self.script}'"]
def handle(groups, **kwargs):
    return RunScriptAction(groups) 