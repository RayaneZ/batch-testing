import yaml
import os
from shtest_compiler.ast.shell_framework_ast import (
    ShellFrameworkAST, ShellFunctionDef, ShellFunctionCall, InlineShellCode, ShellTestStep, ValidationCheck
)
from shtest_compiler.parser.shtest_ast import Action
from typing import Tuple, Dict, List
import re

# Use only the scope attribute on ValidationCheck

def is_global(validation):
    return getattr(validation, 'scope', 'last_action') == 'global'

def is_global_validation(node):
    # Atomic validation
    if hasattr(node, 'scope'):
        return getattr(node, 'scope', 'last_action') == 'global'
    # Compound node (BinaryOp)
    if hasattr(node, 'left') and hasattr(node, 'right'):
        return is_global_validation(node.left) and is_global_validation(node.right)
    # Not node (if you have one)
    if hasattr(node, 'child'):
        return is_global_validation(node.child)
    return False

class ShellFrameworkLifter:
    """
    Lifts global validations from action results to standalone validations.
    This processes the AST to separate action-dependent validations from global validations.
    """
    def __init__(self, ast: ShellFrameworkAST):
        self.ast = ast

    def lift(self) -> ShellFrameworkAST:
        """
        Lift global validations from action results to standalone validations.
        This transforms:
        - Action with global validation result -> Action + standalone validation
        - Action with local validation result -> Action with validation (unchanged)
        """
        for step in self.ast.steps:
            new_actions = []
            i = 0
            while i < len(step.actions):
                action = step.actions[i]
                
                # Check if this action contains validation logic that can be lifted
                if isinstance(action, InlineShellCode):
                    lifted_actions = self._process_inline_shell_code(action)
                    new_actions.extend(lifted_actions)
                else:
                    # Keep non-validation actions as-is
                    new_actions.append(action)
                
                i += 1
            
            step.actions = new_actions
        
        return self.ast
    
    def _process_inline_shell_code(self, action: InlineShellCode) -> List:
        """
        Process InlineShellCode to separate action execution from global validations.
        Returns a list of actions (original action + any lifted validations).
        """
        action_lines = []
        validation_lines = []
        
        for line in action.code_lines:
            if isinstance(line, ValidationCheck):
                # This is a validation - check if it can be lifted
                if self._is_global_validation(line):
                    validation_lines.append(line)
                else:
                    # Keep local validations with the action
                    action_lines.append(line)
            else:
                # This is action execution code - keep with action
                action_lines.append(line)
        
        result = []
        
        # Add the action (with any remaining local validations)
        if action_lines:
            result.append(InlineShellCode(code_lines=action_lines))
        
        # Add lifted validations as standalone actions
        for validation in validation_lines:
            result.append(validation)
        
        return result
    
    def _is_global_validation(self, validation) -> bool:
        """
        Check if a validation can be lifted (is global scope).
        """
        if hasattr(validation, 'scope'):
            return getattr(validation, 'scope', 'last_action') == 'global'
        
        # For compound validations, check if all parts are global
        if hasattr(validation, 'left') and hasattr(validation, 'right'):
            return (self._is_global_validation(validation.left) and 
                   self._is_global_validation(validation.right))
        
        # For NOT validations
        if hasattr(validation, 'child'):
            return self._is_global_validation(validation.child)
        
        # Default to local scope if we can't determine
        return False

