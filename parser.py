"""Utility module to parse natural language test descriptions."""

from dataclasses import dataclass
from typing import Callable, Dict, List
import re

@dataclass
class Rule:
    pattern: re.Pattern
    handler: Callable[[re.Match, Dict[str, List]], None]

class Parser:
    """A modular parser based on a set of regex rules."""

    def __init__(self) -> None:
        self.rules: List[Rule] = []
        self._register_default_rules()

    def _register(self, pattern: str, handler: Callable[[re.Match, Dict[str, List]], None]) -> None:
        compiled = re.compile(pattern, re.IGNORECASE)
        self.rules.append(Rule(compiled, handler))

    def _register_default_rules(self) -> None:
        # Simple actions
        self._register(r"(initialiser|créer|configurer)",
                       lambda m, a: a["initialization"].append(m.string.strip()))
        self._register(r"(exécuter|lancer|traiter)",
                       lambda m, a: a["execution"].append(m.string.strip()))
        self._register(r"(?:vérifier|valider)\s+que\s+(.*)",
                       lambda m, a: a["validation"].append(m.group(1).rstrip('.').strip()))
        self._register(r"(logs|erreurs|fichiers de logs)",
                       lambda m, a: a["logs_check"].append(m.string.strip()))

        # Dynamic extractions
        self._register(r"(?:argument|paramètre)\s+(\S+)\s*=\s*(\S+)",
                       lambda m, a: a["arguments"].__setitem__(m.group(1).strip(), m.group(2).strip()))
        self._register(r"(?:chemin|path) des logs\s*=\s*(\S+)",
                       lambda m, a: a["log_paths"].append(m.group(1)))
        self._register(r"script sql\s*=\s*(.*?\.sql)",
                       lambda m, a: a["sql_scripts"].append(m.group(1)))
        self._register(r"(créer|mettre à jour) (fichier|dossier)\s*=\s*(\S+)\s*(?:avec les droits|mode)\s*=\s*(\S+)",
                       lambda m, a: a["file_operations"].append((m.group(1), m.group(3), m.group(4))))
        self._register(r"(?:afficher le contenu du fichier|cat le fichier)\s*=\s*(\S+)",
                       lambda m, a: a["cat_files"].append(m.group(1)))

    def parse(self, description: str) -> Dict[str, List]:
        actions: Dict[str, List] = {
            "initialization": [],
            "execution": [],
            "validation": [],
            "logs_check": [],
            "arguments": {},
            "log_paths": [],
            "sql_scripts": [],
            "file_operations": [],
            "cat_files": [],
        }

        for line in description.splitlines():
            for rule in self.rules:
                match = rule.pattern.search(line)
                if match:
                    rule.handler(match, actions)
        return actions
