"""
Plugin for file present validation.
"""


class FilePresentValidation:
    def __init__(self, groups, scope="global", canonical_phrase=None):
        self.file = groups[0] if groups else ""
        self.scope = scope
        self.canonical_phrase = canonical_phrase or "le fichier {file} est présent"

    def to_shell(self, varname="result", last_file_var=None, **kwargs):
        file_path = self.file if self.file else last_file_var
        if not file_path:
            return [f"echo 'ERROR: No file specified for file_present validation'"]
        expected = self.canonical_phrase.replace("{file}", file_path)
        opposite = expected.replace("présent", "absent")
        return [
            f"expected='{expected}'",
            f"if [ -f '{file_path}' ]; then actual='{expected}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle(groups, scope="global", canonical_phrase=None):
    return FilePresentValidation(groups, scope, canonical_phrase=canonical_phrase)


# Negation plugin
class FileAbsent:
    def __init__(self, groups, scope="global", canonical_phrase=None):
        self.file = groups[0] if groups else ""
        self.scope = scope
        self.canonical_phrase = canonical_phrase or "le fichier {file} est absent"

    def to_shell(self, varname="result", last_file_var=None, **kwargs):
        file_path = self.file if self.file else last_file_var
        if not file_path:
            return [f"echo 'ERROR: No file specified for file_absent validation'"]
        expected = self.canonical_phrase.replace("{file}", file_path)
        opposite = expected.replace("absent", "présent")
        return [
            f"expected='{expected}'",
            f"if [ ! -f '{file_path}' ]; then actual='{expected}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle_opposite(groups, scope="global", canonical_phrase=None):
    return FileAbsent(groups, scope, canonical_phrase=canonical_phrase)
