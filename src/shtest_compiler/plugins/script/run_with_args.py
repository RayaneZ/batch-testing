class ScriptWithArgsCommand:
    def __init__(self, script, args):
        self.script = script
        self.args = args

    def to_shell(self):
        return f'run_cmd "{self.script} {self.args}"'


def handle(groups):
    script, args = groups
    # On remplace ' et ' par ' ' pour concaténer les arguments
    args = args.replace(" et ", " ")
    return ScriptWithArgsCommand(script, args)
