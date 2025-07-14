# End-to-End Tests

This directory contains end-to-end tests written in `.shtest` format that test complete workflows and user scenarios.

## Purpose
E2E tests verify that the complete system works correctly from the user's perspective. They test real workflows and ensure that compiled scripts work as expected.

## Test Files

### Basic Functionality Tests
- `example.shtest` - Basic example demonstrating core features
- `test_basic_checks.shtest` - Tests basic validation and checking features
- `test_variable_equals.shtest` - Tests variable comparison functionality

### SQL Feature Tests
- `sql_comparison_example.shtest` - Comprehensive SQL comparison features
- `sql_conn_custom.shtest` - Tests custom SQL connection handling
- `sql_script_test.shtest` - Tests SQL script execution

### Validation Tests
- `test_all_validations.shtest` - Tests all available validation types
- `test_file_contains.shtest` - Tests file content validation
- `test_stdout_stderr.shtest` - Tests output stream validation

## Running E2E Tests

### Compile E2E Tests
```bash
# Compile all E2E tests to integration tests
python -m shtest_compiler.run_all --input tests/e2e --output tests/integration

# Compile specific test
python -m shtest_compiler.shtest compile_file tests/e2e/example.shtest --output tests/integration/example.sh

# Compile with verbose output
python -m shtest_compiler.shtest compile_file tests/e2e/example.shtest --output tests/integration/example.sh --verbose
```

### Verify E2E Test Syntax
```bash
# Verify syntax of all E2E tests
python -m shtest_compiler.shtest verify tests/e2e/

# Verify specific test
python -m shtest_compiler.shtest verify tests/e2e/example.shtest
```

## Writing E2E Tests

### Test Structure
```shtest
Étape: Description of the test step
Action: Natural language description of the action to perform
Résultat: Expected outcome or validation

Étape: Another test step
Action: Another action
Résultat: Another validation
```

### Example Test
```shtest
Étape: Test file creation
Action: créer le fichier test.txt
Résultat: le fichier test.txt existe

Étape: Test file content
Action: écrire "Hello World" dans le fichier test.txt
Résultat: le fichier test.txt contient "Hello World"

Étape: Cleanup
Action: supprimer le fichier test.txt
Résultat: le fichier test.txt n'existe pas
```

### Best Practices
1. **Clear steps**: Each step should have a clear purpose
2. **Natural language**: Use natural, readable language for actions and results
3. **Complete workflows**: Test complete user workflows, not just individual features
4. **Realistic scenarios**: Test scenarios that users would actually encounter
5. **Cleanup**: Include cleanup steps to leave the system in a clean state

### Test Categories
- **Basic operations**: File, directory, and system operations
- **SQL operations**: Database queries, comparisons, and exports
- **Validation scenarios**: Different types of validations and assertions
- **Error handling**: Tests that verify proper error handling
- **Integration scenarios**: Tests that combine multiple features

## Test Naming Conventions
- `test_<feature>.shtest` - Tests for specific features
- `<feature>_example.shtest` - Example tests demonstrating features
- `test_<workflow>.shtest` - Tests for complete workflows

## Dependencies
E2E tests may depend on:
- File system access (for file/directory operations)
- Database connections (for SQL tests)
- System commands (for script execution)
- Environment variables (for configuration)

## Compilation Process
1. **Parse**: `.shtest` files are parsed into AST
2. **Validate**: Syntax and semantics are validated
3. **Compile**: AST is compiled to shell scripts
4. **Generate**: Shell scripts are generated in the integration directory

## Debugging E2E Tests
- Use `--verbose` flag for detailed compilation output
- Check generated shell scripts in integration directory
- Run integration tests to see actual execution
- Use `--debug` flag for additional debugging information 