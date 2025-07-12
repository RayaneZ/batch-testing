class CatFileCommand:
    def __init__(self, path):
        self.path = path
    def to_shell(self):
        return f'run_cmd "cat {self.path}"'

def handle(groups):
    path, = groups
    return CatFileCommand(path=path) 