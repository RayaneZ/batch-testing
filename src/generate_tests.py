
import os
from glob import glob
from compiler.shell_generator import generate_shell_script
from compiler.shell_generator import parse_test_file  # À déplacer si pas encore fait

def generate_tests(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    for txt_file in glob(os.path.join(input_dir, "*.shtest")):
        with open(txt_file, encoding="utf-8") as f:
            test_description = f.read()
        actions = parse_test_file(test_description)
        script = generate_shell_script(actions)
        out_name = os.path.splitext(os.path.basename(txt_file))[0] + ".sh"
        out_path = os.path.join(output_dir, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(script)
        print(f"✅ Generated {out_path}")
