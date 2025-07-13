class TouchTimestampAction:
    def __init__(self, groups):
        self.timestamp = groups[0] if len(groups) > 0 else None
        self.path = groups[1] if len(groups) > 1 else None
    def to_shell(self, **kwargs):
        return [f"touch -t '{self.timestamp}' '{self.path}'"]
def handle(groups, **kwargs):
    return TouchTimestampAction(groups) 