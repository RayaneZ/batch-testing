# Negative E2E Tests (KO)

This directory contains E2E tests that are designed to **fail** and test error handling capabilities of the shtest compiler.

## Test Categories

### Syntax Errors
- `invalid_syntax_1.shtest` - Missing step keyword
- `invalid_syntax_2.shtest` - Malformed action syntax
- `invalid_syntax_3.shtest` - Malformed validation syntax
- `invalid_nested_structure.shtest` - Invalid nesting of steps/actions

### File Operations
- `invalid_file_operations.shtest` - Invalid file paths and operations
- `empty_file.shtest` - File with only comments
- `completely_empty.shtest` - Completely empty file

### SQL Operations
- `invalid_sql_1.shtest` - Invalid SQL syntax and queries

### Variable Operations
- `invalid_variable_operations.shtest` - Invalid variable names and assignments

### Validation Issues
- `invalid_validation_combinations.shtest` - Conflicting and invalid validations

### Plugin Issues
- `invalid_plugin_usage.shtest` - Nonexistent plugins and wrong parameters

### Encoding Issues
- `invalid_encoding.shtest` - Invalid characters and encoding problems

### Format Issues
- `invalid_yaml_syntax.shtest` - YAML-like syntax that should be rejected

## Expected Behavior

These tests should:
1. **Fail during compilation** with appropriate error messages
2. **Not generate shell scripts** or generate scripts that fail
3. **Provide clear error diagnostics** about what went wrong
4. **Handle errors gracefully** without crashing the compiler

## Running Tests

```bash
# Run all negative tests
python -m shtest_compiler.run_all tests/e2e/ko/

# Run specific test
python -m shtest_compiler.run_all tests/e2e/ko/invalid_syntax_1.shtest
```

## Success Criteria

A negative test is successful if:
- The compiler detects the error and reports it clearly
- No shell script is generated (or generated script fails appropriately)
- The error message is helpful and points to the specific issue
- The compiler continues processing other files without crashing 