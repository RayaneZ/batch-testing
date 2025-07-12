class CopyDirCommand:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def to_shell(self):
        return f'run_cmd "cp -r {self.src} {self.dest}"'

def handle(groups):
    src, dest = groups
    return CopyDirCommand(src=src, dest=dest) 