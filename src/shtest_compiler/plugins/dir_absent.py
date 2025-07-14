from shtest_compiler.utils.canonicalization import \
    get_canonical_phrase_and_opposite


class DirAbsentValidation:
    def __init__(self, groups, scope="global"):
        self.dir = groups[0] if groups else ""
        self.scope = scope

    def to_shell(self, varname="result", last_file_var=None):
        dir_path = self.dir if self.dir else last_file_var
        phrase, opposite = get_canonical_phrase_and_opposite(
            "dir_absent", plugin_name="dir"
        )
        if not dir_path:
            return [f"echo 'ERROR: No directory specified for dir_absent validation'"]
        return [
            f"expected='{phrase}'",
            f"if [ ! -d '{dir_path}' ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle(groups, scope="global"):
    return DirAbsentValidation(groups, scope)
