from shtest_compiler.utils.canonicalization import get_canonical_phrase_and_opposite


class DirContainsCountValidation:
    def __init__(self, groups, scope="global"):
        self.dir = groups[0] if len(groups) > 0 else None
        self.count = groups[1] if len(groups) > 1 else None
        self.pattern = groups[2] if len(groups) > 2 else None
        self.scope = scope

    def to_shell(self, varname="result", last_file_var=None):
        dir_path = self.dir if self.dir else last_file_var
        phrase, opposite = get_canonical_phrase_and_opposite(
            "dir_contains_count", plugin_name="dir"
        )
        if not dir_path or not self.count or not self.pattern:
            return [
                f"echo 'ERROR: Missing dir, count, or pattern for dir_contains_count validation'"
            ]
        return [
            f"expected='{phrase}'",
            f"actual=$(find '{dir_path}' -type f -name '{self.pattern}' | wc -l)",
            f"if [ \"$actual\" -eq {self.count} ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle(groups, scope="global"):
    return DirContainsCountValidation(groups, scope)
