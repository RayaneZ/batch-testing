from shtest_compiler.utils.canonicalization import \
    get_canonical_phrase_and_opposite


class DirCopiedValidation:
    def __init__(self, groups):
        self.dir1 = groups[0] if len(groups) > 0 else None
        self.dir2 = groups[1] if len(groups) > 1 else None

    def to_shell(self, varname="result", last_file_var=None):
        phrase, opposite = get_canonical_phrase_and_opposite(
            "dir_copied", plugin_name="dir"
        )
        if not self.dir1 or not self.dir2:
            return [f"echo 'ERROR: Missing directory(ies) for dir_copied validation'"]
        return [
            f"expected='{phrase}'",
            f"if [ -d '{self.dir1}' ] && [ -d '{self.dir2}' ]; then diff -r '{self.dir1}' '{self.dir2}' >/dev/null 2>&1 && actual='{phrase}' || actual='{opposite}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle(groups, **kwargs):
    return DirCopiedValidation(groups)
