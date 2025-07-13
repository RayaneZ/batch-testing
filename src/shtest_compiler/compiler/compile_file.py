from shtest_compiler.core.errors import ValidationParseError

def compile_file(input_path, output_path=None, debug=False, debug_output_path=None):
    try:
        # (wherever compile_atomic or validation compilation is called)
        pass
    except ValidationParseError as e:
        print(f"[ERROR] {e}")
        raise 