class ShellFrameworkBinder:
    """
    Handles deduplication, parameter binding, and helper references in the AST.
    Should be run after ShellFrameworkLifter.
    """
    def __init__(self, ast: ShellFrameworkAST):
        self.ast = ast
        self.action_map: Dict[str, Tuple[ShellFunctionDef, List[str]]] = {}  # key -> (helper, param_names)
        self.helper_counter = 0

    def bind_missing_validation_params(self):
        """
        For each step, for each ValidationCheck, if any param is None,
        try to extract it from the associated action's command using regex.
        """
        for step in self.ast.steps:
            for action in step.actions:
                # Only process InlineShellCode or Action nodes with validations
                validations = getattr(action, 'validations', []) if hasattr(action, 'validations') else []
                for validation in validations:
                    if isinstance(validation, ValidationCheck):
                        for pname, pval in validation.params.items():
                            if pval is None:
                                val = self._extract_param_from_action_command(action, pname)
                                if val:
                                    validation.params[pname] = val

    def _extract_param_from_action_command(self, action, pname):
        """
        Try to extract a parameter value from the action's command string.
        Uses the existing action parameter extraction infrastructure.
        """
        if not hasattr(action, 'command') or not action.command:
            return None
        
        # Use the existing argument extraction logic
        from shtest_compiler.compiler.argument_extractor import extract_action_args
        from shtest_compiler.compiler.shell_generator import extract_action_groups, canonize_action
        
        command = action.command
        
        # Method 1: Try using extract_action_args (returns dict with named parameters)
        extracted_args = extract_action_args(command)
        if extracted_args and pname in extracted_args:
            return extracted_args[pname]
        
        # Method 2: Try using canonize_action + extract_action_groups
        canon = canonize_action(command)
        if canon:
            phrase_canonique, handler, pattern_entry = canon
            # Find matching pattern
            matched_pattern = None
            for alias in [pattern_entry["phrase"]] + pattern_entry.get("aliases", []):
                if not isinstance(alias, str):
                    continue
                if alias.lower() == command.lower().strip():
                    matched_pattern = alias
                    break
                if alias.startswith("^") and alias.endswith("$"):
                    try:
                        if re.match(alias, command.lower().strip(), re.IGNORECASE):
                            matched_pattern = alias
                            break
                    except re.error:
                        continue
            
            if matched_pattern:
                groups = extract_action_groups(command, matched_pattern)
                # Extract parameter names from the pattern
                param_names = re.findall(r'\{(\w+)\}', matched_pattern)
                # Map parameter names to groups
                for i, param_name in enumerate(param_names):
                    if param_name == pname and i < len(groups):
                        return groups[i]
        
        # Method 3: Try to extract from action's existing fields if it's an Action node
        if hasattr(action, 'arguments') and action.arguments:
            if pname in action.arguments:
                return action.arguments[pname]
        
        # Method 4: Try to extract from action's variables if available
        if hasattr(action, 'variables') and action.variables:
            if pname in action.variables:
                return action.variables[pname]
        
        return None

    def enforce_scope(self):
        for step in self.ast.steps:
            for validation in getattr(step, 'validations', []):
                if getattr(validation, 'scope', 'last_action') == 'last_action' and not step.actions:
                    raise ValueError(f"Local validation '{getattr(validation, 'phrase', str(validation))}' must follow an action in step '{getattr(step, 'name', str(step))}'")

    def bind(self) -> ShellFrameworkAST:
        self.bind_missing_validation_params()
        self.enforce_scope()
        # 1. Analyze all actions/validations to find duplicates and extract parameters
        occurrence_counter: Dict[str, int] = {}
        action_instances: Dict[str, List[Tuple[ShellTestStep, int, object]]] = {}
        for step in self.ast.steps:
            for idx, action in enumerate(step.actions):
                key, params = self._action_key_and_params(action)
                occurrence_counter[key] = occurrence_counter.get(key, 0) + 1
                action_instances.setdefault(key, []).append((step, idx, action))
        # 2. For those with count > 1, create helpers with parameters
        for key, count in occurrence_counter.items():
            if count > 1 and key not in self.action_map:
                self.helper_counter += 1
                helper_name = f"helper_{self.helper_counter}"
                param_names, body_lines = self._extract_params_and_body(key)
                param_map = {p: f"${i+1}" for i, p in enumerate(param_names)}
                substituted_body = [self._substitute_params(line, param_map) for line in body_lines]
                helper = ShellFunctionDef(name=helper_name, params=param_names, body_lines=substituted_body)
                self.action_map[key] = (helper, param_names)
                self.ast.helpers.append(helper)
        # 3. Replace repeated inlines with function calls, passing real arguments
        for key, instances in action_instances.items():
            if key in self.action_map:
                helper, param_names = self.action_map[key]
                for step, idx, action in instances:
                    args = self._extract_args_from_action(action, param_names)
                    step.actions[idx] = ShellFunctionCall(name=helper.name, args=args)
        # 4. Lift global validations attached as results to standalone synthetic actions
        # This step is now handled by ShellFrameworkLifter.
        # For each global validation, insert a synthetic action+validation
        # for gval in global_valids: # This line is no longer needed here
        #     synthetic_action = InlineShellCode(code_lines=[])  # No-op action
        #     # Attach the validation as a standalone validation after the action
        #     new_actions.append(gval)
        # step.actions = new_actions # This line is no longer needed here
        return self.ast

    def _action_key_and_params(self, action) -> Tuple[str, List[str]]:
        if isinstance(action, InlineShellCode):
            # Convert any ValidationCheck objects to shell code strings
            lines = []
            for item in action.code_lines:
                if isinstance(item, ValidationCheck):
                    lines.append(f"# {item.expected}")
                    lines.append(item.actual_cmd)
                else:
                    lines.append(item)
            key = "\n".join(lines)
            params = self._extract_param_placeholders(lines)
            return key, params
        elif isinstance(action, ShellFunctionCall):
            key = f"{action.name}|{'|'.join(action.args)}"
            return key, action.args
        elif isinstance(action, ValidationCheck):
            # Convert ValidationCheck to shell code string for keying and param extraction
            key = f"# {action.expected}\n{action.actual_cmd}"
            params = self._extract_param_placeholders([action.actual_cmd])
            return key, params
        else:
            return str(action), []

    def _extract_param_placeholders(self, code_lines: List[str]) -> List[str]:
        params = []
        seen = set()
        for line in code_lines:
            for match in re.findall(r'\{(\w+)\}', line):
                if match not in seen:
                    params.append(match)
                    seen.add(match)
        return params

    def _extract_params_and_body(self, key: str) -> Tuple[List[str], List[str]]:
        lines = key.split("\n")
        params = self._extract_param_placeholders(lines)
        return params, lines

    def _extract_args_from_action(self, action, param_names: List[str]) -> List[str]:
        args = []
        if isinstance(action, InlineShellCode):
            for pname in param_names:
                found = None
                for line in action.code_lines:
                    # Convert ValidationCheck to shell code string for argument extraction
                    if isinstance(line, ValidationCheck):
                        line = line.actual_cmd
                    m = re.search(rf'{pname}=([\w\./-]+)', line)
                    if m:
                        found = m.group(1)
                        break
                args.append(found or "")
        elif isinstance(action, ValidationCheck):
            for pname in param_names:
                found = None
                m = re.search(rf'{pname}=([\w\./-]+)', action.actual_cmd)
                if m:
                    found = m.group(1)
                args.append(found or "")
        elif isinstance(action, Action):
            for pname in param_names:
                val = self._extract_from_action_fields(action, pname)
                args.append(val or "")
        else:
            args = [""] * len(param_names)
        return args

    def _extract_from_action_fields(self, action: Action, pname: str) -> str:
        # Try to extract {pname} from command or result_expr using regex
        for field in [action.command, action.result_expr]:
            if not field:
                continue
            # Try {pname}=value
            m = re.search(rf'{pname}=([\w\./-]+)', field)
            if m:
                return m.group(1)
            # Try "{pname}" or '{pname}'
            m = re.search(rf'[{chr(34)}\']{pname}[{chr(34)}\']', field)
            if m:
                return pname
        return ""

    def _substitute_params(self, line: str, param_map: Dict[str, str]) -> str:
        for pname, shell_var in param_map.items():
            line = line.replace(f'{{{pname}}}', shell_var)
        return line 