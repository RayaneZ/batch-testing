from shtest_compiler.utils.canonicalization import get_canonical_phrase_and_opposite

class NoErrorMessageValidation:
    def __init__(self, groups):
        pass
    def to_shell(self, varname="result", last_file_var=None):
        phrase, opposite = get_canonical_phrase_and_opposite("no_error_message", plugin_name="no_error_message")
        # Assume stderr is redirected to 'stderr.log'
        return [
            f"expected='{phrase}'",
            "if [ ! -s 'stderr.log' ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f"{varname}=1; [ \"$actual\" = \"$expected\" ] || {varname}=0"
        ]
def handle(groups, **kwargs):
    return NoErrorMessageValidation(groups) 