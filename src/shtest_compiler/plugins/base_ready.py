class BaseReadyValidation:
    def __init__(self, groups):
        pass
    def to_shell(self, **kwargs):
        return ["echo 'Base ready validation - stub'"]
def handle(groups, **kwargs):
    return BaseReadyValidation(groups) 