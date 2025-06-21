# Batch Testing Project

This repository contains scripts and VS Code assets for working with a small
shell testing language. The VS Code extension located in `vscode/` provides
basic syntax highlighting for files ending in `.shtest`.

## Rebuilding the VS Code extension

The packaged extension (`.vsix`) is not stored in the repository. If you have
been provided with a base64 encoded version of the extension (previously kept in
`vscode/shtest-syntax-0.0.1.txt`), decode it with:

```bash
base64 -d vscode/shtest-syntax-0.0.1.txt > vscode/shtest-syntax-0.0.1.vsix
```

Alternatively, if you have Node.js and [`vsce`](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
installed, you can generate the VSIX directly from the extension sources:

```bash
cd vscode
vsce package
```

This will create `shtest-syntax-0.0.1.vsix` which can then be installed in VS
Code.

## Exporting tests to Excel

Use `export_to_excel.py` to convert `.shtest` files into an Excel summary. Each row corresponds to a step of a test with columns for the test name, actions, expected results and actual results.

```bash
python src/export_to_excel.py --input-dir src/tests --output tests_summary.xlsx
```

This generates `tests_summary.xlsx` in the current directory.
