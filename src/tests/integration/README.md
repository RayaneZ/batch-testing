# Integration Tests

This directory contains compiled shell scripts that are generated from E2E tests. These scripts test the complete integration of the batch testing framework.

## Purpose
Integration tests verify that the compiled shell scripts work correctly in real environments. They test the complete pipeline from `.shtest` files to executable shell scripts.

## Test Files

### Basic Functionality Tests
- `example.sh` - Compiled basic example test
- `test_basic_checks.sh` - Compiled basic validation tests
- `test_file_contains.sh` - Compiled file content validation tests

### SQL Feature Tests
- `sql_script_test.sh` - Compiled SQL script execution tests

### Validation Tests
- `test_all_validations.sh` - Compiled comprehensive validation tests
- `test_stdout_stderr.sh` - Compiled output stream validation tests

### Legacy Tests
- `alias_*.sh` - Legacy alias tests
- `test_case_*.sh` - Legacy test case files

## Running Integration Tests

### Run All Integration Tests
```bash
# Run all integration tests
for test in tests/integration/*.sh; do
    echo "Running $test..."
    bash "$test"
done

# Run with error handling
for test in tests/integration/*.sh; do
    echo "Running $test..."
    if bash "$test"; then
        echo "✓ $test passed"
    else
        echo "✗ $test failed"
    fi
done
```

### Run Specific Integration Tests
```bash
# Run specific test
bash tests/integration/example.sh

# Run with verbose output
bash -x tests/integration/example.sh

# Run with error handling
bash tests/integration/example.sh || echo "Test failed"
```

### Run Tests by Category
```bash
# Run only basic functionality tests
for test in tests/integration/test_basic_*.sh; do
    bash "$test"
done

# Run only SQL tests
for test in tests/integration/sql_*.sh; do
    bash "$test"
done

# Run only validation tests
for test in tests/integration/test_*_validations.sh; do
    bash "$test"
done
```

## Test Execution

### Environment Requirements
Integration tests may require:
- Bash shell environment
- File system access
- Database connections (for SQL tests)
- System commands and utilities
- Proper environment variables

### Test Output
Integration tests typically output:
- Success/failure messages
- Expected vs actual results
- Debug information (when verbose)
- Error messages (when tests fail)

### Example Test Output
```bash
$ bash tests/integration/example.sh
✓ Test step 1 passed
✓ Test step 2 passed
✓ Test step 3 passed
All tests completed successfully
```

## Debugging Integration Tests

### Verbose Execution
```bash
# Run with shell debugging
bash -x tests/integration/example.sh

# Run with both shell and test debugging
bash -x tests/integration/example.sh --verbose
```

### Manual Inspection
```bash
# View the generated script
cat tests/integration/example.sh

# Check script syntax
bash -n tests/integration/example.sh

# Run specific parts of the script
bash -c "source tests/integration/example.sh; echo 'Script loaded'"
```

### Common Issues
1. **Permission errors**: Ensure scripts are executable
2. **Path issues**: Check that required commands are in PATH
3. **Environment variables**: Verify required environment variables are set
4. **File system access**: Ensure proper read/write permissions
5. **Database connectivity**: Check database connection settings

## Test Maintenance

### Regenerating Tests
Integration tests are automatically generated from E2E tests:
```bash
# Regenerate all integration tests
python -m shtest_compiler.run_all --input tests/e2e --output tests/integration

# Regenerate specific test
python -m shtest_compiler.shtest compile_file tests/e2e/example.shtest --output tests/integration/example.sh
```

### Test Validation
```bash
# Validate that all integration tests are valid shell scripts
for test in tests/integration/*.sh; do
    bash -n "$test" || echo "Syntax error in $test"
done
```

## Best Practices

### Running Tests
1. **Clean environment**: Run tests in a clean environment
2. **Error handling**: Always check exit codes
3. **Logging**: Use proper logging for test results
4. **Isolation**: Tests should not interfere with each other
5. **Cleanup**: Ensure tests clean up after themselves

### Test Development
1. **Regenerate after changes**: Always regenerate integration tests after modifying E2E tests
2. **Test locally**: Test integration scripts locally before committing
3. **Version control**: Keep both E2E and integration tests in version control
4. **Documentation**: Document any special requirements or setup needed

## Continuous Integration
Integration tests can be run in CI/CD pipelines:
```yaml
# Example CI configuration
- name: Run Integration Tests
  run: |
    for test in tests/integration/*.sh; do
      bash "$test" || exit 1
    done
``` 