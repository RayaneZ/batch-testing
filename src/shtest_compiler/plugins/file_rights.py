from shtest_compiler.utils.canonicalization import \
    get_canonical_phrase_and_opposite


class FileRightsValidation:
    def __init__(self, groups, scope="global"):
        self.file = groups[0] if len(groups) > 0 else None
        self.mode = groups[1] if len(groups) > 1 else None
        self.scope = scope

    def to_shell(self, varname="result", last_file_var=None):
        file_path = self.file if self.file else last_file_var
        phrase, opposite = get_canonical_phrase_and_opposite(
            "file_rights", plugin_name="file"
        )
        if not file_path or not self.mode:
            return [f"echo 'ERROR: Missing file or mode for file_rights validation'"]
        return [
            f"expected='{phrase}'",
            f"if [ $(stat -c '%a' '{file_path}') = '{self.mode}' ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle(groups, scope="global"):
    return FileRightsValidation(groups, scope)
