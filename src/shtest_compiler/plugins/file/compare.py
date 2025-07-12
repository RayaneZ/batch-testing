class FileCompareValidation:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
    def to_shell(self, var):
        return f'diff -q {self.file1} {self.file2} >/dev/null && {var}=1 || {var}=0'

def handle(groups, scope=None):
    file1, file2 = groups
    return FileCompareValidation(file1, file2) 