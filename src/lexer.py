import re
from dataclasses import dataclass
from typing import Iterator, Optional

@dataclass
class Token:
    kind: str
    value: str
    lineno: int
    result: Optional[str] = None
    original: Optional[str] = None

_STEP_RE = re.compile(r"^(?:Étape|Etape|Step)\s*:\s*(.*)", re.IGNORECASE)
_ACTION_RESULT_RE = re.compile(
    r"^Action\s*:\s*(.*?)\s*(?:R[ée]sultat|Resultat)\s*:?\s*(.*)", re.IGNORECASE
)
_ACTION_ONLY_RE = re.compile(r"^Action\s*:\s*(.*)", re.IGNORECASE)

def lex(text: str, nested: bool = False) -> Iterator[Token]:
    """Tokenize the contents of a ``.shtest`` file.

    If *nested* is True, additional tokens are emitted for the
    expressions inside actions and results.
    """
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        m = _STEP_RE.match(stripped)
        if m:
            yield Token("STEP", m.group(1).strip(), lineno, original=line)
            continue
        m = _ACTION_RESULT_RE.match(stripped)
        if m:
            action = m.group(1).strip()
            result = m.group(2).strip()
            yield Token(
                "ACTION_RESULT",
                action,
                lineno,
                result=result,
                original=line,
            )
            if nested:
                yield Token("ACTION_EXPR", action, lineno, original=line)
                if result:
                    yield Token("RESULT_EXPR", result, lineno, original=line)
            continue
        m = _ACTION_ONLY_RE.match(stripped)
        if m:
            action = m.group(1).strip()
            yield Token("ACTION_ONLY", action, lineno, original=line)
            if nested:
                yield Token("ACTION_EXPR", action, lineno, original=line)
            continue
        yield Token("TEXT", stripped, lineno, original=line)

def lex_file(path: str, nested: bool = False) -> Iterator[Token]:
    """Read *path* and yield :class:`Token` objects."""
    with open(path, encoding="utf-8") as f:
        yield from lex(f.read(), nested=nested)
