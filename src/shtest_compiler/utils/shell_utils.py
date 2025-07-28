import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller (external data)."""
    if getattr(sys, 'frozen', False):  # Running as compiled exe
        base_path = os.path.dirname(sys.executable)
        print(f"Running as compiled exe, base_path: {base_path}")
    else:
        base_path = os.path.dirname(os.path.dirname(__file__))
    
    full_path = os.path.join(base_path, relative_path)
    print(f"resource_path: {relative_path} -> {full_path}")
    
    # Check if file exists and log the result
    if os.path.exists(full_path):
        print(f"✓ File exists: {full_path}")
    else:
        print(f"✗ File not found: {full_path}")
        # List contents of the directory to help debug
        try:
            dir_path = os.path.dirname(full_path)
            if os.path.exists(dir_path):
                print(f"Contents of {dir_path}:")
                for item in os.listdir(dir_path):
                    print(f"  - {item}")
            else:
                print(f"Directory does not exist: {dir_path}")
        except Exception as e:
            print(f"Error listing directory: {e}")
    
    return full_path

def list_meipass():
    """Display the contents of the PyInstaller temporary directory (_MEIPASS)"""
    if not hasattr(sys, '_MEIPASS'):
        print("The program is not running in a PyInstaller executable (no _MEIPASS).")
        return

    root = sys._MEIPASS
    print(f"Recursive contents of _MEIPASS ({root}) :\n")

    for dirpath, dirnames, filenames in os.walk(root):
        rel_path = os.path.relpath(dirpath, root)
        indent = '  ' * rel_path.count(os.sep)
        print(f"{indent}{rel_path if rel_path != '.' else '.'}/")
        for fname in filenames:
            print(f"{indent}  - {fname}")

def shell_escape(value):
    """Escape a string for safe use in single-quoted shell strings."""
    if value is None:
        return ""
    return "'" + str(value).replace("'", "'\\''") + "'" 