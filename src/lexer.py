from dataclasses import dataclass
from typing import Iterator, Optional

from common_patterns import ACTION_ONLY_RE, ACTION_RESULT_RE, STEP_RE

@dataclass
class Token:
    kind: str
    value: str
    lineno: int
    result: Optional[str] = None
    original: Optional[str] = None


def lex(text: str) -> Iterator[Token]:
    """Tokenize the contents of a ``.shtest`` file."""
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        m = STEP_RE.match(stripped)
        if m:
            yield Token("STEP", m.group(1).strip(), lineno, original=line)
            continue
        m = ACTION_RESULT_RE.match(stripped)
        if m:
            yield Token(
                "ACTION_RESULT",
                m.group(1).strip(),
                lineno,
                result=m.group(2).strip(),
                original=line,
            )
            continue
        m = ACTION_ONLY_RE.match(stripped)
        if m:
            yield Token("ACTION_ONLY", m.group(1).strip(), lineno, original=line)
            continue
        yield Token("TEXT", stripped, lineno, original=line)

def lex_file(path: str) -> Iterator[Token]:
    """Read *path* and yield :class:`Token` objects."""
    with open(path, encoding="utf-8") as f:
        yield from lex(f.read())
