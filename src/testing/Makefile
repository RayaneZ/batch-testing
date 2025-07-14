# Makefile for shtest_compiler test suite
# Supports both Windows (with WSL) and Linux environments

.PHONY: help install install-dev test test-unit test-e2e test-integration test-shellcheck test-quality test-all clean format lint type-check coverage install-shellcheck

# Default target
help:
	@echo "Available commands:"
	@echo "  install          - Install production dependencies"
	@echo "  install-dev      - Install development dependencies"
	@echo "  install-shellcheck - Install shellcheck (Linux) or check WSL availability (Windows)"
	@echo "  test             - Run all tests"
	@echo "  test-unit        - Run unit tests only"
	@echo "  test-e2e         - Compile E2E tests to shell scripts"
	@echo "  test-integration - Run integration tests (compiled shell scripts)"
	@echo "  test-shellcheck  - Run shellcheck on compiled scripts"
	@echo "  test-quality     - Run code quality checks (black, flake8, mypy)"
	@echo "  test-all         - Run complete test suite with shellcheck"
	@echo "  format           - Format code with black"
	@echo "  lint             - Run flake8 linting"
	@echo "  type-check       - Run mypy type checking"
	@echo "  coverage         - Generate coverage report"
	@echo "  clean            - Clean generated files and caches"

# Detect OS
ifeq ($(OS),Windows_NT)
    PYTHON := python
    SHELLCHECK_CMD := wsl shellcheck
    IS_WINDOWS := 1
else
    PYTHON := python3
    SHELLCHECK_CMD := shellcheck
    IS_WINDOWS := 0
endif

# Install dependencies
install:
	cd .. && $(PYTHON) -m pip install -e .

install-dev:
	cd .. && $(PYTHON) -m pip install -e ".[dev]"

# Install shellcheck
install-shellcheck:
ifeq ($(IS_WINDOWS),1)
	@echo "Checking WSL availability for shellcheck..."
	@wsl --version > /dev/null 2>&1 || (echo "WSL not available. Please install WSL2." && exit 1)
	@echo "Installing shellcheck in WSL..."
	@wsl sudo apt-get update && wsl sudo apt-get install -y shellcheck
	@echo "Shellcheck installed in WSL"
else
	@echo "Installing shellcheck..."
	@sudo apt-get update && sudo apt-get install -y shellcheck
	@echo "Shellcheck installed"
endif

# Test commands
test: test-all

test-unit:
	@echo "Running unit tests..."
	cd .. && $(PYTHON) -m pytest testing/tests/unit/ -v --cov=shtest_compiler --cov-report=term-missing

test-e2e:
	@echo "Compiling E2E tests..."
	cd .. && $(PYTHON) -m shtest_compiler.run_all --input testing/tests/e2e --output testing/tests/integration

test-integration:
	@echo "Running integration tests..."
	@for test in tests/integration/*.sh; do \
		if [ -f "$$test" ]; then \
			echo "Running $$test..."; \
			bash "$$test" || exit 1; \
		fi; \
	done

test-shellcheck:
	@echo "Running shellcheck on compiled scripts..."
ifeq ($(IS_WINDOWS),1)
	@for test in tests/integration/*.sh; do \
		if [ -f "$$test" ]; then \
			echo "Checking $$test..."; \
			wsl shellcheck --shell=bash --severity=style "$$test" || exit 1; \
		fi; \
	done
else
	@for test in tests/integration/*.sh; do \
		if [ -f "$$test" ]; then \
			echo "Checking $$test..."; \
			shellcheck --shell=bash --severity=style "$$test" || exit 1; \
		fi; \
	done
endif

test-quality:
	@echo "No code quality checks (flake8 removed)"

test-all: test-unit test-e2e test-shellcheck test-integration test-quality
	@echo "All tests completed!"

# Code quality commands
format:
	@echo "Formatting code with black is disabled. (black removed)"

lint:
	@echo "Linting is disabled. (flake8 removed)"

type-check:
	@echo "Type checking is disabled. (mypy removed)"

coverage:
	@echo "Generating coverage report..."
	cd .. && $(PYTHON) -m pytest testing/tests/unit/ --cov=shtest_compiler --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name "htmlcov" -exec rm -rf {} +
	@find . -type f -name "coverage.xml" -delete
	@find . -type f -name ".coverage" -delete
	@echo "Cleanup completed!"

# Development workflow
dev-setup: install-dev install-shellcheck
	@echo "Development environment setup completed!"

# Quick test (unit tests only)
quick-test: test-unit

# Full test suite with comprehensive reporting
full-test:
	@echo "Running comprehensive test suite..."
	cd .. && $(PYTHON) testing/test_suite.py --project-root .

# Test with specific shellcheck severity
test-shellcheck-strict:
	@echo "Running shellcheck with strict settings..."
ifeq ($(IS_WINDOWS),1)
	@for test in tests/integration/*.sh; do \
		if [ -f "$$test" ]; then \
			echo "Checking $$test..."; \
			wsl shellcheck --shell=bash --severity=error "$$test" || exit 1; \
		fi; \
	done
else
	@for test in tests/integration/*.sh; do \
		if [ -f "$$test" ]; then \
			echo "Checking $$test..."; \
			shellcheck --shell=bash --severity=error "$$test" || exit 1; \
		fi; \
	done
endif 