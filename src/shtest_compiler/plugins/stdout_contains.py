"""
Plugin for stdout contains validation.
"""

class StdoutContainsValidation:
    def __init__(self, groups):
        self.text = groups[0] if groups else None
    def to_shell(self, **kwargs):
        return [f'echo "$stdout" | grep -q "{self.text}"']
def handle(groups, **kwargs):
    return StdoutContainsValidation(groups) 