# Testing Infrastructure for shtest_compiler

This directory contains all testing infrastructure for the shtest_compiler project, organized in a clean and modular structure.

## 📁 Directory Structure

```
testing/
├── __init__.py                 # Package initialization
├── test_suite.py              # Main test runner (Python)
├── test_suite.ps1             # PowerShell test runner (Windows)
├── Makefile                   # Unix/Linux test commands
├── pytest.ini                # Pytest configuration
├── .pre-commit-config.yaml   # Pre-commit hooks
├── .github/                   # GitHub Actions CI/CD
│   └── workflows/
│       └── test.yml
├── tests/                     # All test files
│   ├── unit/                  # Unit tests
│   ├── e2e/                   # E2E tests (.shtest files)
│   ├── integration/           # Compiled shell scripts
│   └── legacy/                # Legacy tests
├── TEST_SUITE_README.md       # Comprehensive documentation
└── TEST_SUITE_SUMMARY.md      # Quick start guide
```

## 🚀 Quick Start

### From the src directory:
```bash
# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py --unit-only
python run_tests.py --no-shellcheck
```

### From the testing directory:
```bash
# Run all tests
python test_suite.py

# Run specific test types
python test_suite.py --unit-only
python test_suite.py --no-shellcheck
```

### Using Makefile (Unix/Linux):
```bash
cd testing
make test-all
make test-unit
make test-e2e
```

### Using PowerShell (Windows):
```powershell
cd testing
.\test_suite.ps1
.\test_suite.ps1 -UnitOnly
```

## 🧪 Test Types

### 1. Unit Tests (`tests/unit/`)
- **Purpose**: Test individual components in isolation
- **Files**: `test_*.py`
- **Run**: `python -m pytest testing/tests/unit/`

### 2. E2E Tests (`tests/e2e/`)
- **Purpose**: Test complete workflows using `.shtest` files
- **Files**: `*.shtest`
- **Run**: Compile to shell scripts first, then execute

### 3. Integration Tests (`tests/integration/`)
- **Purpose**: Test compiled shell scripts
- **Files**: `*.sh` (generated from E2E tests)
- **Run**: Execute shell scripts directly

### 4. Shellcheck Validation
- **Purpose**: Validate shell script quality
- **Platform**: Windows (WSL) or Linux
- **Run**: Automatic during test suite execution

### 5. Code Quality Checks
- **Tools**: Black, Flake8, MyPy
- **Purpose**: Ensure code quality and consistency
- **Run**: Automatic during test suite execution

## 🛠️ Test Runners

### Python Test Suite (`test_suite.py`)
- Cross-platform support
- Comprehensive reporting
- JSON test reports
- Configurable test selection

### PowerShell Script (`test_suite.ps1`)
- Windows-native interface
- WSL integration
- Colored output
- Easy parameter handling

### Makefile
- Unix/Linux commands
- OS detection
- WSL integration
- Simple command interface

## 🔧 Configuration

### Pytest Configuration (`pytest.ini`)
- Test discovery paths
- Coverage settings
- Markers definition
- Warning filters

### Coverage Configuration
- Source paths: `shtest_compiler`
- Exclude patterns: `testing/*`, `test_*`
- Minimum coverage: 80%
- Multiple report formats

### Shellcheck Configuration
- Shell: bash
- Severity: style (configurable)
- Platform: Automatic detection

## 🚀 CI/CD Integration

### GitHub Actions (`.github/workflows/test.yml`)
- Multi-platform testing (Ubuntu, Windows)
- Python version matrix (3.8-3.11)
- Shellcheck integration
- Coverage reporting
- Artifact upload

### Pre-commit Hooks (`.pre-commit-config.yaml`)
- Code formatting (Black)
- Linting (Flake8)
- Type checking (MyPy)
- Shellcheck validation
- Pytest execution

## 📊 Reporting

### Test Reports
- **JSON**: Detailed results in `test_reports/`
- **Timing**: Execution duration tracking
- **Success Rate**: Percentage of passed tests
- **Coverage**: HTML and XML reports

### Coverage Reports
- **HTML**: `htmlcov/` directory
- **XML**: `coverage.xml` file
- **Terminal**: Missing lines display

## 🐛 Troubleshooting

### Common Issues

1. **WSL not available on Windows**
   ```bash
   wsl --install
   ```

2. **shellcheck not found**
   ```bash
   # Linux
   sudo apt-get install shellcheck
   
   # Windows (via WSL)
   wsl sudo apt-get install shellcheck
   ```

3. **Python dependencies missing**
   ```bash
   pip install -e ".[dev]"
   ```

### Debug Mode
```bash
# Enable debug output
python test_suite.py --debug

# Check individual components
python -m shtest_compiler.shtest compile_file test.shtest --debug
```

## 🔄 Development Workflow

### Daily Development
```bash
# Quick tests
python run_tests.py --unit-only

# Format code
cd testing && make format

# Quality checks
cd testing && make test-quality

# Full test suite
python run_tests.py
```

### Before Committing
```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit checks
pre-commit run --all-files
```

### Before Releasing
```bash
# Comprehensive test suite
python run_tests.py

# Generate coverage report
cd testing && make coverage

# Check all quality metrics
cd testing && make test-quality
```

## 📚 Additional Resources

- [TEST_SUITE_README.md](TEST_SUITE_README.md) - Comprehensive documentation
- [TEST_SUITE_SUMMARY.md](TEST_SUITE_SUMMARY.md) - Quick start guide
- [Pytest Documentation](https://docs.pytest.org/)
- [Shellcheck Documentation](https://www.shellcheck.net/)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [MyPy Documentation](https://mypy.readthedocs.io/)

## 🎯 Benefits of This Structure

- **Clean Organization**: All testing code in one place
- **Modular Design**: Easy to maintain and extend
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Multiple Interfaces**: Python, Make, PowerShell
- **CI/CD Ready**: GitHub Actions integration
- **Quality Assurance**: Comprehensive checks
- **Well Documented**: Clear instructions and examples

The testing infrastructure is now organized in a clean, modular structure that's easy to use and maintain! 