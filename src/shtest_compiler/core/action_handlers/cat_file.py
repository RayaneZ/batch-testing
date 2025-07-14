from shtest_compiler.ast.shell_framework_ast import ActionNode


class CatFileAction(ActionNode):
    def __init__(self, path):
        self.path = path

    def to_shell(self):
        return f"cat '{self.path}'"


def handle(params):
    path = params["path"]
    return CatFileAction(path)
