class DeleteDirCommand:
    def __init__(self, path):
        self.path = path
    def to_shell(self):
        return f'run_cmd "rm -rf {self.path}"'

def handle(groups):
    path, = groups
    return DeleteDirCommand(path=path) 