from shtest_compiler.ast_nodes import (
    MkdirCommand, TouchCommand, CopyFileCommand, CopyDirCommand, MoveFileCommand, MoveDirCommand,
    DeleteFileCommand, DeleteDirCommand, PurgeDirCommand, CatFileCommand, CompareFilesCommand,
    ScriptCommand, SQLScriptCommand, ExportVarCommand
)

def ast_to_shell(ast):
    if hasattr(ast, 'to_shell'):
        return ast.to_shell()
    raise ValueError(f"AST non supporté : {type(ast)}") 