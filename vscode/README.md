# KnightBatch VS Code Extension

Support for KnightBatch `.shtest` files with syntax highlighting, IntelliSense, and compilation features.

## Features

### 🎨 Syntax Highlighting
- Full syntax highlighting for `.shtest` files
- Support for actions, validations, SQL operations, and file operations
- Color-coded keywords, variables, and logical operators

### ⚡ Commands
- **KnightBatch: Compile Current File** - Compile the current `.shtest` file to shell script
- **KnightBatch: Verify Syntax** - Verify the syntax of the current file
- **KnightBatch: Show AST** - Display the Abstract Syntax Tree
- **KnightBatch: Show Tokens** - Display the tokenized content
- **KnightBatch: Compile Directory** - Compile all `.shtest` files in the workspace
- **KnightBatch: Export to Excel** - Export test scenarios to Excel

### 📝 Snippets
- Modern snippets for common patterns
- Legacy patterns for backward compatibility
- Quick templates for SQL operations, file operations, and validations

### ⚙️ Configuration
- Configurable paths for patterns and aliases
- Customizable output directory
- SQL driver selection
- Debug mode toggle

## Installation

### From VSIX
1. Download the `.vsix` file
2. In VS Code, go to Extensions (Ctrl+Shift+X)
3. Click the "..." menu and select "Install from VSIX..."
4. Select the downloaded file

### From Source
```bash
cd vscode
npm install
npm run compile
npx vsce package
```

## Usage

### Basic Usage
1. Open a `.shtest` file
2. Use snippets to quickly create test scenarios
3. Use commands from the Command Palette (Ctrl+Shift+P)

### Commands
- **Compile Current File**: Compiles the active `.shtest` file to a shell script
- **Verify Syntax**: Checks the syntax of the current file
- **Show AST**: Displays the Abstract Syntax Tree in a new tab
- **Show Tokens**: Shows the tokenized content in a new tab

### Snippets
Type the prefix and press Tab to insert:
- `step` - Create a new step block
- `action` - Create an action with result
- `exec` - Execute a script
- `createfile` - Create a file
- `sqlconn` - Set up SQL connection
- `var` - Define a variable

### Configuration
Add to your VS Code settings:
```json
{
  "knightbatch.configPath": "config/patterns_actions.yml",
  "knightbatch.aliasesPath": "config/aliases.yml",
  "knightbatch.outputDirectory": "output",
  "knightbatch.sqlDriver": "mysql",
  "knightbatch.debugMode": false
}
```

## Architecture Support

This extension supports the new modular architecture:

- **Core Components**: Visitor pattern, AST nodes, compilation context
- **Modular Lexer**: Configurable tokenization with patterns and filters
- **Modular Parser**: Configurable grammar with AST builder
- **Modular Compiler**: Specialized visitors and code generators
- **Plugin System**: Extensible matchers and validations

## Examples

### Basic Test Scenario
```shtest
Etape: Setup
Action: Créer le dossier /tmp/test ; Résultat: le dossier est créé.
Action: Créer le fichier /tmp/test/data.txt ; Résultat: le fichier est présent.

Etape: Execution
Action: Exécuter /opt/scripts/process.sh ; Résultat: retour 0.
Action: Vérifier que le fichier /tmp/test/result.txt existe ; Résultat: le fichier existe.
```

### SQL Operations
```shtest
Action: Définir la variable SQL_DRIVER = mysql ; Résultat: identifiants configurés.
Action: Définir la variable SQL_CONN = user/pass@db ; Résultat: identifiants configurés.
Action: Exécuter le script SQL init.sql ; Résultat: La base est prête.
```

### Complex Validations
```shtest
Action: Exécuter script.sh ; Résultat: retour 0 et (stdout contient "OK" ou stderr contient "WARNING").
```

## Troubleshooting

### Common Issues
1. **Script not found**: Ensure you're in the correct workspace with the KnightBatch source
2. **Configuration errors**: Check the paths in VS Code settings
3. **Compilation failures**: Verify the `.shtest` syntax and check debug mode

### Debug Mode
Enable debug mode in settings to get detailed error messages:
```json
{
  "knightbatch.debugMode": true
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `npm test`
5. Submit a pull request

## License

MIT License - see LICENSE.txt for details.
