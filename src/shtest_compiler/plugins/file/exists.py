class FileExistsValidation:
    def __init__(self, path):
        self.path = path
    def to_shell(self, var):
        return f'if [ -f {self.path} ]; then {var}=1; else {var}=0; fi'

def handle(groups, scope=None):
    path, = groups
    return FileExistsValidation(path) 