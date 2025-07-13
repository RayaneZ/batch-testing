class NoErrorMessageValidation:
    def __init__(self, groups):
        pass
    def to_shell(self, **kwargs):
        return ["echo 'No error message validation - stub'"]
def handle(groups, **kwargs):
    return NoErrorMessageValidation(groups) 