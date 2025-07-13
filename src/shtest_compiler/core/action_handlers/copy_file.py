from shtest_compiler.ast.shell_framework_ast import ActionNode

class CopyFileAction(ActionNode):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def to_shell(self):
        return f"cp '{self.src}' '{self.dest}'"

def handle(params):
    src = params['src']
    dest = params['dest']
    return CopyFileAction(src, dest) 