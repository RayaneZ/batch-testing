# KnightBatch VSCode Extension

Support for KnightBatch `.shtest` files with syntax highlighting, IntelliSense, compilation features, and test suite integration.

## Features

### Syntax Highlighting
- Full syntax highlighting for `.shtest` files
- Support for French and English keywords
- Highlighting for file paths, validation patterns, and SQL operations
- Support for new validation patterns with file paths (e.g., "Le fichier /tmp/test.txt est présent")

### Commands

#### Compilation Commands
- **KnightBatch: Compile Current File** - Compile the active `.shtest` file to shell script
- **KnightBatch: Compile Directory** - Compile all `.shtest` files in the workspace
- **KnightBatch: Export to Excel** - Export test cases to Excel format

#### Analysis Commands
- **KnightBatch: Verify Syntax** - Verify the syntax of the current file
- **KnightBatch: Show AST** - Display the Abstract Syntax Tree
- **KnightBatch: Show Tokens** - Display the lexical tokens

#### Testing Commands
- **KnightBatch: Run Test Suite** - Run the complete test suite using pytest

### Snippets

The extension provides code snippets for common patterns:

- `step` - Create a new step with action and result
- `action` - Create an action with result
- `exec` - Execute a script with success validation
- `execout` - Execute a script and check output
- `createfile` - Create a file and validate its presence
- `filepresent` - Check if a file is present (with file path)
- `fileempty` - Check if a file is empty (with file path)
- `fileabsent` - Check if a file is absent (with file path)
- `copyfile` - Copy a file and validate the copy
- `sqlconn` - Set up SQL connection variables
- `sqlscript` - Execute a SQL script and validate DB readiness

### Configuration

The extension can be configured through VSCode settings:

- `knightbatch.configPath` - Path to patterns configuration file
- `knightbatch.aliasesPath` - Path to aliases configuration file
- `knightbatch.outputDirectory` - Default output directory for compiled scripts
- `knightbatch.sqlDriver` - Default SQL driver to use
- `knightbatch.debugMode` - Enable debug mode for detailed logging
- `knightbatch.testDirectory` - Path to the test directory

## Usage

### Basic Usage
1. Open a `.shtest` file in VSCode
2. Use the command palette (Ctrl+Shift+P) to access KnightBatch commands
3. Right-click on `.shtest` files in the explorer for context menu options

### Validation Patterns
The extension supports the latest validation patterns including:

```shtest
# File existence with explicit paths
Action: touch /tmp/test.txt ; Résultat: Le fichier /tmp/test.txt est présent

# File content validation
Action: echo "test" > /tmp/file.txt ; Résultat: Le fichier /tmp/file.txt contient "test"

# File emptiness check
Action: touch /tmp/empty.txt ; Résultat: Le fichier /tmp/empty.txt est vide

# Complex validations
Action: run_script.sh ; Résultat: Le fichier /tmp/output.txt est présent et stdout contient "OK"
```

### Testing Integration
- Run the complete test suite directly from VSCode
- View test results in a new document
- Debug test failures with detailed output

## Requirements

- Python 3.9+ with the KnightBatch package installed
- pytest for test suite execution
- VSCode 1.101.0 or higher

## Installation

1. Install the KnightBatch Python package in your workspace:
   ```bash
   cd src
   pip install -e .
   ```

2. Install the VSCode extension from the marketplace or build from source

3. Configure the extension settings as needed

## Development

### Building the Extension
```bash
cd vscode
npm install
npm run compile
```

### Running Tests
```bash
cd vscode
npm test
```

### Extracting Plugin Patterns
```bash
cd vscode
npm run extract-patterns
```

## Changelog

### Version 3.0.0
- Updated to work with new modular architecture
- Added support for new validation patterns with file paths
- Integrated test suite execution
- Improved error handling and debugging
- Updated configuration paths for new project structure
- Added new snippets for file validation patterns

### Version 2.0.0
- Added syntax highlighting for French keywords
- Improved snippet support
- Added AST and token visualization

### Version 1.0.0
- Initial release with basic compilation support
- Syntax highlighting for `.shtest` files
- Basic command integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This extension is licensed under the same license as the KnightBatch project.
