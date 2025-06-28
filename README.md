# Batch Testing Documentation

This repository contains utilities for writing automated shell tests using a simple Action/Resultat syntax. It also ships a VS Code extension for `.shtest` files.

Full documentation lives in [`docs/`](docs/index.md) and can be served locally using [MkDocs](https://www.mkdocs.org/).
Launch a development server with:

```bash
mkdocs serve
```

This command starts a local site on `http://127.0.0.1:8000/` so you can browse the guide and CLI reference.
The existing HTML pages generated from the [iDocs](https://github.com/harnishdesign/iDocs) template remain available under the same folder.

## Quick Start
1. Create your `.shtest` scenarios inside `src/tests`.
2. Run `python src/generate_tests.py` to produce shell scripts in `output/`.
3. Optionally run `python src/verify_syntax.py` to validate the scenarios.
4. Optionally run `python src/export_to_excel.py` to create an Excel summary.

Default directories can be adjusted in `config.ini`.

## Command Reference

### `generate_tests.py`
Converts `.shtest` files into executable shell scripts saved in `output/`.

```bash
python src/generate_tests.py
```

Paths can be customised via `config.ini`.

### `verify_syntax.py`
Checks `.shtest` files for syntax errors using the built-in parser.

```bash
python src/verify_syntax.py src/tests
```

Provide directories or files as arguments. The script exits with a non-zero
status if issues are found.

### `export_to_excel.py`
Creates an Excel workbook summarising each scenario.

```bash
python src/export_to_excel.py --input-dir src/tests --output tests.xlsx
```

Use the options above to override the default locations.

### `run_all.py`
Convenience script that chains syntax checks, shell script generation and Excel export.

```bash
python src/run_all.py --input src/tests --output output --excel tests.xlsx
```

Disable steps with `--no-shell` or `--no-excel`.

## VS Code Extension
The `vscode/` folder contains a minimal syntax highlighter for `.shtest` files. Package it with `vsce package` (requires Node.js and `vsce`) and install the generated `.vsix` file in Visual Studio Code.

## License
This project and the bundled documentation template are released under the MIT License.
