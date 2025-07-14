# Comprehensive Test Suite for shtest_compiler

This document describes the complete test suite for the shtest_compiler project, including unit tests, integration tests, E2E tests, and shellcheck validation.

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **WSL2** (on Windows) for shellcheck integration
3. **shellcheck** (automatically installed via scripts)

### Installation

```bash
# Install development dependencies
cd src
pip install -e ".[dev]"

# Install shellcheck (Linux)
sudo apt-get update && sudo apt-get install -y shellcheck

# Install shellcheck (Windows via WSL)
wsl sudo apt-get update && wsl sudo apt-get install -y shellcheck
```

### Running Tests

```bash
# Run all tests
python test_suite.py

# Run specific test types
python test_suite.py --no-shellcheck  # Skip shellcheck
python test_suite.py --unit-only      # Unit tests only
```

## 📁 Test Structure

```
src/
├── tests/
│   ├── unit/           # Unit tests (pytest)
│   ├── e2e/            # E2E tests (.shtest files)
│   ├── integration/    # Compiled shell scripts
│   └── legacy/         # Legacy tests
├── test_suite.py       # Main test runner
├── Makefile           # Unix/Linux commands
├── test_suite.ps1     # PowerShell commands
└── pytest.ini        # Pytest configuration
```

## 🧪 Test Types

### 1. Unit Tests (`tests/unit/`)

**Purpose**: Test individual components in isolation

**Files**: `test_*.py`

**Examples**:
- `test_parser.py` - Parser functionality
- `test_compiler.py` - Compiler logic
- `test_modular_lexer.py` - Lexer operations

**Run**:
```bash
# Using pytest directly
pytest tests/unit/ -v

# Using test suite
python test_suite.py --unit-only

# Using Makefile
make test-unit
```

### 2. E2E Tests (`tests/e2e/`)

**Purpose**: Test complete workflows using `.shtest` files

**Files**: `*.shtest`

**Examples**:
- `example.shtest` - Basic functionality
- `test_basic_checks.shtest` - Validation features
- `sql_comparison_example.shtest` - SQL operations

**Run**:
```bash
# Compile E2E tests to shell scripts
python -m shtest_compiler.run_all --input tests/e2e --output tests/integration

# Using test suite
python test_suite.py --e2e-only

# Using Makefile
make test-e2e
```

### 3. Integration Tests (`tests/integration/`)

**Purpose**: Test compiled shell scripts

**Files**: `*.sh` (generated from E2E tests)

**Run**:
```bash
# Run all integration tests
for test in tests/integration/*.sh; do
    bash "$test"
done

# Using test suite
python test_suite.py --integration-only

# Using Makefile
make test-integration
```

### 4. Shellcheck Validation

**Purpose**: Validate shell script quality and best practices

**Requirements**: shellcheck installed

**Run**:
```bash
# Check all compiled scripts
for test in tests/integration/*.sh; do
    shellcheck --shell=bash --severity=style "$test"
done

# Using test suite
python test_suite.py --shellcheck-only

# Using Makefile
make test-shellcheck
```

### 5. Code Quality Checks

**Purpose**: Ensure code quality and consistency

**Tools**:
- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking

**Run**:
```bash
# All quality checks
python test_suite.py --quality-only

# Individual checks
black --check shtest_compiler/ tests/
flake8 shtest_compiler/ tests/
mypy shtest_compiler/

# Using Makefile
make test-quality
```

## 🛠️ Test Runners

### 1. Python Test Suite (`test_suite.py`)

**Features**:
- Cross-platform support (Windows/WSL, Linux)
- Comprehensive reporting
- JSON test reports
- Configurable test selection

**Usage**:
```bash
# Run all tests
python test_suite.py

# Specific options
python test_suite.py --project-root /path/to/project
python test_suite.py --no-shellcheck
python test_suite.py --unit-only
python test_suite.py --e2e-only
python test_suite.py --integration-only
python test_suite.py --quality-only
python test_suite.py --shellcheck-only
```

### 2. Makefile (Unix/Linux)

**Features**:
- Simple command interface
- OS detection
- WSL integration

