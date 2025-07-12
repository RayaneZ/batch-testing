class CompareFilesCommand:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
    def to_shell(self):
        return f'run_cmd "diff {self.file1} {self.file2}"'

def handle(groups, scope=None):
    file1, file2 = groups
    return CompareFilesCommand(file1=file1, file2=file2) 