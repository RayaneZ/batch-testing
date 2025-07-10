
class CompileContext:
    def __init__(self, counter=None, last_file_var=None, verbose=False):
        self.counter = counter or [0]
        self.last_file_var = last_file_var or [None]
        self.verbose = verbose
