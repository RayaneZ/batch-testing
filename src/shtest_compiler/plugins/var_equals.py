from shtest_compiler.utils.canonicalization import \
    get_canonical_phrase_and_opposite


class VarEqualsValidation:
    def __init__(self, groups, scope="global", canonical_phrase=None):
        self.var = groups[0] if len(groups) > 0 else ""
        self.value = groups[1] if len(groups) > 1 else ""
        self.scope = scope
        self.canonical_phrase = canonical_phrase or "variable {var} vaut {value}"

    def to_shell(self, **kwargs):
        # Substitute {var} and {value} in the canonical phrase
        expected = self.canonical_phrase.replace("{var}", self.var).replace(
            "{value}", self.value
        )
        opposite = expected.replace("vaut", "ne vaut pas")
        return [
            f"expected='{expected}'",
            f"if [ \"${self.var}\" = \"{self.value}\" ]; then actual='{expected}'; else actual='{opposite}'; fi",
            f'result=1; [ "$actual" = "$expected" ] || result=0',
        ]


def handle(groups, scope="global", canonical_phrase=None):
    return VarEqualsValidation(groups, scope, canonical_phrase=canonical_phrase)