**Usage**:
```bash
# Show available commands
make help

# Run all tests
make test

# Specific test types
make test-unit
make test-e2e
make test-integration
make test-shellcheck
make test-quality

# Development setup
make dev-setup
make install-shellcheck
```

### 3. PowerShell Script (Windows)

**Features**:
- Windows-native interface
- WSL integration
- Colored output

**Usage**:
```powershell
# Run all tests
.\test_suite.ps1

# Specific options
.\test_suite.ps1 -UnitOnly
.\test_suite.ps1 -E2EOnly
.\test_suite.ps1 -IntegrationOnly
.\test_suite.ps1 -QualityOnly
.\test_suite.ps1 -ShellcheckOnly
.\test_suite.ps1 -NoShellcheck
.\test_suite.ps1 -Help
```

## 🔧 Configuration

### Pytest Configuration (`pytest.ini`)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
addopts = 
    --strict-markers
    --verbose
    --cov=shtest_compiler
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    shellcheck: Tests requiring shellcheck
```

### Coverage Configuration

Coverage reports are generated in multiple formats:
- **Terminal**: `--cov-report=term-missing`
- **HTML**: `htmlcov/` directory
- **XML**: `coverage.xml` file

### Shellcheck Configuration

Shellcheck is configured with:
- **Shell**: bash
- **Severity**: style (can be changed to error, warning, info)
- **Platform**: Automatic detection (WSL on Windows, native on Linux)

## 🚀 CI/CD Integration

### GitHub Actions

The test suite is integrated with GitHub Actions:

```yaml
# .github/workflows/test.yml
- Runs on Ubuntu and Windows
- Tests Python 3.8-3.11
- Includes shellcheck validation
- Generates coverage reports
- Uploads test artifacts
```

### Pre-commit Hooks

Pre-commit hooks ensure code quality:

```yaml
# .pre-commit-config.yaml
- Black formatting
- Flake8 linting
- MyPy type checking
- Shellcheck validation
- Pytest execution
```

## 📊 Test Reports

### JSON Reports

Test results are saved as JSON files in `test_reports/`:

```json
{
  "total_tests": 15,
  "passed": 12,
  "failed": 2,
  "errors": 1,
  "skipped": 0,
  "success_rate": 80.0,
  "total_duration": 45.23,
  "reports": [...]
}
```

### Coverage Reports

Coverage reports are generated in:
- `htmlcov/` - HTML coverage report
- `coverage.xml` - XML coverage data
- Terminal output - Summary with missing lines

## 🐛 Troubleshooting

### Common Issues

1. **WSL not available on Windows**
   ```bash
   # Install WSL2
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

4. **Test compilation fails**
   ```bash
   # Check E2E test syntax
   python -m shtest_compiler.verify_syntax tests/e2e/
   ```

### Debug Mode

Enable debug output:

```bash
# Python test suite
python test_suite.py --debug

# Individual components
python -m shtest_compiler.shtest compile_file test.shtest --debug
```

## 📈 Performance

### Test Execution Times

Typical execution times:
- **Unit tests**: 5-10 seconds
- **E2E compilation**: 2-5 seconds
- **Shellcheck**: 1-3 seconds per script
- **Integration tests**: 10-30 seconds
- **Quality checks**: 5-15 seconds

### Optimization

1. **Parallel execution**:
   ```bash
   pytest -n auto  # Parallel pytest
   ```

2. **Selective testing**:
   ```bash
   pytest -k "test_parser"  # Run specific tests
   ```

3. **Caching**:
   ```bash
   pytest --cache-clear  # Clear cache
   ```

## 🔄 Development Workflow

### Daily Development

```bash
# 1. Run quick tests
make quick-test

# 2. Format code
make format

# 3. Run quality checks
make lint
make type-check

# 4. Run full test suite
make test-all
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
# Run comprehensive test suite
python test_suite.py

# Generate coverage report
make coverage

# Check all quality metrics
make test-quality
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Shellcheck Documentation](https://www.shellcheck.net/)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [MyPy Documentation](https://mypy.readthedocs.io/) 