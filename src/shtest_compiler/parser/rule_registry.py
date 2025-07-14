import re
from typing import Any, Callable, Dict, Optional

from shtest_compiler.common_patterns import SIMPLE_RULES


def build_handler_map() -> Dict[str, Callable[..., None]]:
    return {
        "initialization": lambda a, text: a["initialization"].append(text.strip()),
        "set_variable": lambda a, name, value: a["arguments"].update(
            {name: value.strip()}
        ),
        "sql_script": lambda a, line: _handle_sql_script_text(line, a),
        "batch_script": lambda a, path: a.update({"batch_path": path}),
        "execution": lambda a, text: a["execution"].append(text.strip()),
        "validation": lambda a, expr: a["validation"].append(expr.rstrip(".;").strip()),
        "logs_check": lambda a, text: a["logs_check"].append(text.strip()),
        "arguments": lambda a, name, value: a["arguments"].update(
            {name.strip(): value.strip()}
        ),
        "variable": lambda a, name, value: a["arguments"].update(
            {name.strip(): value.strip()}
        ),
        "log_path": lambda a, path: a["log_paths"].append(path),
        "sql_script_single": lambda a, script: (
            a["sql_scripts"].append(script) if script not in a["sql_scripts"] else None
        ),
        "file_op": lambda a, op, typ, path, mode: a["file_operations"].append(
            (op, typ, path, mode)
        ),
        "create_dir": lambda a, path: a["file_operations"].append(
            ("créer", "dossier", path, "0755")
        ),
        "create_file": lambda a, path: a["file_operations"].append(
            ("créer", "fichier", path, "0644")
        ),
        "touch_date": lambda a, path, ts=None: a["touch_files"].append((path, ts)),
        "touch": lambda a, path, ts=None: a["touch_files"].append((path, ts)),
        "compare_files": lambda a, src, dest: a["compare_files"].append((src, dest)),
        "copy_move": lambda a, op, typ, src, dest: a["copy_operations"].append(
            (op, typ or "fichier", src, dest)
        ),
        "cat": lambda a, f: a["cat_files"].append(f),
        "step": lambda a, name: a["steps"].append(name.strip()),
    }


def _handle_sql_script_text(line: str, actions: Dict[str, Any]) -> None:
    # Ajoute tous les fichiers *.sql trouvés dans la ligne
    scripts = re.findall(r"\S+\.sql", line, re.IGNORECASE)
    for script in scripts:
        if script not in actions["sql_scripts"]:
            actions["sql_scripts"].append(script)


def load_default_rules(handler_map: Dict[str, Callable]) -> list:
    rules = []
    for rule in SIMPLE_RULES:
        pattern = rule["pattern"]
        handler_spec = rule["handler"]
        handler = _make_handler(handler_spec, handler_map)
        rules.append((re.compile(pattern, re.I), handler))
    return rules


def _make_handler(spec: str, handler_map: Dict[str, Callable]) -> Callable:
    """Build a rule handler from *spec* using *handler_map*.

    The *spec* syntax supports positional placeholders like ``{1}`` and
    optional placeholders ``{{2}}`` which are replaced by the respective
    regex groups when present. This mirrors the logic used by
    :class:`Parser` so ``simple_rules.yml`` can be shared between the
    module and the CLI parser.
    """

    tokens = spec.split()
    name = tokens[0]
    arg_specs = tokens[1:]

    def get_value(match: re.Match, token: str) -> Optional[str]:
        if token.startswith("{{") and token.endswith("}}"):
            idx = int(token[2:-2])
            return match.group(idx) if idx <= match.lastindex else None
        if token.startswith("{") and token.endswith("}"):
            idx = int(token[1:-1])
            return match.group(idx)
        return token

    def handler(match: re.Match, actions: Dict[str, Any]) -> None:
        args = [get_value(match, t) for t in arg_specs]
        handler_map[name](actions, *args)

    return handler
