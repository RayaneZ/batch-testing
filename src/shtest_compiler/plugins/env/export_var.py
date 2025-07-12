class ExportVarCommand:
    def __init__(self, var, value):
        self.var = var
        self.value = value
    def to_shell(self):
        return f'export {self.var}={self.value}'

def handle(groups):
    var, value = groups
    return ExportVarCommand(var=var, value=value) 