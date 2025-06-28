import re
from typing import Callable, Dict, List, Tuple, Optional, Any

class AliasResolver:
    """Maps verbose French test outputs to canonical validation tokens."""

    def __init__(self) -> None:
        self.aliases = self._build_aliases()

    def _build_aliases(self) -> List[Tuple[re.Pattern, Callable[[re.Match], List[str]]]]:
        def tok(s): return s.strip()

        return [
            (re.compile(r"le script retourne un code\s*(\d+)", re.I), lambda m: [f"retour {m[1]}"]),
            (re.compile(r"le script affiche un code\s*\"?(\d+)\"?", re.I), lambda m: [f"stdout contient {m[1]}"]),
            (re.compile(r"la sortie standard est\s*(.+)", re.I), lambda m: [f"stdout={tok(m[1])}"]),
            (re.compile(r"la sortie standard contient\s*(.+)", re.I), lambda m: [f"stdout contient {tok(m[1])}"]),
            (re.compile(r"la sortie d'?erreur est\s*(.+)", re.I), lambda m: [f"stderr={tok(m[1])}"]),
            (re.compile(r"la sortie d'?erreur contient\s*(.+)", re.I), lambda m: [f"stderr contient {tok(m[1])}"]),
            (re.compile(r"le fichier\s+(\S+)\s+(?:existe|est présent)", re.I), lambda m: [f"le fichier {m[1]} existe"]),
            (re.compile(r"le fichier\s+est\s+(?:présent|copi[ée]|initialis[eé])", re.I), lambda m: ["Le fichier est présent"]),
            (re.compile(r"(?:le\s+)?fichier(?:\s+est)?\s+cr[eé]{1,2}e?", re.I), lambda m: ["fichier cree"]),
            (re.compile(r"le dossier\s+est\s+(?:copi[ée])", re.I), lambda m: ["le dossier est copié"]),
            (re.compile(r"le dossier\s+est\s+(?:pr[êe]t|cr[eé]{1,2}e?)", re.I), lambda m: ["dossier créé"]),
            (re.compile(r"le script s'?ex[ée]cute\s+avec\s+succ[eè]s", re.I), lambda m: ["retour 0"]),
            (re.compile(r"le fichier\s+(\S+)\s+est identique(?:\s+[àa])?\s*(\S+)", re.I), lambda m: [f"fichier_identique {m[1]} {m[2]}"]),
            (re.compile(r"les?\s+fichiers\s+sont\s+identiques", re.I), lambda m: ["les fichiers sont identiques"]),
            (re.compile(r"la base(?: de test)?\s+est\s+pr[êe]te", re.I), lambda m: ["base prête"]),
            (re.compile(r"le contenu\s+est\s+(?:affich[ée]|correct|lisible)", re.I), lambda m: ["contenu affiché" if "lisible" in m[0] or "affich" in m[0] else "contenu correct"]),
            (re.compile(r"aucun message d'?erreur", re.I), lambda m: ["stderr="]),
            (re.compile(r"les logs sont accessibles", re.I), lambda m: ["logs accessibles"]),
            (re.compile(r"les?\s+identifiants?\s+(?:sont\s+)?configur[ée]s", re.I), lambda m: ["identifiants configurés"]),
        ]

    def resolve(self, text: str) -> List[str]:
        """Return canonical tokens for *text* if it matches a known alias."""
        cleaned = text.strip().rstrip('.;')
        for pattern, handler in self.aliases:
            match = pattern.fullmatch(cleaned)
            if match:
                return handler(match)
        return [cleaned]
