from shtest_compiler.utils.canonicalization import get_canonical_phrase_and_opposite


class ContentDisplayedValidation:
    def __init__(self, groups, scope="global", canonical_phrase=None):
        self.file = groups[0] if groups and groups[0] else None
        self.scope = scope
        self.canonical_phrase = canonical_phrase or "le contenu est affiché"

    def to_shell(self, varname="result", last_file_var=None):
        file_path = self.file if self.file else last_file_var
        if not file_path:
            return [f"echo 'ERROR: No file specified for content_displayed validation'"]
        phrase = self.canonical_phrase
        if "{file}" in phrase:
            phrase = phrase.replace("{file}", file_path)
        opposite = phrase.replace("affiché", "non affiché")
        return [
            f"expected='{phrase}'",
            f"if [ -s '{file_path}' ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle(groups, scope="global", canonical_phrase=None):
    return ContentDisplayedValidation(groups, scope, canonical_phrase)


# Negation plugin
class ContentNotDisplayedValidation:
    def __init__(self, groups, scope="global", canonical_phrase=None):
        self.file = groups[0] if groups and groups[0] else None
        self.scope = scope
        self.canonical_phrase = canonical_phrase or "le contenu n'est pas affiché"

    def to_shell(self, varname="result", last_file_var=None):
        file_path = self.file if self.file else last_file_var
        if not file_path:
            return [
                f"echo 'ERROR: No file specified for content_not_displayed validation'"
            ]
        phrase = self.canonical_phrase
        if "{file}" in phrase:
            phrase = phrase.replace("{file}", file_path)
        opposite = phrase.replace("non affiché", "affiché")
        return [
            f"expected='{phrase}'",
            f"if [ ! -s '{file_path}' ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle_opposite(groups, scope="global", canonical_phrase=None):
    return ContentNotDisplayedValidation(groups, scope, canonical_phrase)
