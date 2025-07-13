from shtest_compiler.ast_nodes import CopyFileCommand

def handle(groups):
    src, dest = groups
    return CopyFileCommand(src=src, dest=dest) 