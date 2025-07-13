class ExportVarAction:
    def __init__(self, groups):
        self.var = groups[0] if len(groups) > 0 else None
        self.value = groups[1] if len(groups) > 1 else None
    def to_shell(self, **kwargs):
        return [f"export {self.var}='{self.value}'"]
def handle(groups, **kwargs):
    return ExportVarAction(groups) 