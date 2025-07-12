class TouchCommand:
    def __init__(self, path, timestamp=None):
        self.path = path
        self.timestamp = timestamp
    def to_shell(self):
        if self.timestamp:
            return f'run_cmd "touch -t {self.timestamp} {self.path}"'
        else:
            return f'run_cmd "touch {self.path}"'

def handle(groups):
    path, timestamp = groups
    return TouchCommand(path=path, timestamp=timestamp) 