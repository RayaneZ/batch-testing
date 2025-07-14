# Unit Tests

This directory contains unit tests for individual components of the batch testing framework.

## Purpose
Unit tests verify that individual functions, classes, and modules work correctly in isolation. They should be fast, reliable, and not depend on external systems.

## Test Files

### Core Tests
- `test_core.py` - Tests core functionality and utilities
- `test_core_visitor.py` - Tests AST visitor pattern implementation

### Parser Tests
- `test_parser.py` - Tests the main parser functionality
- `test_modular_parser.py` - Tests the modular parser system

### Lexer Tests
- `test_modular_lexer.py` - Tests the modular lexer system

### Compiler Tests
- `test_compiler.py` - Tests the main compiler functionality
- `test_visitors.py` - Tests compiler visitors

### System Tests
- `test_modular_system.py` - Tests the complete modular system integration

### Utility Tests
- `test_alias_utils.py` - Tests alias resolution utilities
- `test_verify_syntax.py` - Tests syntax verification
- `test_generate_tests.py` - Tests test generation utilities

## Running Unit Tests

```bash
# Run all unit tests
python -m pytest tests/unit/

# Run with verbose output
python -m pytest tests/unit/ -v

# Run specific test file
python -m pytest tests/unit/test_parser.py

# Run specific test function
python -m pytest tests/unit/test_parser.py::test_parse_simple_action

# Run with coverage
python -m pytest tests/unit/ --cov=shtest_compiler
```

## Writing Unit Tests

### Test Structure
```python
import pytest
from shtest_compiler.component import SomeClass

def test_some_function():
    """Test description"""
    # Arrange
    input_data = "test input"
    
    # Act
    result = SomeClass.some_function(input_data)
    
    # Assert
    assert result == "expected output"

def test_some_function_with_invalid_input():
    """Test error handling"""
    with pytest.raises(ValueError):
        SomeClass.some_function("invalid input")
```

### Best Practices
1. **One assertion per test**: Each test should verify one specific behavior
2. **Descriptive names**: Test names should clearly describe what they test
3. **Arrange-Act-Assert**: Structure tests with clear sections
4. **Mock external dependencies**: Don't depend on files, databases, or network
5. **Fast execution**: Unit tests should run quickly (< 1 second each)

### Test Categories
- **Happy path tests**: Test normal operation with valid inputs
- **Edge case tests**: Test boundary conditions and edge cases
- **Error handling tests**: Test how the code handles invalid inputs
- **Integration tests**: Test how components work together (keep minimal)

## Coverage
Unit tests should aim for high code coverage (> 80%) of the core functionality. Focus on:
- Business logic
- Data validation
- Error handling
- Edge cases

## Dependencies
Unit tests should have minimal dependencies:
- Use `pytest` for testing framework
- Use `unittest.mock` for mocking
- Avoid external file system access
- Avoid network calls
- Avoid database connections 