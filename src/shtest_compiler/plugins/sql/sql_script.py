class SQLScriptCommand:
    def __init__(self, script):
        self.script = script
    def to_shell(self):
        return f'run_cmd "sqlplus -s ${{SQL_CONN}} @{self.script}"'
 
def handle(groups):
    script, = groups
    return SQLScriptCommand(script=script) 