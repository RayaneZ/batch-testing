from shtest_compiler.ast_nodes import (
    CatFileCommand,
    CompareFilesCommand,
    CopyDirCommand,
    CopyFileCommand,
    DeleteDirCommand,
    DeleteFileCommand,
    ExportVarCommand,
    MkdirCommand,
    MoveDirCommand,
    MoveFileCommand,
    PurgeDirCommand,
    ScriptCommand,
    SQLScriptCommand,
    TouchCommand,
)


def ast_to_shell(ast):
    if hasattr(ast, "to_shell"):
        return ast.to_shell()
    raise ValueError(f"AST non supporté : {type(ast)}")
