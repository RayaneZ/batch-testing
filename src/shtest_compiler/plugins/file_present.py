"""
Plugin for file present validation.
"""

class FilePresentValidation:
    def __init__(self, groups):
        pass
    def to_shell(self, **kwargs):
        return ["echo 'File present validation - stub'"]
def handle(groups, **kwargs):
    return FilePresentValidation(groups)

# Negation plugin
class FileAbsent:
    def __init__(self, groups, scope="global"):
        self.file = groups[0] if groups else ""
        self.scope = scope
    def to_shell(self, varname="result", last_file_var=None):
        file_path = self.file if self.file else last_file_var
        if not file_path:
            return [f"echo 'ERROR: No file specified for file_absent validation'"]
        return [
            f"expected='Le fichier est absent'",
            f"if [ ! -f '{file_path}' ]; then actual='Le fichier est absent'; else actual='Le fichier est présent'; fi",
            f"{varname}=1; [ \"$actual\" = \"$expected\" ] || {varname}=0"
        ]

def handle_opposite(groups, scope="global"):
    return FileAbsent(groups, scope) 