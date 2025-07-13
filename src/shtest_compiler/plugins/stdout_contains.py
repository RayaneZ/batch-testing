"""
Plugin for stdout contains validation.
"""

from shtest_compiler.utils.canonicalization import get_canonical_phrase_and_opposite

class StdoutContainsValidation:
    def __init__(self, groups, scope="global"):
        self.text = groups[0] if groups else ""
        self.scope = scope
    def to_shell(self, varname="result", last_file_var=None):
        phrase, opposite = get_canonical_phrase_and_opposite("stdout_contains", plugin_name="stdout")
        if not self.text:
            return [f"echo 'ERROR: No text specified for stdout_contains validation'"]
        return [
            f"expected='{phrase}'",
            f"if echo \"$stdout\" | grep -q \"{self.text}\"; then actual='{phrase}'; else actual='{opposite}'; fi",
            f"{varname}=1; [ \"$actual\" = \"$expected\" ] || {varname}=0"
        ]
def handle(groups, scope="global"):
    return StdoutContainsValidation(groups, scope) 