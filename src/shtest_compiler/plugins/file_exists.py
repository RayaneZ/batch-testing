"""
Plugin for file exists validation.
"""

from shtest_compiler.utils.canonicalization import get_canonical_phrase_and_opposite

class FileExists:
    def __init__(self, groups, scope="global"):
        self.file = groups[0] if groups else ""
        self.scope = scope
    def to_shell(self, varname="result", last_file_var=None):
        file_path = self.file if self.file else last_file_var
        phrase, opposite = get_canonical_phrase_and_opposite("file_exists", plugin_name="file")
        if not file_path:
            return [f"echo 'ERROR: No file specified for file_exists validation'"]
        return [
            f"expected='{phrase}'",
            f"if [ -f '{file_path}' ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f"{varname}=1; [ \"$actual\" = \"$expected\" ] || {varname}=0"
        ]
def handle(groups, scope="global"):
    return FileExists(groups, scope)

# Negation plugin
class FileNotExistsValidation:
    def __init__(self, groups, scope="global"):
        self.file = groups[0] if groups else ""
        self.scope = scope
    def to_shell(self, varname="result", last_file_var=None):
        file_path = self.file if self.file else last_file_var
        phrase, opposite = get_canonical_phrase_and_opposite("file_not_exists", plugin_name="file")
        if not file_path:
            return [f"echo 'ERROR: No file specified for file_not_exists validation'"]
        return [
            f"expected='{phrase}'",
            f"if [ ! -f '{file_path}' ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f"{varname}=1; [ \"$actual\" = \"$expected\" ] || {varname}=0"
        ]
def handle_opposite(groups, scope="global"):
    return FileNotExistsValidation(groups, scope) 