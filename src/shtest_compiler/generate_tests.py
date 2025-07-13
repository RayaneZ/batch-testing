
import sys
import os
from glob import glob
from .compiler.shell_generator import ShellGenerator
from .parser.parser import Parser
from .parser.core import ParseError


def generate_tests(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    parser = Parser()
    any_failed = False
    
    for txt_file in glob(os.path.join(input_dir, "*.shtest")):
        with open(txt_file, encoding="utf-8") as f:
            test_description = f.read()
        try:
            # Parse the shtest file
            shtest_file = parser.parse(test_description, path=txt_file)
            # Generate shell script
            generator = ShellGenerator()
            script = generator.visit_shtest_file(shtest_file)
            out_name = os.path.splitext(os.path.basename(txt_file))[0] + ".sh"
            out_path = os.path.join(output_dir, out_name)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(script)
            print(f"Generated {out_path}")
        except ParseError as e:
            print(f"[ERROR] Parse error in {txt_file}: {e}", file=sys.stderr)
            any_failed = True
        except Exception as e:
            print(f"[ERROR] Unexpected error in {txt_file}: {e}", file=sys.stderr)
            any_failed = True
    if any_failed:
        print("[FAIL] One or more files failed to compile.", file=sys.stderr)
        sys.exit(1)
