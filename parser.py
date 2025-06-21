"""Utility module to parse natural language test descriptions."""

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple, Optional, Any
import re

@dataclass
class Rule:
    pattern: re.Pattern
    handler: Callable[[re.Match, Dict[str, Any]], None]

class Parser:
    """A modular parser based on a set of regex rules."""

    def __init__(self) -> None:
        self.rules: List[Rule] = []
        self.action_result_re: Optional[re.Pattern] = None
        self._register_default_rules()

    def _register(self, pattern: str, handler: Callable[[re.Match, Dict[str, List]], None]) -> None:
        compiled = re.compile(pattern, re.IGNORECASE)
        self.rules.append(Rule(compiled, handler))

    def _register_default_rules(self) -> None:
        # Action/Result grammar should be evaluated first
        pattern = r"Action\s*:\s*(.*?)\s*(?:Résultat|Resultat)\s*:?\s*(.*)"
        self.action_result_re = re.compile(pattern, re.IGNORECASE)
        self._register(pattern, self._handle_action_result)

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
        self._register(r"(créer|mettre à jour) (?:le\s+)?(fichier|dossier)\s*=\s*(\S+)\s*(?:avec les droits|mode)\s*=\s*(\S+)",
                       lambda m, a: a["file_operations"].append((m.group(1), m.group(2), m.group(3), m.group(4))))
        self._register(r"mettre à jour la date du fichier\s*(\S+)\s*(\d{8,14})?",
                       lambda m, a: a["touch_files"].append((m.group(1), m.group(2))))
        self._register(r"touch(?:er)?(?:\s+le\s+fichier)?\s*(\S+)(?:\s+(?:-t\s*)?(\d{8,14}))?",
                       lambda m, a: a["touch_files"].append((m.group(1), m.group(2))))
        self._register(r"exécuter\s+(\/\S+\.sh)",
                       lambda m, a: a.__setitem__("batch_path", m.group(1)))
        self._register(r"(?:afficher le contenu du fichier|cat le fichier)\s*=\s*(\S+)",
                       lambda m, a: a["cat_files"].append(m.group(1)))

    def _handle_action_result(self, match: re.Match, actions: Dict[str, List]) -> None:
        """Parse a line written as 'Action: ... Resultat: ...'."""
        sub_parser = Parser()
        sub_actions = sub_parser.parse(match.group(1))
        for key, value in sub_actions.items():
            if key == "batch_path" and value:
                actions[key] = value
            elif isinstance(value, dict):
                actions[key].update(value)
            elif isinstance(value, list):
                actions[key].extend(value)
        result = match.group(2).rstrip('.').strip()
        if result:
            actions["validation"].append(result)

    def parse(self, description: str) -> Dict[str, Any]:
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
            "touch_files": [],
            "batch_path": None,
        }

        for line in description.splitlines():
            for rule in self.rules:
                match = rule.pattern.search(line)
                if match:
                    rule.handler(match, actions)
                    if self.action_result_re and rule.pattern.pattern == self.action_result_re.pattern:
                        break

        return actions
