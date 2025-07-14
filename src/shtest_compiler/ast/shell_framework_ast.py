from dataclasses import dataclass, field
from typing import List, Optional


class ActionNode:
    def to_shell(self) -> str:
        raise NotImplementedError("ActionNode subclasses must implement to_shell()")


@dataclass
class ShellFunctionDef:
    name: str
    params: List[str]
    body_lines: List[str]


@dataclass
class ShellFunctionCall:
    name: str
    args: List[str]


@dataclass
class InlineShellCode:
    code_lines: List[str]


@dataclass
class ValidationCheck:
    expected: str
    actual_cmd: str
    handler: str
    scope: str  # 'global' or 'local' (or 'last_action')
    params: dict = field(default_factory=dict)


@dataclass
class ShellTestStep:
    name: str
    actions: List[object]
    validations: List[object]


@dataclass
class ShellFrameworkAST:
    helpers: List[ShellFunctionDef] = field(default_factory=list)
    steps: List[ShellTestStep] = field(default_factory=list)
    global_code: List[str] = field(default_factory=list)


def pretty_print_ast(node, indent=0):
    prefix = " " * indent
    if isinstance(node, list):
        for item in node:
            pretty_print_ast(item, indent)
    elif hasattr(node, "__dataclass_fields__"):
        print(f"{prefix}{node.__class__.__name__}(")
        for field_name in node.__dataclass_fields__:
            value = getattr(node, field_name)
            print(f"{prefix}  {field_name}:")
            pretty_print_ast(value, indent + 4)
        print(f"{prefix})")
    elif isinstance(node, ActionNode):
        print(f"{prefix}{node.__class__.__name__}(to_shell={node.to_shell()!r})")
    else:
        print(f"{prefix}{repr(node)}")
