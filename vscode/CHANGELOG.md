# Changelog

All notable changes to the KnightBatch VS Code Extension will be documented in this file.

## [3.0.0] - 2024-01-15

### Added
- **Modular Architecture Support**: Full support for the new KnightBatch modular architecture
- **New Commands**: 
  - KnightBatch: Compile Current File
  - KnightBatch: Verify Syntax
  - KnightBatch: Show AST
  - KnightBatch: Show Tokens
  - KnightBatch: Compile Directory
  - KnightBatch: Export to Excel
- **Enhanced Syntax Highlighting**: Support for SQL operations, file operations, and variables
- **Modern Snippets**: New snippets for common patterns with better organization
- **Configuration System**: VS Code settings for paths, SQL driver, and debug mode
- **TypeScript Implementation**: Complete rewrite in TypeScript for better maintainability
- **Error Handling**: Improved error messages and debugging support

### Changed
- **Package Name**: Changed from `shtest` to `knightbatch-shtest`
- **Display Name**: Updated to "KnightBatch - Shell Test Language"
- **Version**: Bumped to 3.0.0 for major architecture changes
- **Syntax Highlighting**: Enhanced patterns for better recognition of modern syntax
- **Snippets**: Reorganized and modernized snippet collection

### Removed
- **Legacy Commands**: Removed old command structure in favor of new modular commands

### Fixed
- **Import Issues**: Resolved module import problems
- **Configuration Loading**: Fixed configuration path resolution
- **Error Reporting**: Improved error message clarity

## [2.0.3] - 2023-12-01

### Added
- Basic syntax highlighting for .shtest files
- Simple snippets for common patterns
- Dark theme support

### Changed
- Updated VS Code engine requirements

## [1.0.0] - 2023-11-01

### Added
- Initial release
- Basic language support
- File association for .shtest files

## [3.0.1] - 2024-06-28

### Added
- **Automated Packaging in CI**: The extension is now automatically packaged and uploaded in the GitHub workflow.
- **Documentation Improvements**: Updated README for clarity and new usage examples.
- **Snippet Enhancements**: Improved and clarified snippets for SQL, file, and directory operations.

### Changed
- **README**: Expanded documentation for configuration, snippets, and troubleshooting.
- **Snippets**: Modernized and clarified several snippet templates for better usability.

### Fixed
- **Packaging**: Ensured the `.vsix` is always up-to-date and available as a release asset.
