from parser.alias_utils import AliasResolver

def test_resolver_aliases():
    r = AliasResolver()
    assert r.resolve("identifiants configurés") == ["variable SQL_CONN définie"]
    assert r.resolve("stdout contient OK") == ["stdout.contains('OK')"]
    assert r.resolve("stderr vide") == ["stderr.contains('')"]
    assert r.resolve("inconnu") == ["inconnu"]
