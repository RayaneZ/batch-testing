# Batch Testing Project

This repository contains scripts and VS Code assets for working with a small
shell testing language. The VS Code extension located in `vscode/` provides
basic syntax highlighting for files ending in `.shtest`.

## Writing tests

Test scenarios are written in plain text using the `Action:`/`Resultat:` format.
An example line looks like:

```text
Action: initialiser la base ; Resultat: base prête
```

Several examples can be found in `src/tests/` and the detailed grammar is
available in `docs/grammar.html`.

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

## Generating shell scripts

Use `generate_tests.py` to convert `.shtest` files into executable shell scripts.

```bash
python src/generate_tests.py --batch-path ./process_batch.sh
```

The scripts will be created in the `output/` directory with the same name as
their source test files.

## Checking results

Validation steps can verify the return code and command outputs. Use `retour N`
to check the exit status. To compare exact output, write `stdout=VALEUR` or
`stderr=VALEUR`.

You can also search for patterns with `stdout contient MOTIF` or `stderr contient MOTIF`. Phrases like "Le script retourne un code 0" or "Le script affiche un code \"030\"" are automatically interpreted as validations.
