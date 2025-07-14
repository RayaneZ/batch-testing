from shtest_compiler.utils.canonicalization import get_canonical_phrase_and_opposite


class DirMovedValidation:
    def __init__(self, source=None, destination=None):
        self.source = source
        self.destination = destination

    def to_shell(self, varname="result", last_file_var=None):
        phrase, opposite = get_canonical_phrase_and_opposite(
            "dir_moved", plugin_name="dir"
        )
        if not self.source or not self.destination:
            return [f"echo 'ERROR: Missing directory(ies) for dir_moved validation'"]
        return [
            f"expected='{phrase}'",
            f"if [ $last_ret -eq 0 ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle(groups, scope=None):
    source = groups[0] if len(groups) > 0 else None
    destination = groups[1] if len(groups) > 1 else None
    return DirMovedValidation(source, destination)
