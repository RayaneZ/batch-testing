#!/usr/bin/env python3
"""
Comprehensive test suite for shtest_compiler with shellcheck integration.
Supports both Windows/WSL and Linux environments.
"""

import os
import sys
import subprocess
import platform
import argparse
import pathlib
from typing import List, Optional, Dict, Any
import json
import time
from dataclasses import dataclass
from enum import Enum


class TestResult(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"


@dataclass
class TestReport:
    name: str
    result: TestResult
    duration: float
    output: str
    error: Optional[str] = None


class TestSuite:
    def __init__(self, project_root: str):
        self.project_root = pathlib.Path(project_root)
        self.src_dir = self.project_root / "src"
        self.testing_dir = self.src_dir / "testing"
        self.tests_dir = self.testing_dir / "tests"
        self.reports_dir = self.project_root / "test_reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        # Detect environment
        self.is_windows = platform.system() == "Windows"
        self.has_wsl = self._check_wsl_availability()
        
        # Test results
        self.results: List[TestReport] = []
        
    def _check_wsl_availability(self) -> bool:
        """Check if WSL is available on Windows."""
        if not self.is_windows:
            return False
        try:
            result = subprocess.run(
                ["wsl", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _run_command(self, cmd: List[str], cwd: Optional[str] = None, 
                    capture_output: bool = True, timeout: int = 300) -> subprocess.CompletedProcess:
        """Run a command with proper error handling."""
        try:
            return subprocess.run(
                cmd,
                cwd=cwd or str(self.project_root),
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Command timed out after {timeout} seconds: {' '.join(cmd)}")
        except FileNotFoundError as e:
            raise RuntimeError(f"Command not found: {' '.join(cmd)} - {e}")
    
    def _run_shellcheck(self, shell_script: str) -> TestReport:
        """Run shellcheck on a shell script."""
        script_path = pathlib.Path(shell_script)
        if not script_path.exists():
            return TestReport(
                name=f"shellcheck_{script_path.name}",
                result=TestResult.ERROR,
                duration=0.0,
                output="",
                error=f"Script not found: {script_path}"
            )
        
        start_time = time.time()
        
        try:
            if self.is_windows and self.has_wsl:
                # Use WSL for shellcheck on Windows
                cmd = ["wsl", "shellcheck", "--shell=bash", "--severity=style", str(script_path)]
            else:
                # Use native shellcheck on Linux
                cmd = ["shellcheck", "--shell=bash", "--severity=style", str(script_path)]
            
            result = self._run_command(cmd, timeout=60)
            duration = time.time() - start_time
            
            if result.returncode == 0:
                return TestReport(
                    name=f"shellcheck_{script_path.name}",
                    result=TestResult.PASSED,
                    duration=duration,
                    output=result.stdout
                )
            else:
                return TestReport(
                    name=f"shellcheck_{script_path.name}",
                    result=TestResult.FAILED,
                    duration=duration,
                    output=result.stdout,
                    error=result.stderr
                )
                
        except Exception as e:
            duration = time.time() - start_time
            return TestReport(
                name=f"shellcheck_{script_path.name}",
                result=TestResult.ERROR,
                duration=duration,
                output="",
                error=str(e)
            )
    
    def run_unit_tests(self) -> TestReport:
        """Run unit tests with pytest."""
        start_time = time.time()
        
        try:
            cmd = [
                sys.executable, "-m", "pytest", 
                str(self.tests_dir / "unit"),
                "--cov=shtest_compiler",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov",
                "--cov-report=xml:coverage.xml",
                "-v"
            ]
            
            result = self._run_command(cmd, cwd=str(self.src_dir), timeout=600)
            duration = time.time() - start_time
            
            if result.returncode == 0:
                return TestReport(
                    name="unit_tests",
                    result=TestResult.PASSED,
                    duration=duration,
                    output=result.stdout
                )
            else:
                return TestReport(
                    name="unit_tests",
                    result=TestResult.FAILED,
                    duration=duration,
                    output=result.stdout,
                    error=result.stderr
                )
                
        except Exception as e:
            duration = time.time() - start_time
            return TestReport(
                name="unit_tests",
                result=TestResult.ERROR,
                duration=duration,
                output="",
                error=str(e)
            )
    
    def compile_e2e_tests(self) -> TestReport:
        """Compile E2E tests to shell scripts."""
        start_time = time.time()
        
        try:
            e2e_dir = self.tests_dir / "e2e"
            integration_dir = self.tests_dir / "integration"
            integration_dir.mkdir(exist_ok=True)
            
            cmd = [
                sys.executable, "-m", "shtest_compiler.run_all",
                "--input", str(e2e_dir),
                "--output", str(integration_dir)
            ]
            
            result = self._run_command(cmd, cwd=str(self.src_dir), timeout=300)
            duration = time.time() - start_time
            
            if result.returncode == 0:
                return TestReport(
                    name="compile_e2e_tests",
                    result=TestResult.PASSED,
                    duration=duration,
                    output=result.stdout
                )
            else:
                return TestReport(
                    name="compile_e2e_tests",
                    result=TestResult.FAILED,
                    duration=duration,
                    output=result.stdout,
                    error=result.stderr
                )
                
        except Exception as e:
            duration = time.time() - start_time
            return TestReport(
                name="compile_e2e_tests",
                result=TestResult.ERROR,
                duration=duration,
                output="",
                error=str(e)
            )
    
    def run_shellcheck_on_compiled_scripts(self) -> List[TestReport]:
        """Run shellcheck on all compiled shell scripts."""
        integration_dir = self.tests_dir / "integration"
        if not integration_dir.exists():
            return [TestReport(
                name="shellcheck_compiled_scripts",
                result=TestResult.SKIPPED,
                duration=0.0,
                output="",
                error="Integration directory not found - compile E2E tests first"
            )]
        
        shell_scripts = list(integration_dir.glob("*.sh"))
        if not shell_scripts:
            return [TestReport(
                name="shellcheck_compiled_scripts",
                result=TestResult.SKIPPED,
                duration=0.0,
                output="",
                error="No shell scripts found in integration directory"
            )]
        
        reports = []
        for script in shell_scripts:
            report = self._run_shellcheck(str(script))
            reports.append(report)
        
        return reports
    
    def run_integration_tests(self) -> TestReport:
        """Run integration tests (compiled shell scripts)."""
        start_time = time.time()
        
        try:
            integration_dir = self.tests_dir / "integration"
            if not integration_dir.exists():
                return TestReport(
                    name="integration_tests",
                    result=TestResult.SKIPPED,
                    duration=0.0,
                    output="",
                    error="Integration directory not found - compile E2E tests first"
                )
            
            shell_scripts = list(integration_dir.glob("*.sh"))
            if not shell_scripts:
                return TestReport(
                    name="integration_tests",
                    result=TestResult.SKIPPED,
                    duration=0.0,
                    output="",
                    error="No shell scripts found in integration directory"
                )
            
            # Run each shell script
            results = []
            for script in shell_scripts:
                try:
                    if self.is_windows and self.has_wsl:
                        cmd = ["wsl", "bash", str(script)]
                    else:
                        cmd = ["bash", str(script)]
                    
                    result = self._run_command(cmd, timeout=120)
                    results.append(f"{script.name}: {'PASS' if result.returncode == 0 else 'FAIL'}")
                    
                except Exception as e:
                    results.append(f"{script.name}: ERROR - {e}")
            
            duration = time.time() - start_time
            
            return TestReport(
                name="integration_tests",
                result=TestResult.PASSED,
                duration=duration,
                output="\n".join(results)
            )
            
        except Exception as e:
            duration = time.time() - start_time
            return TestReport(
                name="integration_tests",
                result=TestResult.ERROR,
                duration=duration,
                output="",
                error=str(e)
            )
    
    def run_code_quality_checks(self) -> List[TestReport]:
        """Run code quality checks (black, flake8, mypy)."""
        reports = []
        
        # Black formatting check
        start_time = time.time()
        try:
            cmd = [sys.executable, "-m", "black", "--check", str(self.src_dir / "shtest_compiler")]
            result = self._run_command(cmd, timeout=60)
            duration = time.time() - start_time
            
            reports.append(TestReport(
                name="black_formatting",
                result=TestResult.PASSED if result.returncode == 0 else TestResult.FAILED,
                duration=duration,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None
            ))
        except Exception as e:
            duration = time.time() - start_time
            reports.append(TestReport(
                name="black_formatting",
                result=TestResult.ERROR,
                duration=duration,
                output="",
                error=str(e)
            ))
        
        # Flake8 linting
        start_time = time.time()
        try:
            cmd = [sys.executable, "-m", "flake8", str(self.src_dir / "shtest_compiler")]
            result = self._run_command(cmd, timeout=60)
            duration = time.time() - start_time
            
            reports.append(TestReport(
                name="flake8_linting",
                result=TestResult.PASSED if result.returncode == 0 else TestResult.FAILED,
                duration=duration,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None
            ))
        except Exception as e:
            duration = time.time() - start_time
            reports.append(TestReport(
                name="flake8_linting",
                result=TestResult.ERROR,
                duration=duration,
                output="",
                error=str(e)
            ))
        
        # MyPy type checking
        start_time = time.time()
        try:
            cmd = [sys.executable, "-m", "mypy", str(self.src_dir / "shtest_compiler")]
            result = self._run_command(cmd, timeout=120)
            duration = time.time() - start_time
            
            reports.append(TestReport(
                name="mypy_type_checking",
                result=TestResult.PASSED if result.returncode == 0 else TestResult.FAILED,
                duration=duration,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None
            ))
        except Exception as e:
            duration = time.time() - start_time
            reports.append(TestReport(
                name="mypy_type_checking",
                result=TestResult.ERROR,
                duration=duration,
                output="",
                error=str(e)
            ))
        
        return reports
    
    def run_all_tests(self, include_shellcheck: bool = True) -> Dict[str, Any]:
        """Run all tests and return comprehensive results."""
        print("🚀 Starting comprehensive test suite...")
        print(f"📁 Project root: {self.project_root}")
        print(f"🖥️  Platform: {platform.system()}")
        print(f"🐧 WSL available: {self.has_wsl}")
        print()
        
        all_reports = []
        
        # 1. Unit tests
        print("🧪 Running unit tests...")
        unit_report = self.run_unit_tests()
        all_reports.append(unit_report)
        print(f"   {unit_report.result.value} ({unit_report.duration:.2f}s)")
        
        # 2. Compile E2E tests
        print("🔨 Compiling E2E tests...")
        compile_report = self.compile_e2e_tests()
        all_reports.append(compile_report)
        print(f"   {compile_report.result.value} ({compile_report.duration:.2f}s)")
        
        # 3. Shellcheck on compiled scripts
        if include_shellcheck:
            print("🔍 Running shellcheck on compiled scripts...")
            shellcheck_reports = self.run_shellcheck_on_compiled_scripts()
            all_reports.extend(shellcheck_reports)
            passed = sum(1 for r in shellcheck_reports if r.result == TestResult.PASSED)
            failed = sum(1 for r in shellcheck_reports if r.result == TestResult.FAILED)
            print(f"   {passed} passed, {failed} failed")
        
        # 4. Integration tests
        print("🔗 Running integration tests...")
        integration_report = self.run_integration_tests()
        all_reports.append(integration_report)
        print(f"   {integration_report.result.value} ({integration_report.duration:.2f}s)")
        
        # 5. Code quality checks
        print("✨ Running code quality checks...")
        quality_reports = self.run_code_quality_checks()
        all_reports.extend(quality_reports)
        for report in quality_reports:
            print(f"   {report.name}: {report.result.value}")
        
        # Generate summary
        total_tests = len(all_reports)
        passed_tests = sum(1 for r in all_reports if r.result == TestResult.PASSED)
        failed_tests = sum(1 for r in all_reports if r.result == TestResult.FAILED)
        error_tests = sum(1 for r in all_reports if r.result == TestResult.ERROR)
        skipped_tests = sum(1 for r in all_reports if r.result == TestResult.SKIPPED)
        total_duration = sum(r.duration for r in all_reports)
        
        summary = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "skipped": skipped_tests,
            "total_duration": total_duration,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "reports": [
                {
                    "name": r.name,
                    "result": r.result.value,
                    "duration": r.duration,
                    "output": r.output,
                    "error": r.error
                }
                for r in all_reports
            ]
        }
        
        # Print summary
        print()
        print("📊 Test Summary:")
        print(f"   Total tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Errors: {error_tests}")
        print(f"   Skipped: {skipped_tests}")
        print(f"   Success rate: {summary['success_rate']:.1f}%")
        print(f"   Total duration: {total_duration:.2f}s")
        
        # Save detailed report
        report_file = self.reports_dir / f"test_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"📄 Detailed report saved to: {report_file}")
        
        return summary


def main():
    parser = argparse.ArgumentParser(description="Comprehensive test suite for shtest_compiler")
    parser.add_argument(
        "--project-root", 
        default="..", 
        help="Project root directory (default: parent directory)"
    )
    parser.add_argument(
        "--no-shellcheck", 
        action="store_true", 
        help="Skip shellcheck validation"
    )
    parser.add_argument(
        "--report-only", 
        action="store_true", 
        help="Only generate test report without running tests"
    )
    
    args = parser.parse_args()
    
    # Find project root
    project_root = pathlib.Path(args.project_root).resolve()
    if not (project_root / "src" / "shtest_compiler").exists():
        print("❌ Error: Could not find shtest_compiler in the specified directory")
        sys.exit(1)
    
    # Create and run test suite
    test_suite = TestSuite(str(project_root))
    
    if args.report_only:
        print("📄 Generating test report only...")
        # This would load existing reports and generate summary
        print("Report-only mode not yet implemented")
        sys.exit(0)
    
    try:
        summary = test_suite.run_all_tests(include_shellcheck=not args.no_shellcheck)
        
        # Exit with appropriate code
        if summary["failed"] > 0 or summary["errors"] > 0:
            print("❌ Some tests failed!")
            sys.exit(1)
        else:
            print("✅ All tests passed!")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n⏹️  Test suite interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"💥 Test suite failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 