class FileCopiedValidation:
    def __init__(self, groups):
        pass
    def to_shell(self, **kwargs):
        return ["echo 'File copied validation - stub'"]
def handle(groups, **kwargs):
    return FileCopiedValidation(groups) 