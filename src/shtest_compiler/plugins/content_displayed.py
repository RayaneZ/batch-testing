class ContentDisplayedValidation:
    def __init__(self, groups):
        pass
    def to_shell(self, **kwargs):
        return ["echo 'Content displayed validation - stub'"]
def handle(groups, **kwargs):
    return ContentDisplayedValidation(groups) 