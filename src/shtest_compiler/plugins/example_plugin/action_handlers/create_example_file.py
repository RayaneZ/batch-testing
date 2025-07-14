import os
# Example Plugin Action Handler: Create Example File
# --------------------------------------------------
# This handler demonstrates how to implement a custom action handler for the batch testing framework.
# It creates a file at the specified path with the given content, using a shell command.
#
# Usage:
#   - 'path': the file path to create (default: 'example.txt')
#   - 'content': the content to write into the file (default: 'This is an example file.')
#
# The handler returns an ActionNode subclass with a to_shell() method, so it integrates with the shell generation pipeline.

from shtest_compiler.ast.shell_framework_ast import ActionNode

class CreateExampleFileAction(ActionNode):
    """
    ActionNode for creating a file with specified content using a shell command.
    This is a template for plugin developers: extend this pattern for your own actions!
    """
    def __init__(self, path, content="This is an example file."):
        self.path = path
        self.content = content

    def to_shell(self):
        # Generates a shell command to create the file with the given content.
        # Note: This will overwrite the file if it already exists.
        return f"echo '{self.content}' > '{self.path}'"


def handle(params):
    """
    Handler entry point for the action. Expects a 'params' dict with optional 'path' and 'content'.
    Returns an ActionNode for shell script generation.
    """
    path = params.get("path", "example.txt")
    content = params.get("content", "This is an example file.")
    return CreateExampleFileAction(path, content)
