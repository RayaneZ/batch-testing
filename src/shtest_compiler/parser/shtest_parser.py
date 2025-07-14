"""
Parser for .shtest files.

This module provides the main parser for converting .shtest files into AST nodes.
"""

from typing import List, Optional

from ..utils.logger import debug_log, is_debug_enabled
from .lexer import Token
from .shtest_ast import Action, ShtestFile, TestStep

debug_log("PARSER DEBUG ACTIVE: src/shtest_compiler/parser/shtest_parser.py loaded")


class ShtestParser:
    """Parser for .shtest files."""

    def __init__(self):
        """Initialize the parser."""
        self.debug = is_debug_enabled()

    def parse(self, tokens: List[Token]) -> ShtestFile:
        """
        Parse tokens into a ShtestFile AST.

        Args:
            tokens: List of tokens from the lexer

        Returns:
            ShtestFile AST node
        """
        shtest_file = ShtestFile()
        current_step = None
        pending_action = None
        orphan_actions = []

        for i, token in enumerate(tokens):
            if token.kind == "STEP":
                if self.debug:
                    debug_log(
                        f"Parser: Processing STEP token: value='{token.value}' at line {token.lineno}"
                    )

                # Add any pending action to the previous step
                if pending_action and current_step:
                    current_step.actions.append(pending_action)
                    pending_action = None

                # If this is the first step and there are orphans, add a synthetic step
                if current_step is None and orphan_actions:
                    if self.debug:
                        debug_log(
                            f"Parser: Creating synthetic 'Orphan Actions' step with {len(orphan_actions)} actions"
                        )
                    synthetic = TestStep(name="Orphan Actions", lineno=1)
                    synthetic.actions = orphan_actions.copy()
                    shtest_file.steps.append(synthetic)
                    orphan_actions.clear()

                # Create new test step
                current_step = TestStep(name=token.value, lineno=token.lineno)
                shtest_file.steps.append(current_step)

            elif token.kind == "ACTION_ONLY":
                if self.debug:
                    debug_log(
                        f"Parser: Processing ACTION_ONLY token: value='{token.value}' at line {token.lineno}"
                    )

                if pending_action and current_step:
                    current_step.actions.append(pending_action)

                pending_action = Action(
                    command=token.value,
                    result_expr=None,
                    result_ast=None,
                    lineno=token.lineno,
                )

                if current_step is None:
                    if self.debug:
                        debug_log(
                            f"Parser: Adding orphan action: {token.value}"
                        )
                    orphan_actions.append(pending_action)
                    pending_action = None

            elif token.kind == "RESULT_ONLY":
                if self.debug:
                    debug_log(
                        f"Parser: Processing RESULT_ONLY token: value='{token.value}' at line {token.lineno}"
                    )

                if pending_action:
                    pending_action.result_expr = token.value
                    if current_step:
                        current_step.actions.append(pending_action)
                    elif current_step is None:
                        if self.debug:
                            debug_log(
                                f"Parser: Adding orphan action with result: {pending_action.command} -> {token.value}"
                            )
                        orphan_actions.append(pending_action)
                    pending_action = None
                else:
                    action = Action(
                        command=None,
                        result_expr=token.value,
                        result_ast=None,
                        lineno=token.lineno,
                    )
                    if current_step:
                        current_step.actions.append(action)
                    elif current_step is None:
                        if self.debug:
                            debug_log(
                                f"Parser: Adding orphan result-only action: {token.value}"
                            )
                        orphan_actions.append(action)

            elif token.kind == "ACTION_RESULT":
                if self.debug:
                    debug_log(
                        f"Parser: Processing ACTION_RESULT token: value='{token.value}' at line {token.lineno}"
                    )

                if pending_action and current_step:
                    current_step.actions.append(pending_action)
                    pending_action = None

                parts = token.value.split("Résultat:", 1)
                if len(parts) == 2:
                    command = parts[0].replace("Action:", "").strip()
                    result_expr = parts[1].strip()
                    action = Action(
                        command=command,
                        result_expr=result_expr,
                        result_ast=None,
                        lineno=token.lineno,
                    )
                else:
                    action = Action(
                        command=token.value,
                        result_expr=None,
                        result_ast=None,
                        lineno=token.lineno,
                    )

                if current_step:
                    current_step.actions.append(action)
                elif current_step is None:
                    if self.debug:
                        debug_log(
                            f"Parser: Adding orphan action-result: {action.command} -> {action.result_expr}"
                        )
                    orphan_actions.append(action)

        # Add any remaining pending action to the last step or orphans
        if pending_action:
            if current_step:
                current_step.actions.append(pending_action)
            elif current_step is None:
                if self.debug:
                    debug_log(
                        f"Parser: Adding final orphan action: {pending_action.command}"
                    )
                orphan_actions.append(pending_action)

        # If there are still orphans at the end and no steps, add them as a synthetic step
        if orphan_actions and not shtest_file.steps:
            if self.debug:
                debug_log(
                    f"Parser: Creating final synthetic 'Orphan Actions' step with {len(orphan_actions)} actions"
                )
            synthetic = TestStep(name="Orphan Actions", lineno=1)
            synthetic.actions = orphan_actions
            shtest_file.steps.append(synthetic)

        return shtest_file
