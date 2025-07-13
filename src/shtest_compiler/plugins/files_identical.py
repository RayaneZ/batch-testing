import re

class FilesIdenticalValidation:
    def __init__(self, groups):
        self.file1 = groups[0] if len(groups) > 0 else None
        self.file2 = groups[1] if len(groups) > 1 else None
    def to_shell(self, **kwargs):
        return [f"cmp -s '{self.file1}' '{self.file2}'"]
def handle(groups, **kwargs):
    return FilesIdenticalValidation(groups) 