from shtest_compiler.utils.canonicalization import get_canonical_phrase_and_opposite

class StderrContainsValidation:
    def __init__(self, groups, scope="global"):
        self.text = groups[0] if groups else ""
        self.scope = scope
    def to_shell(self, varname="result", last_file_var=None):
        phrase, opposite = get_canonical_phrase_and_opposite("stderr_contains", plugin_name="stderr")
        if not self.text:
            return [f"echo 'ERROR: No text specified for stderr_contains validation'"]
        return [
            f"expected='{phrase}'",
            f"if echo \"$stderr\" | grep -q \"{self.text}\"; then actual='{phrase}'; else actual='{opposite}'; fi",
            f"{varname}=1; [ \"$actual\" = \"$expected\" ] || {varname}=0"
        ]
def handle(groups, scope="global"):
    return StderrContainsValidation(groups, scope) 