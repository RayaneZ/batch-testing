#!/usr/bin/env python3
"""
Test Runner for Batch Testing Framework

This script demonstrates the new test organization and provides easy ways to run
different types of tests.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_unit_tests(verbose=False):
    """Run all unit tests"""
    print("Running Unit Tests...")
    unit_test_dir = Path(__file__).parent.parent / "tests" / "unit"
    cmd = ["python", "-m", "pytest", str(unit_test_dir)]
    if verbose:
        cmd.append("-v")

    try:
        result = subprocess.run(cmd, capture_output=not verbose, text=True)
        if result.returncode == 0:
            print("Unit tests passed")
        else:
            print("Unit tests failed")
            if not verbose:
                print(result.stdout)
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running unit tests: {e}")
        return False


def compile_e2e_tests(verbose=False):
    """Compile E2E tests to integration tests"""
    print("Compiling E2E Tests...")
    cmd = [
        "python",
        "-m",
        "shtest_compiler.run_all",
        "--input",
        "tests/e2e",
        "--output",
        "tests/integration",
    ]
    if verbose:
        cmd.append("--verbose")

    try:
        result = subprocess.run(cmd, capture_output=not verbose, text=True)
        if result.returncode == 0:
            print("E2E tests compiled successfully")
        else:
            print("E2E compilation failed")
            if not verbose:
                print(result.stdout)
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error compiling E2E tests: {e}")
        return False


def run_integration_tests(verbose=False):
    """Run all integration tests"""
    print("Running Integration Tests...")

    integration_dir = Path("tests/integration")
    if not integration_dir.exists():
        print("Integration tests directory not found")
        return False

    shell_scripts = list(integration_dir.glob("*.sh"))
    if not shell_scripts:
        print("No integration tests found")
        return False

    passed = 0
    failed = 0

    for script in shell_scripts:
        print(f"  Running {script.name}...")
        try:
            result = subprocess.run(
                ["bash", str(script)], capture_output=not verbose, text=True, timeout=30
            )
            if result.returncode == 0:
                print(f"    {script.name} passed")
                passed += 1
            else:
                print(f"    {script.name} failed")
                if not verbose:
                    print(f"      {result.stderr}")
                failed += 1
        except subprocess.TimeoutExpired:
            print(f"    {script.name} timed out")
            failed += 1
        except Exception as e:
            print(f"    {script.name} error: {e}")
            failed += 1

    print(f"Integration Tests Summary: {passed} passed, {failed} failed")
    return failed == 0


def verify_e2e_syntax():
    """Verify syntax of all E2E tests"""
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
        try:
            # Use the new ConfigurableParser for verification
            from shtest_compiler.parser.configurable_parser import ConfigurableParser

            with open(shtest_file, encoding="utf-8") as f:
                content = f.read()

            parser = ConfigurableParser(debug=False)
            shtest_obj = parser.parse(content, path=str(shtest_file))

            # Verify that the ShtestFile object has the expected structure
            if hasattr(shtest_obj, "steps") and isinstance(shtest_obj.steps, list):
                print(f"    {shtest_file.name} syntax OK")
                passed += 1
            else:
                print(
                    f"    {shtest_file.name} syntax error: Invalid ShtestFile structure"
                )
                failed += 1

        except Exception as e:
            print(f"    {shtest_file.name} syntax error: {e}")
            failed += 1

    print(f"Syntax Verification Summary: {passed} passed, {failed} failed")
    return failed == 0


def main():
    parser = argparse.ArgumentParser(
        description="Test Runner for Batch Testing Framework"
    )
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--e2e", action="store_true", help="Compile E2E tests only")
    parser.add_argument(
        "--integration", action="store_true", help="Run integration tests only"
    )
    parser.add_argument(
        "--verify", action="store_true", help="Verify E2E test syntax only"
    )
    parser.add_argument("--all", action="store_true", help="Run all tests (default)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Default to running all tests if no specific type is specified
    if not any([args.unit, args.e2e, args.integration, args.verify]):
        args.all = True

    print("Batch Testing Framework - Test Runner")
    print("=" * 50)

    success = True

    if args.unit or args.all:
        success &= run_unit_tests(args.verbose)
        print()

    if args.verify or args.all:
        success &= verify_e2e_syntax()
        print()

    if args.e2e or args.all:
        success &= compile_e2e_tests(args.verbose)
        print()

    if args.integration or args.all:
        success &= run_integration_tests(args.verbose)
        print()

    print("=" * 50)
    if success:
        print("All tests completed successfully!")
        sys.exit(0)
    else:
        print("Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
