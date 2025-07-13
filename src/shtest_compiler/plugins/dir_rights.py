from shtest_compiler.utils.canonicalization import get_canonical_phrase_and_opposite

class DirRightsValidation:
    def __init__(self, groups, scope="global"):
        self.dir = groups[0] if len(groups) > 0 else None
        self.mode = groups[1] if len(groups) > 1 else None
        self.scope = scope
    def to_shell(self, varname="result", last_file_var=None):
        dir_path = self.dir if self.dir else last_file_var
        phrase, opposite = get_canonical_phrase_and_opposite("dir_rights", plugin_name="dir")
        if not dir_path or not self.mode:
            return [f"echo 'ERROR: Missing dir or mode for dir_rights validation'"]
        return [
            f"expected='{phrase}'",
            f"if [ $(stat -c '%a' '{dir_path}') = '{self.mode}' ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f"{varname}=1; [ \"$actual\" = \"$expected\" ] || {varname}=0"
        ]
def handle(groups, scope="global"):
    return DirRightsValidation(groups, scope) 