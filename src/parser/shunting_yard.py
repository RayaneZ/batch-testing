from dataclasses import dataclass
from typing import List
import re
from parser.parser import AliasResolver

@dataclass
class ASTNode:
    pass

@dataclass
class Atomic(ASTNode):
    value: str

@dataclass
class BinaryOp(ASTNode):
    op: str  # 'et' or 'ou'
    left: ASTNode
    right: ASTNode


def _tokenize_expression(expr: str) -> List[str]:
    """Split a validation expression into tokens."""
    return [t.strip() for t in re.split(r"(\bet\b|\bou\b|\(|\))", expr) if t.strip()]


def _to_postfix(tokens: List[str]) -> List[str]:
    """Convert infix tokens to postfix notation using the shunting-yard algorithm."""
    precedence = {"et": 2, "ou": 1}
    output: List[str] = []
    stack: List[str] = []
    for tok in tokens:
        ltok = tok.lower()
        if ltok in precedence:
            while stack and stack[-1].lower() in precedence and precedence[stack[-1].lower()] >= precedence[ltok]:
                output.append(stack.pop())
            stack.append(ltok)
        elif tok == "(":
            stack.append(tok)
        elif tok == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if stack and stack[-1] == "(":
                stack.pop()
        else:
            output.append(tok)
    while stack:
        output.append(stack.pop())
    return output


def parse_validation_expression(expression: str) -> ASTNode:
    """Parse a validation expression into an AST."""
    # Resolve aliases so that the AST only contains canonical forms
    resolver = AliasResolver()
    tokens = _tokenize_expression(expression)
    tokens = [resolver.resolve(t)[0] if t not in ("et", "ou", "(", ")") else t for t in tokens]
    postfix = _to_postfix(tokens)
    stack: List[ASTNode] = []
    for tok in postfix:
        if tok in ("et", "ou"):
            right = stack.pop()
            left = stack.pop()
            stack.append(BinaryOp(tok, left, right))
        else:
            stack.append(Atomic(tok))
    return stack.pop() if stack else Atomic("")
