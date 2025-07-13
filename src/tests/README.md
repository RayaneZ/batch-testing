# Test Organization

This directory contains all tests for the batch testing framework, organized by type and purpose.

## Directory Structure

### `/unit/` - Unit Tests
**Purpose**: Test individual components and functions in isolation
**Files**: Python test files (`.py`)
**Examples**: 
- `test_parser.py` - Tests the parser component
- `test_compiler.py` - Tests the compiler component
- `test_modular_lexer.py` - Tests the lexer functionality

**How to run**:
```bash
python -m pytest tests/unit/
```

### `/e2e/` - End-to-End Tests
**Purpose**: Test complete workflows using `.shtest` files
**Files**: `.shtest` files (source test files)
**Examples**:
- `sql_comparison_example.shtest` - Tests SQL comparison features
- `test_basic_checks.shtest` - Tests basic validation features
- `example.shtest` - Basic example tests

**How to run**:
```bash
python -m shtest_compiler.run_all --input tests/e2e --output tests/integration
```

### `/integration/` - Integration Tests
**Purpose**: Compiled shell scripts for integration testing
**Files**: `.sh` files (compiled from `.shtest` files)
**Examples**:
- `test_basic_checks.sh` - Compiled basic checks test
- `example.sh` - Compiled example test
- `sql_script_test.sh` - Compiled SQL test

**How to run**:
```bash
# Run individual tests
bash tests/integration/test_basic_checks.sh

# Run all integration tests
for test in tests/integration/*.sh; do
    bash "$test"
done
```

### `/legacy/` - Legacy Tests
**Purpose**: Old test files for backward compatibility
**Files**: Mix of `.shtest` and `.sh` files
**Note**: These tests may use deprecated features

## Test Categories

### Unit Tests
- **Parser Tests**: Test the `.shtest` file parsing
- **Compiler Tests**: Test the compilation to shell scripts
- **Lexer Tests**: Test tokenization and lexical analysis
- **Visitor Tests**: Test AST traversal and processing
- **Core Tests**: Test core functionality

### E2E Tests
- **Basic Functionality**: Core features like file operations, variable handling
- **SQL Features**: Database operations, query execution, result comparison
- **Validation Tests**: Different types of validations and assertions
- **Plugin Tests**: Tests for various plugins (file, directory, SQL, etc.)

### Integration Tests
- **Compiled Scripts**: Shell scripts generated from E2E tests
- **Runtime Tests**: Tests that verify the generated scripts work correctly
- **Cross-Platform Tests**: Tests that work on different operating systems

## Running Tests

### All Tests
```bash
# Run unit tests
python -m pytest tests/unit/

# Compile E2E tests to integration tests
python -m shtest_compiler.run_all --input tests/e2e --output tests/integration

# Run integration tests
for test in tests/integration/*.sh; do
    bash "$test"
done
```

### Specific Test Types
```bash
# Run only unit tests
python -m pytest tests/unit/ -v

# Compile specific E2E test
python -m shtest_compiler.shtest compile_file tests/e2e/example.shtest --output tests/integration/example.sh

# Run specific integration test
bash tests/integration/example.sh
```

## Adding New Tests

### Unit Tests
1. Create a new file in `tests/unit/` with prefix `test_`
2. Use pytest framework
3. Test individual functions or classes
4. Example: `tests/unit/test_new_feature.py`

### E2E Tests
1. Create a new `.shtest` file in `tests/e2e/`
2. Use natural language syntax
3. Test complete workflows
4. Example: `tests/e2e/test_new_workflow.shtest`

### Integration Tests
1. Compile E2E tests to generate integration tests
2. Integration tests are automatically generated
3. They verify that compiled scripts work correctly

## Test Naming Conventions

- **Unit Tests**: `test_<component>_<feature>.py`
- **E2E Tests**: `test_<feature>.shtest` or `<feature>_example.shtest`
- **Integration Tests**: Same name as E2E tests but with `.sh` extension

## Best Practices

1. **Unit Tests**: Test one thing at a time, use descriptive names
2. **E2E Tests**: Test complete user workflows, use natural language
3. **Integration Tests**: Verify that compiled scripts work in real environments
4. **Documentation**: Keep this README updated when adding new test types 