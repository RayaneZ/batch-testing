from shtest_compiler.ast.shell_framework_ast import ActionNode

class TouchTimestampAction(ActionNode):
    def __init__(self, timestamp, path):
        self.timestamp = timestamp
        self.path = path
    def to_shell(self):
        return f"touch -t '{self.timestamp}' '{self.path}'"

def handle(params):
    # Map the extracted variables to the expected parameter names
    # The pattern extracts 'file' and 'date', but we need 'timestamp' and 'path'
    timestamp = params.get('date') or params.get('timestamp')
    path = params.get('file') or params.get('path')
    
    if not timestamp or not path:
        # Fallback: try to extract from context if available
        context = params.get('context', {})
        variables = context.get('variables', {})
        timestamp = timestamp or variables.get('date') or variables.get('timestamp')
        path = path or variables.get('file') or variables.get('path')
    
    if not timestamp or not path:
        raise ValueError(f"Missing required parameters for touch_ts: timestamp={timestamp}, path={path}")
    
    return TouchTimestampAction(timestamp, path) 