# Batch Testing Documentation

This repository contains utilities for writing automated shell tests using a simple Action/Resultat syntax. It also ships a VS Code extension for `.shtest` files.

The HTML documentation in [`docs/`](docs/index.html) is generated from the [iDocs](https://github.com/harnishdesign/iDocs) template and explains the language grammar and available tools.

## Quick Start
1. Create your `.shtest` scenarios inside `src/tests`.
2. Run `python src/generate_tests.py` to produce shell scripts in `output/`.
3. Optionally run `python src/export_to_excel.py` to create an Excel summary.

Default directories can be adjusted in `config.ini`.

## Command Reference

### `generate_tests.py`
Converts `.shtest` files into executable shell scripts saved in `output/`.

```bash
python src/generate_tests.py
```

Paths can be customised via `config.ini`.

### `export_to_excel.py`
Creates an Excel workbook summarising each scenario.

```bash
python src/export_to_excel.py --input-dir src/tests --output tests.xlsx
```

Use the options above to override the default locations.

## VS Code Extension
The `vscode/` folder contains a minimal syntax highlighter for `.shtest` files. To create the extension package, run the following commands:

```bash
npm install  # installs `vsce` with a compatible dependency set
npx vsce package
```

The `package.json` at the repository root pins `css-select@5.0.0` via `overrides` to avoid a packaging error in newer versions of `vsce`. Install the generated `.vsix` file in Visual Studio Code once the package is created.

## License
This project and the bundled documentation template are released under the MIT License.
