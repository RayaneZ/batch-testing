import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # Join from the src root, not from the utils directory
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), relative_path)

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