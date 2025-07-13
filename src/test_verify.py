#!/usr/bin/env python3
"""
Simple syntax verification script
"""

import sys
from pathlib import Path
from shtest_compiler.parser.parser import Parser

def verify_file(file_path):
    """Verify syntax of a single .shtest file"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        
        parser = Parser()
        parser.parse(content, path=str(file_path), debug=False)
        print(f"    {file_path.name} syntax OK")
        return True
    except Exception as e:
        print(f"    {file_path.name} syntax error: {e}")
        return False

def main():
    print("Verifying E2E Test Syntax...")
    
    e2e_dir = Path("tests/e2e")
    if not e2e_dir.exists():
        print("E2E tests directory not found")
        return False
    
    shtest_files = list(e2e_dir.glob("*.shtest"))
    if not shtest_files:
        print("No E2E tests found")
        return False
    
    passed = 0
    failed = 0
    
    for shtest_file in shtest_files:
        print(f"  Verifying {shtest_file.name}...")
        if verify_file(shtest_file):
            passed += 1
        else:
            failed += 1
    
    print(f"Syntax Verification Summary: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 