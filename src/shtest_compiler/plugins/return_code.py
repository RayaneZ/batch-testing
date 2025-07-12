class ReturnCodeValidation:
    def __init__(self, code):
        self.code = code
    def to_shell(self, var):
        return f'if [ $last_ret -eq {self.code} ]; then {var}=1; else {var}=0; fi'

def handle(groups, scope=None):
    code, = groups
    return ReturnCodeValidation(code) 