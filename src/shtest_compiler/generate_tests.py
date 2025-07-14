import os
import sys
from glob import glob

from .compile_file import compile_file


def generate_tests(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    any_failed = False
    debug = os.environ.get("SHTEST_DEBUG", "0") == "1"

    for txt_file in glob(os.path.join(input_dir, "*.shtest")):
        try:
            base = os.path.splitext(os.path.basename(txt_file))[0]
            out_name = base + ".sh"
            out_path = os.path.join(output_dir, out_name)
            debug_output_path = (
                os.path.join(output_dir, base + ".txt") if debug else None
            )
            compile_file(
                input_path=txt_file,
                output_path=out_path,
                debug=debug,
                debug_output_path=debug_output_path,
            )
            print(f"Generated {out_path}")
        except Exception as e:
            print(f"[ERROR] Failed to compile {txt_file}: {e}", file=sys.stderr)
            any_failed = True
    if any_failed:
        print("[FAIL] One or more files failed to compile.", file=sys.stderr)
        sys.exit(1)
