import re

from shtest_compiler.compiler.matcher_registry import register_matcher

# ============================================================
# Orchestrateur de correspondance
# ============================================================


# Fonction de coordination : essaie chaque fonction de correspondance jusqu'à en trouver une qui renvoie un résultat.
# Utilise 'expected' (la consigne en texte) et 'last_file_var' (utilisé pour mémoriser un fichier pour usage ultérieur).
@register_matcher("file_matchers")
def match(expected, last_file_var):
    for fn in [
        _match_files_identical,
        _match_file_exists,
        _match_file_contains_exact,
        _match_file_contains,
        _match_dir_file_count,
        _match_dir_exists,
        _match_permissions,
        _match_file_timestamp,
    ]:
        result = fn(expected, last_file_var)
        if result:
            return result
    return None


# ============================================================
# Vérifications d'existence (fichier / dossier)
# ============================================================


# Vérifie si un fichier existe.
# Retourne un script shell qui teste l'existence et met à jour 'last_file_var'.
def _match_file_exists(expected, last_file_var):
    m = re.search(r"le fichier (\S+) existe", expected, re.IGNORECASE)
    if m:
        path = m.group(1)
        last_file_var[0] = path
        return [
            f'if [ -e {path} ]; then actual="le fichier {path} existe"; else actual="le fichier {path} absent"; fi',
            f'expected="le fichier {path} existe"',
        ]
    return None


# Vérifie si un dossier existe.
# Génère un test shell pour vérifier la présence du répertoire.
def _match_dir_exists(expected, _):
    m = re.search(r"le dossier (\S+) existe", expected, re.IGNORECASE)
    if m:
        path = m.group(1)
        return [
            f'if [ -d {path} ]; then actual="le dossier {path} existe"; else actual="le dossier {path} absent"; fi',
            f'expected="le dossier {path} existe"',
        ]
    return None


# ============================================================
# Vérification du contenu des fichiers et dossiers
# ============================================================


# Vérifie que le contenu d’un fichier est exactement égal à une valeur.
def _match_file_contains_exact(expected, _):
    m = re.search(
        r"le fichier (\S+) contient exactement\s*(.+)", expected, re.IGNORECASE
    )
    if m:
        path, value = m.groups()
        return [f"actual=$(cat {path})", f'expected="{value}"']
    return None


# Vérifie qu’un fichier contient un motif donné (sans exigence d’exactitude).
def _match_file_contains(expected, _):
    m = re.search(r"le fichier (\S+) contient\s*(.+)", expected, re.IGNORECASE)
    if m:
        path, pattern = m.groups()
        return [
            f'if grep -q {pattern!r} {path}; then actual={pattern!r}; else actual=""; fi',
            f"expected={pattern!r}",
        ]
    return None


# Vérifie le nombre de fichiers présents dans un dossier, avec ou sans motif.
def _match_dir_file_count(expected, _):
    m = re.search(
        r"le dossier (\S+) contient\s*(\d+)\s*fichiers?(?:\s+(.*))?",
        expected,
        re.IGNORECASE,
    )
    if m:
        path, count, pat = m.groups()
        search = f"-name {pat!r}" if pat else "-type f"
        return [
            f"actual=$(find {path} -maxdepth 1 {search} | wc -l)",
            f"expected={count}",
        ]
    return None


# ============================================================
# Vérification des propriétés des fichiers (droits, date, comparaison)
# ============================================================


# Vérifie si deux fichiers sont identiques.
# Produit un script shell utilisant `diff` et retourne l’état d’égalité.
def _match_files_identical(expected, _):
    m = re.search(r"fichier_identique\s+(\S+)\s+(\S+)", expected, re.IGNORECASE)
    if m:
        src, dest = m.groups()
        return [
            f'if diff -q {src} {dest} >/dev/null; then actual="Les fichiers sont identiques"; else actual="Les fichiers sont différents"; fi',
            'expected="Les fichiers sont identiques"',
        ]
    return None


# Vérifie les permissions (droits) d’un fichier ou dossier.
# Utilise `stat` pour extraire les droits numériques et les comparer.
def _match_permissions(expected, _):
    m = re.search(
        r"(fichier|dossier)\s+(\S+)\s+a\s+les\s+droits\s+(\d+)", expected, re.IGNORECASE
    )
    if m:
        typ, path, mode = m.groups()
        test = "-f" if typ.lower().startswith("f") else "-d"
        return [
            f'if [ {test} {path} ] && [ \$(stat -c \'%a\' {path}) = {mode} ]; then actual="{typ} {path} a les droits {mode}"; else actual="{typ} {path} droits incorrects"; fi',
            f'expected="{typ} {path} a les droits {mode}"',
        ]
    return None


# Vérifie la date de modification d’un fichier sous forme de timestamp (YYYYMMDDhhmmss).
# Utilise `date -r` pour extraire la date de dernière modification du fichier.
def _match_file_timestamp(expected, _):
    m = re.search(r"la date du fichier (\S+) est (\d{8,14})", expected, re.IGNORECASE)
    if m:
        path, ts = m.groups()
        return [f"actual=$(date -r {path} +%Y%m%d%H%M%S)", f"expected={ts}"]
    return None
