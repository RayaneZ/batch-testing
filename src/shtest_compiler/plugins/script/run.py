class ScriptCommand:
    def __init__(self, script):
        self.script = script
    def to_shell(self):
        return f'run_cmd "{self.script}"'

def handle(groups):
    script, = groups
    return ScriptCommand(script=script) 