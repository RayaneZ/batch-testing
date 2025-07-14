class FileEmptyValidation:
    def __init__(self, file):
        self.file = file

    def to_shell(self, var):
        return f'if [ ! -s "{self.file}" ]; then {var}=1; else {var}=0; fi'


def handle(groups, scope=None):
    (file,) = groups
    return FileEmptyValidation(file)
