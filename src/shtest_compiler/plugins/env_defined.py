class EnvDefinedValidation:
    def __init__(self, var_name=None):
        self.var_name = var_name

    def to_shell(self, varname="result", last_file_var=None):
        """Generate shell code for environment variable defined validation."""
        var_name = self.var_name or "SQL_CONN"
        return [
            f"{varname}=0",
            f'if [ -n "${var_name}" ]; then',
            f"    {varname}=1",
            f'    actual="variable d\'environnement définie"',
            f"else",
            f'    actual="variable d\'environnement non définie"',
            f"fi",
            f'expected="variable d\'environnement définie"',
        ]


def handle(groups, scope=None):
    var_name = groups[0] if groups else None
    return EnvDefinedValidation(var_name)
