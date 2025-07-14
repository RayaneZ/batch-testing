# Changelog

All notable changes to the KnightBatch VSCode Extension will be documented in this file.

## [3.0.0] - 2024-12-19

### Added
- **Test Suite Integration**: New command "KnightBatch: Run Test Suite" to execute the complete test suite
- **New Validation Patterns**: Support for file path validation patterns like "Le fichier /tmp/test.txt est présent"
- **Enhanced Syntax Highlighting**: Updated highlighting for new validation patterns with file paths
- **New Snippets**: Added snippets for file validation patterns:
  - `filepresent` - Check if a file is present (with file path)
  - `fileempty` - Check if a file is empty (with file path)
  - `fileabsent` - Check if a file is absent (with file path)
- **Module-based Commands**: Updated all commands to use the new modular architecture
- **Improved Error Handling**: Better error messages and debugging support
- **Configuration Updates**: Updated default paths for new project structure

### Changed
- **Command Architecture**: All commands now use Python module imports instead of direct script execution
- **Configuration Paths**: Updated default configuration paths to match new project structure:
  - `configPath`: `src/shtest_compiler/config/patterns_actions.yml`
  - `aliasesPath`: `src/shtest_compiler/config/aliases.yml`
  - `testDirectory`: `src/testing`
- **Syntax Highlighting**: Enhanced to support new validation patterns with file paths
- **Snippets**: Updated existing snippets to use new validation patterns
- **Documentation**: Completely rewritten README with new features and usage examples

### Fixed
- **Import Issues**: Fixed module import paths for new project structure
- **Command Execution**: Improved command execution with better workspace handling
- **Error Reporting**: Enhanced error reporting with detailed output display
- **Test Integration**: Fixed test suite execution to work with new testing structure

### Technical Improvements
- **TypeScript Updates**: Updated to use latest TypeScript features
- **Error Handling**: Improved Promise-based error handling
- **Workspace Integration**: Better workspace folder detection and handling
- **Debug Support**: Enhanced debug mode with detailed logging

## [2.0.0] - 2024-11-15

### Added
- **French Language Support**: Added syntax highlighting for French keywords
- **AST Visualization**: New command to display Abstract Syntax Tree
- **Token Visualization**: New command to display lexical tokens
- **Enhanced Snippets**: Improved snippet support with more patterns
- **Configuration Options**: Added configurable paths and settings

### Changed
- **Syntax Highlighting**: Enhanced to support both French and English keywords
- **Command Structure**: Improved command organization and error handling
- **Documentation**: Updated documentation with new features

## [1.0.0] - 2024-10-01

### Added
- **Initial Release**: Basic VSCode extension for KnightBatch
- **Syntax Highlighting**: Support for `.shtest` files
- **Basic Commands**: Compile file, verify syntax
- **Snippets**: Basic code snippets for common patterns
- **Configuration**: Basic extension configuration

### Features
- Syntax highlighting for `.shtest` files
- Basic compilation support
- Command palette integration
- File explorer context menu
- Basic snippet support
