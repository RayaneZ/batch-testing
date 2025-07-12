class MoveDirCommand:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def to_shell(self):
        return f'run_cmd "mv {self.src} {self.dest}"'

def handle(groups):
    src, dest = groups
    return MoveDirCommand(src=src, dest=dest) 