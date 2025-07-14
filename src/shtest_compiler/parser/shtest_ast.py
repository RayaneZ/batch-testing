from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Action:
    command: str  # Ligne de commande
    result_expr: Optional[str]  # Expression attendue (str brute)
    result_ast: Optional[object]  # ASTNode compilé (représentation logique)
    lineno: int  # Numéro de ligne dans le fichier test
    raw_line: Optional[str] = None  # Ligne originale brute


@dataclass
class TestStep:
    name: str  # preparation / execution / validation / logs_check
    lineno: int
    actions: List[Action] = field(default_factory=list)


@dataclass
class ShtestFile:
    steps: List[TestStep] = field(default_factory=list)
    variables: Dict[str, str] = field(
        default_factory=dict
    )  # SQL_DRIVER, SQL_CONN, etc.
    arguments: Dict[str, str] = field(default_factory=dict)  # Legacy argument storage
    last_file_var: List[Optional[str]] = field(default_factory=lambda: [None])
    path: Optional[str] = None

    def get_grouped_steps(self) -> Dict[str, List[Action]]:
        grouped = {
            "preparation": [],
            "execution": [],
            "validation": [],
            "logs_check": [],
        }
        for step in self.steps:
            if step.name in grouped:
                grouped[step.name].extend(step.actions)
        return grouped

    def set_variable(self, name: str, value: str):
        self.variables[name.strip()] = value.strip()

    def get_variable(self, name: str) -> Optional[str]:
        return self.variables.get(name.strip())

    def add_step(self, name: str, lineno: int):
        step = TestStep(name=name, lineno=lineno)
        self.steps.append(step)
        return step
