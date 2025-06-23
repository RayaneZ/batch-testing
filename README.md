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
python src/generate_tests.py --batch-path ./process_batch.sh
```

The scripts will be created in the `output/` directory with the same name as
their source test files.

Generated scripts use `/bin/sh` for portability.

Initialization lines that reference `*.sql` files will execute those scripts automatically.
Set the `SQL_CONN` environment variable to override the SQL connection used by
`execute_sql`. For example:

```bash
export SQL_CONN="sqlplus -S myuser/mypass@mydb"
```
If `SQL_CONN` is unset, `sqlplus -S user/password@db` is used.

### Options

- `--batch-path PATH` – path to the script to run for each test (default: `./process_batch.sh`)

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
