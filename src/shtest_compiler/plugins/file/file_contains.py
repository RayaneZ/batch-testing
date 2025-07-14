class FileContainsValidation:
    def __init__(self, groups):
        self.file = groups[0] if len(groups) > 0 else None
        self.text = groups[1] if len(groups) > 1 else None

    def to_shell(self, **kwargs):
        return [f"grep -q \"{self.text}\" '{self.file}'"]


def handle(groups, **kwargs):
    return FileContainsValidation(groups)
