from shtest_compiler.ast_nodes import MkdirCommand
 
def handle(groups):
    path, = groups
    return MkdirCommand(path=path) 