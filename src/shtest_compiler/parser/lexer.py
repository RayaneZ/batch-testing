# Importation du décorateur dataclass pour simplifier la déclaration de classes de données
from dataclasses import dataclass

# Importation des types pour l'annotation de type
from typing import Iterator, Optional

# Importation de motifs regex utilisés pour identifier les différents types de lignes
from shtest_compiler.common_patterns import (
    ACTION_ONLY_RE,
    ACTION_RESULT_RE,
    RESULT_ONLY_RE,
    STEP_RE,
    COMMENT_RE,
)

# Définition de la structure de données Token pour représenter une ligne analysée
@dataclass
class Token:
    kind: str                    # Type de jeton (STEP, ACTION_ONLY, etc.)
    value: str                   # Contenu principal du jeton
    lineno: int                  # Numéro de ligne dans le fichier source
    result: Optional[str] = None  # Résultat attendu (si applicable)
    original: Optional[str] = None  # Ligne originale complète

# Fonction principale d'analyse lexicale
def lex(text: str, debug: bool = False) -> Iterator[Token]:
    """Tokenize the contents of a `.shtest` file."""
    # Parcours de chaque ligne du texte, avec suivi du numéro de ligne
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()  # Suppression des espaces autour de la ligne

        # Ignorer les lignes vides
        if not stripped:
            continue

        # Ignorer les lignes correspondant à des commentaires
        if COMMENT_RE.match(stripped):
            continue

        # Correspond à une ligne de type STEP (étape)
        m = STEP_RE.match(stripped)
        if m:
            t = Token("STEP", m.group(1).strip(), lineno, original=line)
            if debug: print(f"[LEX] STEP @{lineno}: '{t.value}'")
            yield t
            continue

        # Correspond à une ligne contenant une action suivie d'un résultat
        m = ACTION_RESULT_RE.match(stripped)
        if m:
            t = Token(
                "ACTION_RESULT",
                m.group(1).strip(),         # Partie action
                lineno,
                result=m.group(2).strip(),  # Partie résultat
                original=line,
            )
            if debug: print(f"[LEX] ACTION_RESULT @{lineno}: '{t.value}' -> '{t.result}'")
            yield t
            continue

        # Correspond à une ligne contenant uniquement une action
        m = ACTION_ONLY_RE.match(stripped)
        if m:
            t = Token("ACTION_ONLY", m.group(1).strip(), lineno, original=line)
            if debug: print(f"[LEX] ACTION_ONLY @{lineno}: '{t.value}'")
            yield t
            continue

        # Correspond à une ligne contenant uniquement un résultat
        m = RESULT_ONLY_RE.match(stripped)
        if m:
            t = Token("RESULT_ONLY", m.group(1).strip(), lineno, original=line)
            if debug: print(f"[LEX] RESULT_ONLY @{lineno}: '{t.value}'")
            yield t
            continue

        # Si aucune expression régulière ne correspond, on la considère comme du texte brut
        t = Token("TEXT", stripped, lineno, original=line)
        if debug: print(f"[LEX] TEXT @{lineno}: '{t.value}'")
        yield t

# Fonction utilitaire pour lire un fichier et le passer à la fonction lex
def lex_file(path: str) -> Iterator[Token]:
    """Read *path* and yield :class:`Token` objects."""
    with open(path, encoding="utf-8") as f:
        # Analyse lexicale du contenu du fichier
        yield from lex(f.read())
