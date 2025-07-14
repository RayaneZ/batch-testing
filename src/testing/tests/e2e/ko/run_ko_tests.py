#!/usr/bin/env python3
"""
Negative E2E Test Runner

This script runs all negative tests in the ko directory and verifies that they fail appropriately.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_negative_test(test_file):
    """Run a single negative test and verify it fails appropriately."""
    print(f"Testing: {test_file}")

    try:
        # Try to compile the test file
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "shtest_compiler.run_all",
                "--input",
                str(test_file),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # For negative tests, we expect compilation to fail
        if result.returncode == 0:
            print(
                f"  ❌ FAIL: {test_file} compiled successfully but should have failed"
            )
            return False
        else:
            print(f"  ✅ PASS: {test_file} failed as expected")
            if result.stderr:
                print(f"    Error: {result.stderr.strip()}")
            return True

    except subprocess.TimeoutExpired:
        print(f"  ⏰ TIMEOUT: {test_file} took too long")
        return False
    except Exception as e:
        print(f"  💥 ERROR: {test_file} - {e}")
        return False


def main():
    """Run all negative tests in the ko directory."""
    ko_dir = Path(__file__).parent
    test_files = list(ko_dir.glob("*.shtest"))

    if not test_files:
        print("No .shtest files found in ko directory")
        return

    print(f"Running {len(test_files)} negative tests...")
    print("=" * 50)

    passed = 0
    failed = 0

    for test_file in sorted(test_files):
        if run_negative_test(test_file):
            passed += 1
        else:
            failed += 1
        print()

    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")

    if failed > 0:
        print("❌ Some negative tests did not fail as expected")
        sys.exit(1)
    else:
        print("✅ All negative tests failed as expected")


if __name__ == "__main__":
    main()
