from shtest_compiler.utils.canonicalization import \
    get_canonical_phrase_and_opposite


class CredentialsConfiguredValidation:
    def __init__(self, groups):
        self.var = groups[0] if groups else "SQL_CONN"

    def to_shell(self, varname="result", last_file_var=None):
        phrase, opposite = get_canonical_phrase_and_opposite(
            "credentials_configured", plugin_name="credentials_configured"
        )
        return [
            f"expected='{phrase}'",
            f"if [ -n \"${self.var}\" ]; then actual='{phrase}'; else actual='{opposite}'; fi",
            f'{varname}=1; [ "$actual" = "$expected" ] || {varname}=0',
        ]


def handle(groups, **kwargs):
    return CredentialsConfiguredValidation(groups)
