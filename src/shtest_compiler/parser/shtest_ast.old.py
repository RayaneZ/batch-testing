
from dataclasses import dataclass
from typing import Optional, List
from .shunting_yard import ASTNode

@dataclass
class Action:
    command: str
    result_expr: Optional[str]
    result_ast: Optional[ASTNode]
    lineno: int
    raw_line: Optional[str] = None

@dataclass
class TestStep:
    name: str
    lineno: int
    actions: List[Action]

@dataclass
class ShtestFile:
    steps: List[TestStep]
