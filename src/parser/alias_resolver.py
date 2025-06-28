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
            (re.compile(r"le fichier\s+est\s+(?:présent|copi[ée])", re.I), lambda m: ["Le fichier est présent"]),
            (re.compile(r"le dossier\s+est\s+(?:copi[ée]|prêt)", re.I), lambda m: ["le dossier est copié"]),
            (re.compile(r"le fichier\s+(\S+)\s+est identique(?:\s+[àa])?\s*(\S+)", re.I), lambda m: [f"fichier_identique {m[1]} {m[2]}"]),
            (re.compile(r"fichier\s+cr[eé]{1,2}e?", re.I), lambda m: ["fichier cree"]),
            (re.compile(r"la base(?: de test)?\s+est\s+pr[êe]te", re.I), lambda m: ["base prête"]),
            (re.compile(r"le contenu\s+est\s+(?:affich[ée]|correct|lisible)", re.I), lambda m: ["contenu affiché" if "lisible" in m[0] or "affich" in m[0] else "contenu correct"]),
            (re.compile(r"aucun message d'?erreur", re.I), lambda m: ["stderr="]),
            (re.compile(r"les logs sont accessibles", re.I), lambda m: ["logs accessibles"]),
            (re.compile(r"les?\s+identifiants?\s+(?:sont\s+)?configur[ée]s", re.I), lambda m: ["identifiants configurés"]),
        ]

    def resolve(self, text: str) -> List[str]:
        for pattern, handler in self.aliases:
            match = pattern.search(text)
            if match:
                return handler(match)
        return [text]
