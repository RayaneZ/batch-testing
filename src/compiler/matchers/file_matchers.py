import re

def match(expected, last_file_var):
    for fn in [_match_file_exists, _match_file_contains_exact, _match_file_contains, _match_dir_file_count]:
        result = fn(expected, last_file_var)
        if result:
            return result
    return None

def _match_file_exists(expected, last_file_var):
    m = re.search(r"le fichier (\S+) existe", expected, re.IGNORECASE)
    if m:
        path = m.group(1)
        last_file_var[0] = path
        return [f"if [ -e {path} ]; then actual=\"le fichier {path} existe\"; else actual=\"le fichier {path} absent\"; fi", f"expected=\"le fichier {path} existe\""]
    return None

def _match_file_contains_exact(expected, _):
    m = re.search(r"le fichier (\S+) contient exactement\s*(.+)", expected, re.IGNORECASE)
    if m:
        path, value = m.groups()
        return [f"actual=$(cat {path})", f"expected=\"{value}\""]
    return None

def _match_file_contains(expected, _):
    m = re.search(r"le fichier (\S+) contient\s*(.+)", expected, re.IGNORECASE)
    if m:
        path, pattern = m.groups()
        return [f"if grep -q {pattern!r} {path}; then actual={pattern!r}; else actual=\"\"; fi", f"expected={pattern!r}"]
    return None

def _match_dir_file_count(expected, _):
    m = re.search(r"le dossier (\S+) contient\s*(\d+)\s*fichiers?(?:\s+(.*))?", expected, re.IGNORECASE)
    if m:
        path, count, pat = m.groups()
        search = f"-name {pat!r}" if pat else "-type f"
        return [f"actual=$(find {path} -maxdepth 1 {search} | wc -l)", f"expected={count}"]
    return None