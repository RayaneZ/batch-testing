class MkdirCommand:
    def __init__(self, path):
        self.path = path
    def to_shell(self):
        return f'run_cmd "mkdir -p {self.path}"'

def handle(groups):
    path, = groups
    return MkdirCommand(path=path) 