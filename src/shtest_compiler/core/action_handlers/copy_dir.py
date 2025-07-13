from shtest_compiler.ast.shell_framework_ast import ActionNode

class CopyDirAction(ActionNode):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def to_shell(self):
        return f"cp -r '{self.src}' '{self.dest}'"

def handle(params):
    src = params['src']
    dest = params['dest']
    return CopyDirAction(src, dest) 