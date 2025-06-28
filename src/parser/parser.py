import re
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Any
from parser.alias_resolver import AliasResolver



@dataclass
class Rule:
    pattern: re.Pattern
    handler: Callable[[re.Match, Dict[str, Any]], None]


class Parser:
    """Parser for structured French-like test scenario descriptions."""

    def __init__(self) -> None:
        self.rules: List[Rule] = []
        self.action_result_re: Optional[re.Pattern] = None
        self.arg_pattern = re.compile(r"(?:argument|paramètre|et\s+(?:l['ae]|l'))\s*(\S+)=\s*(\S+)", re.I)
        self._register_default_rules()

    def _register(self, pattern: str, handler: Callable[[re.Match, Dict[str, Any]], None]) -> None:
        self.rules.append(Rule(re.compile(pattern, re.I), handler))

    def _register_default_rules(self) -> None:
        self.action_result_re = re.compile(r"Action\s*:\s*(.*?)\s*(?:R[ée]sultat)\s*:?\s*(.*)", re.I)
        self._register(self.action_result_re.pattern, self._handle_action_result)

        simple_rules = [
            (r"(?:Étape|Etape|Step)\s*:\s*(.*)", lambda m, a: a["steps"].append(m[1].strip())),
            (r"(créer|configurer)(?!.*(?:dossier|fichier|=))", lambda m, a: a["initialization"].append(m.string.strip())),
            (r"initialiser(?!.*?\.sql)", lambda m, a: a["initialization"].append(m.string.strip())),
            (r"exécuter.*?\.sql", self._handle_sql_script),
            (r"(?:exécuter|lancer|traiter)\s+(\S+\.sh)", lambda m, a: a.update({"batch_path": m[1]})),
            (r"(exécuter|lancer|traiter)", lambda m, a: a["execution"].append(m.string.strip())),
            (r"(?:vérifier|valider)\s+que\s+(.*)", lambda m, a: a["validation"].append(m[1].rstrip('.;').strip())),
            (r"(logs|erreurs|fichiers de logs)", lambda m, a: a["logs_check"].append(m.string.strip())),
            (self.arg_pattern.pattern, self._handle_arguments),
            (r"d[ée]finir la variable\s+(\w+)\s*=\s*([^;]+)", self._handle_variable),
            (r"R[ée]sultat\s*:\s*(.*)", self._handle_result_only),
            (r"(?:chemin|path) des logs\s*=\s*(\S+)", lambda m, a: a["log_paths"].append(m[1])),
            (r"script sql\s*=\s*(.*?\.sql)", lambda m, a: a["sql_scripts"].append(m[1]) if m[1] not in a["sql_scripts"] else None),
            (r"(cr[ée]er|mettre\s+(?:à|a)\s+jour)\s+(fichier|dossier)\s*=\s*(\S+)\s*(?:avec les droits|mode)\s*=\s*(\S+)",
             lambda m, a: a["file_operations"].append((m[1], m[2], m[3], m[4]))),
            (r"cr[ée]er\s+le\s+dossier\s*=?\s*(\S+)", lambda m, a: a["file_operations"].append(("créer", "dossier", m[1], "0755"))),
            (r"cr[ée]er\s+le\s+fichier\s*=?\s*(\S+)", lambda m, a: a["file_operations"].append(("créer", "fichier", m[1], "0644"))),
            (r"mettre\s+(?:à|a)\s+jour\s+la\s+date\s+du\s+fichier\s*(\S+)\s*(\d{8,14})?", lambda m, a: a["touch_files"].append((m[1], m[2]))),
            (r"touch(?:er)?(?:\s+le\s+fichier)?\s*(\S+)(?:\s+(?:-t\s*)?(\d{8,14}))?", lambda m, a: a["touch_files"].append((m[1], m[2]))),
            (r"(copier|d\xE9placer)\s+(?:le\s+)?(fichier|dossier)?\s*(\S+)\s+vers\s+(\S+)",
             lambda m, a: a["copy_operations"].append((m[1], m[2] or "fichier", m[3], m[4]))),
            (r"(?:afficher le contenu du fichier|cat le fichier|lire le fichier)\s*=?\s*(\S+)",
             lambda m, a: a["cat_files"].append(m[1])),
            (r"(?:vider|purger)\s+le\s+(?:r[eé]pertoire|dossier)\s*=?\s*(\S+)",
             lambda m, a: a["purge_dirs"].append(m[1])),
        ]

        for pattern, handler in simple_rules:
            self._register(pattern, handler)

    def _handle_arguments(self, match: re.Match, actions: Dict[str, Any]) -> None:
        for m in self.arg_pattern.finditer(match.string):
            actions["arguments"][m[1].strip()] = m[2].strip()

    def _handle_variable(self, match: re.Match, actions: Dict[str, Any]) -> None:
        actions["arguments"][match[1].strip()] = match[2].strip()

    def _handle_result_only(self, match: re.Match, actions: Dict[str, Any]) -> None:
        result = match[1].rstrip('.;').strip()
        if result:
            resolver = AliasResolver()
            actions["validation"].extend(resolver.resolve(result))

    def _handle_sql_script(self, match: re.Match, actions: Dict[str, Any]) -> None:
        scripts = re.findall(r"\S+\.sql", match.string, re.I)
        for path in scripts:
            if path not in actions["sql_scripts"]:
                actions["sql_scripts"].append(path)

    def _handle_action_result(self, match: re.Match, actions: Dict[str, Any]) -> None:
        sub_parser = Parser()
        sub_actions = sub_parser.parse(match[1])

        for key, value in sub_actions.items():
            if key == "batch_path" and value:
                actions[key] = value
            elif isinstance(value, dict):
                actions[key].update(value)
            elif isinstance(value, list):
                actions[key].extend(value)

        result = match[2].rstrip('.;').strip()
        if result:
            resolver = AliasResolver()
            actions["validation"].extend(resolver.resolve(result))

    def parse(self, description: str) -> Dict[str, Any]:
        actions = {
            "initialization": [], "execution": [], "validation": [],
            "logs_check": [], "arguments": {}, "log_paths": [],
            "sql_scripts": [], "file_operations": [], "copy_operations": [],
            "cat_files": [], "touch_files": [], "purge_dirs": [],
            "steps": [], "batch_path": None,
        }

        for line in description.splitlines():
            for rule in self.rules:
                match = rule.pattern.search(line)
                if match:
                    rule.handler(match, actions)
                    if self.action_result_re and rule.pattern.pattern == self.action_result_re.pattern:
                        break
        return actions
