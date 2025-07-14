class StdoutContainsValidation:
    def __init__(self, substring, scope=None):
        self.substring = substring
        self.scope = scope  # Peut être 'last_action' ou 'global'

    def to_shell(self, var):
        # Exemple d'utilisation du scope :
        # if self.scope == 'last_action': ...
        return f'echo "$last_stdout" | grep -q "{self.substring}" && {var}=1 || {var}=0'


def handle(groups, scope=None):
    (substring,) = groups
    return StdoutContainsValidation(substring, scope=scope)
