from shtest_compiler.ast.shell_framework_ast import ActionNode


class ExportVarAction(ActionNode):
    def __init__(self, var, value):
        self.var = var
        self.value = value

    def to_shell(self):
        return f"export {self.var}='{self.value}'"


def handle(params):
    var = params["var"]
    value = params["value"]
    return ExportVarAction(var, value)
