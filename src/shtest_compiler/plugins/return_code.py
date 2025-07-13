class ReturnCodeValidation:
    def __init__(self, groups):
        self.code = groups[0] if groups else "0"
    def to_shell(self, **kwargs):
        return [f"[ $last_ret -eq {self.code} ]"]
def handle(groups, **kwargs):
    return ReturnCodeValidation(groups) 