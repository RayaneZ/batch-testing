# Batch Testing Project

This repository contains scripts and VS Code assets for working with a small
shell testing language. The VS Code extension located in `vscode/` provides
basic syntax highlighting for files ending in `.shtest`.

## Writing tests

Test scenarios are written in plain text using the `Action:`/`Resultat:` format.
An example line looks like:

```text
Action: configurer la base ; Resultat: base prête
```

Trailing periods or semicolons in the result are ignored by the parser.

Several examples can be found in `src/tests/` and the detailed grammar is
available in `docs/documentation.html`.

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

### Options

- `--input-dir DIR` – directory containing `.shtest` files (default: `tests`)
- `--output FILE` – path to the resulting Excel file (default: `tests_summary.xlsx`)

## Generating shell scripts

Use `generate_tests.py` to convert `.shtest` files into executable shell scripts.

```bash
python src/generate_tests.py
```

The scripts will be created in the `output/` directory with the same name as
their source test files.

Default directories can also be configured via
`config.ini` at the repository root:

```ini
[application]
input_dir = src/tests
output_dir = output
```

`generate_tests.py` will read this file if present and use the values as
defaults for where test files are located.

Generated scripts use `/bin/sh` for portability.

Initialization lines that reference `*.sql` files will execute those scripts automatically.
Set the `SQL_CONN` environment variable to override the SQL connection used by
`execute_sql`. For example:

```bash
export SQL_CONN="sqlplus -S myuser/mypass@mydb"
```
If `SQL_CONN` is unset, `sqlplus -S user/password@db` is used.

### Notes

The path to the batch script must be provided directly in each `.shtest` file.

To pass arguments to the batch script, use `argument NOM=VALEUR` in your action
lines and chain additional pairs with `et`:

```text
Action: Exécuter mon_batch.sh avec l'argument produit=42 et la quantité=10 ;
```

The generated command will be `mon_batch.sh produit=42 quantité=10`.

## Checking results

Validation steps can verify the return code and command outputs. Use `retour N`
to check the exit status. To compare exact output, write `stdout=VALEUR` or
`stderr=VALEUR`.

You can also search for patterns with `stdout contient MOTIF` or `stderr contient MOTIF`. Phrases like "Le script retourne un code 0" or "Le script affiche un code \"030\"" are automatically interpreted as validations.

Several validations can be combined in one expression using the keywords `et` and `ou`. Parentheses are supported and parsed with the shunting-yard algorithm. For example:

```text
Resultat: retour 0 et (stdout contient OK ou stderr contient WARNING)
```

Additional checks exist for file operations:
- `le fichier /chemin existe` or `Le fichier est présent` to validate presence.
- `le fichier est copié` / `le dossier est copié` to assert copy success.

## Project architecture

This section explains how each Python module reacts to the `.shtest` files and
how the pieces fit together. See `docs/documentation.html` for a complete
grammar reference and an HTML version of this overview.

### `parser.py`

The parser reads one line at a time and matches it against a set of regular
expressions. Phrases such as `Le script retourne un code 0` are normalised by
`AliasResolver` into atomic forms like `retour 0`. The resulting dictionary
contains keys for `initialization`, `execution`, `file_operations`,
`validation`, and more. Preserving the order of the original lines guarantees
that generated scripts mirror the input description.

Example output for a single line:

```python
{
    "initialization": [],
    "execution": ["exécuter purge.sh"],
    "validation": ["retour 0"],
}
```

### `generate_tests.py`

This script loops over all `.shtest` files in the configured directory. Each
file is parsed and transformed into shell code through the templates found in
`templates.py`. If an action references a `.sql` file, the generated command is
similar to:

```sh
run_cmd "sqlplus -S ${SQL_CONN:-user/password@db} @purge.sql"
```

Helper functions capture the command output so validations can compare the
expected and actual values.

### `validation_compiler.py`

Validation expressions form a small language with operators `et` and `ou`.
They are first parsed into an abstract syntax tree so that parentheses and
precedence are honoured. Each atomic check (e.g. `stdout contient OK`) becomes a
few shell lines updating a boolean variable. The final variable is then used to
print `OK` or `KO`.

### `export_to_excel.py`

For reporting purposes this utility converts the parsed structure of each test
into an Excel workbook. Every `.shtest` file becomes a worksheet listing each
step, the normalised actions and the expected results. This helps reviewing long
scenarios without reading shell scripts.

### Configuration file

`config.ini` at the repository root stores the default input and output
directories. If the file is missing, `generate_tests.py` falls back to
`src/tests` for input and `output` for generated scripts.

Overall the workflow is:

1. parse the text files;
2. generate the shell scripts;
3. optionally export the same information to Excel.
