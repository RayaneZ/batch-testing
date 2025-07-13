from shtest_compiler.ast.shell_framework_ast import ActionNode

class TouchTimestampAction(ActionNode):
    def __init__(self, timestamp, path):
        self.timestamp = timestamp
        self.path = path
    def to_shell(self):
        return f"touch -t '{self.timestamp}' '{self.path}'"

def handle(params):
    timestamp = params['timestamp']
    path = params['path']
    return TouchTimestampAction(timestamp, path) 