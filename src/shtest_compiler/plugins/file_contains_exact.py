from shtest_compiler.utils.canonicalization import get_canonical_phrase_and_opposite


class FileContainsExactValidation:
    def __init__(self, groups, scope="global"):
        self.file = groups[0] if len(groups) > 0 else None
        self.text = groups[1] if len(groups) > 1 else None
        self.scope = scope

    def to_shell(self, varname="result", last_file_var=None):
        file_path = self.file if self.file else last_file_var
        phrase, opposite = get_canonical_phrase_and_opposite(
            "file_contains_exact", plugin_name="file"
        )
        if not file_path or not self.text:
            return [
                f"echo 'ERROR: Missing file or text for file_contains_exact validation'"
            ]
        return [
            f"expected='{phrase}'",
            f"if [ \"$(cat '{file_path}')\" = \"{self.text}\" ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle(groups, scope="global"):
    return FileContainsExactValidation(groups, scope)
