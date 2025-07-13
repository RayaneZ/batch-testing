class DirCopiedValidation:
    def __init__(self, groups):
        pass
    def to_shell(self, **kwargs):
        return ["echo 'Directory copied validation - stub'"]
def handle(groups, **kwargs):
    return DirCopiedValidation(groups) 