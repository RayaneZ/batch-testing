class CommandAST:
    pass


class MkdirCommand(CommandAST):
    def __init__(self, path):
        self.path = path


class TouchCommand(CommandAST):
    def __init__(self, path, timestamp=None):
        self.path = path
        self.timestamp = timestamp


class CopyFileCommand(CommandAST):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest


class CopyDirCommand(CommandAST):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest


class MoveFileCommand(CommandAST):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest


class MoveDirCommand(CommandAST):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest


class DeleteFileCommand(CommandAST):
    def __init__(self, path):
        self.path = path


class DeleteDirCommand(CommandAST):
    def __init__(self, path):
        self.path = path


class PurgeDirCommand(CommandAST):
    def __init__(self, path):
        self.path = path


class CatFileCommand(CommandAST):
    def __init__(self, path):
        self.path = path


class CompareFilesCommand(CommandAST):
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2


class ScriptCommand(CommandAST):
    def __init__(self, script):
        self.script = script


class SQLScriptCommand(CommandAST):
    def __init__(self, script):
        self.script = script


class ExportVarCommand(CommandAST):
    def __init__(self, var, value):
        self.var = var
        self.value = value
