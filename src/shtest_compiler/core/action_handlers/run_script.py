from shtest_compiler.ast.shell_framework_ast import ActionNode

class RunScriptAction(ActionNode):
    def __init__(self, script):
        self.script = script
    def to_shell(self):
        return f"sh '{self.script}'"

def handle(params):
    script = params['script']
    return RunScriptAction(script) 