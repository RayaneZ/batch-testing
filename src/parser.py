"""Utility module to parse natural language test descriptions.

This module exposes a :class:`Parser` capable of reading test scenarios
written in a French-like language and turning them into a structured
dictionary describing all actions to perform and validations to check.
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple, Optional, Any
import re


class AliasResolver:
    """Convert literary phrases into canonical validation tokens.

    The generator only understands a small set of validation expressions
    (``retour N``, ``stdout=...`` etc.).  This class maps more verbose
    sentences found in ``.shtest`` files to those atomic forms.
    """

    def __init__(self) -> None:
        # Each entry associates a regex with a function returning canonical
        # strings. The first match wins.
        self.aliases: List[Tuple[re.Pattern, Callable[[re.Match], List[str]]]] = [
            (
                re.compile(r"le script retourne un code\s*(\d+)", re.IGNORECASE),
                lambda m: [f"retour {m.group(1)}"],
            ),  # "Le script retourne un code 0" -> "retour 0"
            (
                re.compile(r"le script affiche un code\s*\"?(\d+)\"?", re.IGNORECASE),
                lambda m: [f"stdout contient {m.group(1)}"],
            ),  # "affiche un code 030" -> "stdout contient 030"
            (
                re.compile(r"la sortie standard est\s*(.+)", re.IGNORECASE),
                lambda m: [f"stdout={m.group(1).strip()}"]
            ),
            (
                re.compile(r"la sortie standard contient\s*(.+)", re.IGNORECASE),
                lambda m: [f"stdout contient {m.group(1).strip()}"]
            ),
            (
                re.compile(r"la sortie d'?erreur est\s*(.+)", re.IGNORECASE),
                lambda m: [f"stderr={m.group(1).strip()}"]
            ),
            (
                re.compile(r"la sortie d'?erreur contient\s*(.+)", re.IGNORECASE),
                lambda m: [f"stderr contient {m.group(1).strip()}"]
            ),
            (
                re.compile(r"le fichier\s+(\S+)\s+(?:existe|est présent)", re.IGNORECASE),
                lambda m: [f"le fichier {m.group(1)} existe"]
            ),
            (
                re.compile(r"le fichier\s+est\s+pr[eé]sent", re.IGNORECASE),
                lambda m: ["Le fichier est présent"]
            ),
            (
                re.compile(r"le fichier\s+est\s+copié", re.IGNORECASE),
                lambda m: ["le fichier est copié"]
            ),
            (
                re.compile(r"le dossier\s+est\s+copié", re.IGNORECASE),
                lambda m: ["le dossier est copié"]
            ),
            (
                re.compile(r"le fichier\s+(\S+)\s+est identique(?:\s+[àa])?\s*(\S+)", re.IGNORECASE),
                lambda m: [f"fichier_identique {m.group(1)} {m.group(2)}"]
            ),
            (
                re.compile(r"le fichier\s+est\s+initialis[ée]", re.IGNORECASE),
                lambda m: ["Le fichier est présent"]
            ),
            (
                re.compile(r"le fichier\s+est\s+cr[eé]{1,2}e?", re.IGNORECASE),
                lambda m: ["Le fichier est présent"]
            ),
            (
                re.compile(r"fichier\s+cr[eé]{1,2}e?", re.IGNORECASE),
                lambda m: ["fichier cree"]
            ),
            (
                re.compile(r"la base(?: de test)?\s+est\s+pr[êe]te(?:\s+pour le test)?", re.IGNORECASE),
                lambda m: ["base prête"]
            ),
            (
                re.compile(r"le contenu\s+est\s+affich[ée]", re.IGNORECASE),
                lambda m: ["contenu affiché"]
            ),
            (
                re.compile(r"le script\s+est\s+affich[ée]", re.IGNORECASE),
                lambda m: ["contenu affiché"]
            ),
            (
                re.compile(r"le dossier\s+est\s+cr[eé]{1,2}e?", re.IGNORECASE),
                lambda m: ["dossier créé"]
            ),
            (
                re.compile(r"le dossier\s+est\s+pr[êe]t", re.IGNORECASE),
                lambda m: ["dossier créé"]
            ),
            (
                re.compile(r"la date\s+est\s+modifi[eé]e?", re.IGNORECASE),
                lambda m: ["date modifiée"]
            ),
            (
                re.compile(r"date\s+modifi[eé]e?", re.IGNORECASE),
                lambda m: ["date modifiée"]
            ),
            (
                re.compile(r"le contenu\s+est\s+correct", re.IGNORECASE),
                lambda m: ["contenu correct"]
            ),
            (
                re.compile(r"le contenu\s+est\s+lisible", re.IGNORECASE),
                lambda m: ["contenu affiché"]
            ),
            (
                re.compile(r"aucun message d'?erreur", re.IGNORECASE),
                lambda m: ["stderr="]
            ),
            (
                re.compile(r"les logs sont accessibles", re.IGNORECASE),
                lambda m: ["logs accessibles"]
            ),
        ]

    def resolve(self, text: str) -> List[str]:
        for pattern, handler in self.aliases:
            m = pattern.search(text)
            if m:
                return handler(m)
        return [text]

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
        """Register a new parsing rule.

        Parameters
        ----------
        pattern: str
            Regular expression describing the rule.
        handler: Callable
            Function called when the pattern matches a line. It must mutate
            the ``actions`` dictionary passed to :meth:`parse`.
        """
        compiled = re.compile(pattern, re.IGNORECASE)
        self.rules.append(Rule(compiled, handler))

    def _register_default_rules(self) -> None:
        """Populate the parser with all built-in regex rules.

        The order of registration matters: some expressions are subsets of
        others and must therefore be checked first.  The very first rule
        handles the ``Action: ... Resultat: ...`` form which may itself
        contain nested actions.
        """
        # Action/Result grammar should be evaluated first
        pattern = r"Action\s*:\s*(.*?)\s*(?:Résultat|Resultat)\s*:?\s*(.*)"
        self.action_result_re = re.compile(pattern, re.IGNORECASE)
        self._register(pattern, self._handle_action_result)

        # Step markers
        self._register(r"(?:Étape|Etape|Step)\s*:\s*(.*)",
                       lambda m, a: a["steps"].append(m.group(1).strip()))

        # Simple actions
        self._register(
            r"(créer|configurer)(?!.*(?:dossier|fichier|=))",
            lambda m, a: a["initialization"].append(m.string.strip()),
        )
        # Connection setup instructions commonly start with "initialiser".
        # We only capture them as initialization when they don't reference
        # a SQL script which would be executed explicitly.
        self._register(
            r"initialiser(?!.*?\.sql)",
            lambda m, a: a["initialization"].append(m.string.strip()),
        )
        # SQL scripts are executed via an explicit instruction such as
        # "Exécuter le script SQL = nom.sql".
        self._register(r"exécuter.*?\.sql",
                       self._handle_sql_script)
        self._register(r"(?:exécuter|lancer|traiter)\s+(\S+\.sh)",
                       lambda m, a: a.__setitem__("batch_path", m.group(1)))
        self._register(r"(exécuter|lancer|traiter)",
                       lambda m, a: a["execution"].append(m.string.strip()))
        self._register(r"(?:vérifier|valider)\s+que\s+(.*)",
                       lambda m, a: a["validation"].append(m.group(1).rstrip('.;').strip()))
        self._register(r"(logs|erreurs|fichiers de logs)",
                       lambda m, a: a["logs_check"].append(m.string.strip()))

        # Dynamic extractions
        self.arg_pattern = re.compile(r"(?:argument|paramètre|et\s+(?:l['ae]\s+|l')?)\s*(\S+)=\s*(\S+)", re.IGNORECASE)
        self._register(self.arg_pattern.pattern,
                       self._handle_arguments)
        self._register(r"(?:chemin|path) des logs\s*=\s*(\S+)",
                       lambda m, a: a["log_paths"].append(m.group(1)))
        self._register(
            r"script sql\s*=\s*(.*?\.sql)",
            lambda m, a: a["sql_scripts"].append(m.group(1))
            if m.group(1) not in a["sql_scripts"] else None,
        )
        self._register(r"(cr[ée]er|mettre\s+(?:à|a)\s+jour) (?:le\s+)?(fichier|dossier)\s*=\s*(\S+)\s*(?:avec les droits|mode)\s*=\s*(\S+)",
                       lambda m, a: a["file_operations"].append((m.group(1), m.group(2), m.group(3), m.group(4))))
        # Simple directory creation without explicit mode
        self._register(r"cr[ée]er\s+le\s+dossier\s*=?\s*(\S+)",
                       lambda m, a: a["file_operations"].append(("créer", "dossier", m.group(1), "0755")))
        self._register(r"cr[ée]er\s+le\s+fichier\s*=?\s*(\S+)",
                       lambda m, a: a["file_operations"].append(("créer", "fichier", m.group(1), "0644")))
        self._register(r"mettre\s+(?:à|a)\s+jour\s+la\s+date\s+du\s+fichier\s*(\S+)\s*(\d{8,14})?",
                       lambda m, a: a["touch_files"].append((m.group(1), m.group(2))))
        self._register(r"touch(?:er)?(?:\s+le\s+fichier)?\s*(\S+)(?:\s+(?:-t\s*)?(\d{8,14}))?",
                       lambda m, a: a["touch_files"].append((m.group(1), m.group(2))))
        self._register(r"(copier|d\xE9placer)\s+(?:le\s+)?(fichier|dossier)?\s*(\S+)\s+vers\s+(\S+)",
                       lambda m, a: a["copy_operations"].append((m.group(1), m.group(2) or "fichier", m.group(3), m.group(4))))
        self._register(r"(?:afficher le contenu du fichier|cat le fichier|lire le fichier)\s*=?\s*(\S+)",
                       lambda m, a: a["cat_files"].append(m.group(1)))

    def _handle_arguments(self, match: re.Match, actions: Dict[str, List]) -> None:
        """Extract all key=value pairs from an argument expression."""
        for m in self.arg_pattern.finditer(match.string):
            actions["arguments"][m.group(1).strip()] = m.group(2).strip()

    def _handle_sql_script(self, match: re.Match, actions: Dict[str, List]) -> None:
        """Register the SQL script referenced in the instruction."""
        # Only register the SQL script so that the generator executes it once.
        script = re.search(r"(\S+\.sql)", match.string, re.IGNORECASE)
        if script:
            path = script.group(1)
            if path not in actions["sql_scripts"]:
                actions["sql_scripts"].append(path)

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
        result = match.group(2).rstrip('.;').strip()
        if result:
            if re.search(r"\bet\b|\bou\b|\(|\)", result):
                actions["validation"].append(result)
            else:
                resolver = AliasResolver()
                for res in resolver.resolve(result):
                    actions["validation"].append(res)

    def parse(self, description: str) -> Dict[str, Any]:
        """Parse a block of text and return a dictionary of actions."""

        # Structure accumulating all recognized actions. Lists are used so
        # that order is preserved when generating shell scripts.
        actions: Dict[str, List] = {
            "initialization": [],
            "execution": [],
            "validation": [],
            "logs_check": [],
            "arguments": {},
            "log_paths": [],
            "sql_scripts": [],
            "file_operations": [],
            "copy_operations": [],
            "cat_files": [],
            "touch_files": [],
            "steps": [],
            "batch_path": None,
        }

        for line in description.splitlines():
            # Apply each rule to the current line. Some rules may also
            # trigger nested parsing (see ``_handle_action_result``).
            for rule in self.rules:
                match = rule.pattern.search(line)
                if match:
                    rule.handler(match, actions)
                    # Once "Action ... Resultat" has matched we stop
                    # evaluating other patterns for this line.
                    if self.action_result_re and rule.pattern.pattern == self.action_result_re.pattern:
                        break

        return actions
