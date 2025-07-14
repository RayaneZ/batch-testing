from shtest_compiler.utils.canonicalization import \
    get_canonical_phrase_and_opposite


class BaseReadyValidation:
    def __init__(self, groups, scope="global", canonical_phrase=None):
        self.scope = scope
        self.canonical_phrase = canonical_phrase or "la base est prête"

    def to_shell(self, varname="result", last_file_var=None):
        phrase = self.canonical_phrase
        opposite = phrase.replace("prête", "non prête")
        # Placeholder: check for a file named 'db_ready.flag' to simulate DB readiness
        return [
            f"expected='{phrase}'",
            f"if [ -f 'db_ready.flag' ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle(groups, scope="global", canonical_phrase=None):
    return BaseReadyValidation(groups, scope, canonical_phrase)
