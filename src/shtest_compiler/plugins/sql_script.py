from shtest_compiler.ast_nodes import SQLScriptCommand

def handle(groups):
    script, = groups
    return SQLScriptCommand(script=script) 