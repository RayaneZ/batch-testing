from dataclasses import dataclass, field
from typing import List

@dataclass
class ShellScript:
    lines: List[str] = field(default_factory=list)
