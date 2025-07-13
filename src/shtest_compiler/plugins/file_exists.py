"""
Plugin for file exists validation.
"""

class FileExists:
    def __init__(self, groups, scope="global"):
        self.file = groups[0] if groups else ""
        self.scope = scope
    
    def to_shell(self, varname="result", last_file_var=None):
        file_path = self.file if self.file else last_file_var
        if not file_path:
            return [f"echo 'ERROR: No file specified for file_exists validation'"]
        
        return [
            f"{varname}=0",
            f"if [ -f '{file_path}' ]; then",
            f"    {varname}=1",
            "fi"
        ]

def handle(groups, scope="global"):
    return FileExists(groups, scope) 