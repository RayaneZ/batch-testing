"""
AST (Abstract Syntax Tree) nodes based on the formal grammar.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .visitor import ASTNode

# ===== Base AST Nodes =====


@dataclass
class Program(ASTNode):
    """Root node representing a complete .shtest program"""

    lines: List["Line"] = field(default_factory=list)

    def add_line(self, line: "Line"):
        """Add a line to the program"""
        self.lines.append(line)


@dataclass
class Line(ASTNode):
    """Base class for all line types"""

    lineno: int
    raw_text: str


# ===== Line Types =====


@dataclass
class Comment(Line):
    """Comment line starting with #"""

    text: str


@dataclass
class Step(Line):
    """Step definition: Step: NomDeStep"""

    name: str


@dataclass
class ActionResultLine(Line):
    """Single line with action and result: Action: Instruction; Résultat: ExpressionLogique"""

    action: "Instruction"
    result: "ExpressionLogique"


@dataclass
class ActionResultTwoLines(Line):
    """Action and result on separate lines"""

    action: "Instruction"
    result: "ExpressionLogique"


@dataclass
class ResultOnly(Line):
    """Result only line: Résultat: ExpressionLogique"""

    result: "ExpressionLogique"


# ===== Expression Nodes =====


@dataclass
class Instruction(ASTNode):
    """Instruction text (free form)"""

    text: str


@dataclass
class ExpressionLogique(ASTNode):
    """Logical expression: Terme { OperateurLogique Terme }"""

    terms: List["Terme"] = field(default_factory=list)
    operators: List["OperateurLogique"] = field(default_factory=list)

    def add_term(self, term: "Terme", operator: Optional["OperateurLogique"] = None):
        """Add a term with optional operator"""
        if operator and self.terms:
            self.operators.append(operator)
        self.terms.append(term)


@dataclass
class Terme(ASTNode):
    """Term in logical expression: ResultatSimple | (ExpressionLogique)"""

    value: "ResultatSimple | ExpressionLogique"


@dataclass
class ResultatSimple(ASTNode):
    """Simple result: Texte"""

    text: str


@dataclass
class OperateurLogique(ASTNode):
    """Logical operator: et | ou"""

    operator: str  # 'et' or 'ou'

    def __post_init__(self):
        if self.operator not in ["et", "ou"]:
            raise ValueError(f"Invalid logical operator: {self.operator}")


@dataclass
class Texte(ASTNode):
    """Text content: { Caractere }"""

    content: str


# ===== Utility Classes =====


@dataclass
class ParseError(Exception):
    """Parse error with line information"""

    message: str
    lineno: int
    line_content: str

    def __str__(self):
        return f"Parse error at line {self.lineno}: {self.message}\nLine: {self.line_content}"


# ===== Type Aliases for convenience =====
NomDeStep = Texte
Caractere = str
