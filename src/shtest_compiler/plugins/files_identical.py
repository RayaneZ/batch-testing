import re

from shtest_compiler.utils.canonicalization import \
    get_canonical_phrase_and_opposite


class FilesIdenticalValidation:
    def __init__(self, groups):
        self.file1 = groups[0] if len(groups) > 0 else None
        self.file2 = groups[1] if len(groups) > 1 else None

    def to_shell(self, varname="result", last_file_var=None):
        phrase, opposite = get_canonical_phrase_and_opposite(
            "files_identical", plugin_name="file"
        )
        if not self.file1 or not self.file2:
            return [f"echo 'ERROR: Missing file(s) for files_identical validation'"]
        return [
            f"expected='{phrase}'",
            f"if [ -f '{self.file1}' ] && [ -f '{self.file2}' ]; then cmp -s '{self.file1}' '{self.file2}' && actual='{phrase}' || actual='{opposite}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle(groups, **kwargs):
    return FilesIdenticalValidation(groups)
