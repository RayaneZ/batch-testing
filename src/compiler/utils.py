import unicodedata


def strip_accents(text: str) -> str:
    """Normalize *text* by removing accents for lenient comparisons."""
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )


def shell_condition(success_val: str, fail_val: str, expected_val: str | None = None) -> list[str]:
    """Return shell instructions validating that the last command succeeded."""
    if expected_val is None:
        expected_val = success_val
    return [
        f"if [ $last_ret -eq 0 ]; then actual=\"{success_val}\"; else actual=\"{fail_val}\"; fi",
        f"expected=\"{expected_val}\"",
    ]


def retcode_condition(code: int | str) -> list[str]:
    """Return instructions checking that ``$last_ret`` matches *code*."""
    code = int(code)
    return [
        f"if [ $last_ret -eq {code} ]; then actual=\"retour {code}\"; else actual=\"retour $last_ret\"; fi",
        f"expected=\"retour {code}\"",
    ]
