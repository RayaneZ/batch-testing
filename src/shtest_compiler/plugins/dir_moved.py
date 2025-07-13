class DirMovedValidation:
    def __init__(self, source=None, destination=None):
        self.source = source
        self.destination = destination
    
    def to_shell(self, varname="result", last_file_var=None):
        """Generate shell code for directory moved validation."""
        return [
            f'{varname}=0',
            f'if [ $last_ret -eq 0 ]; then',
            f'    {varname}=1',
            f'    actual="le dossier est déplacé"',
            f'else',
            f'    actual="dossier non déplacé"',
            f'fi',
            f'expected="le dossier est déplacé"'
        ]

def handle(groups, scope=None):
    source = groups[0] if len(groups) > 0 else None
    destination = groups[1] if len(groups) > 1 else None
    return DirMovedValidation(source, destination) 