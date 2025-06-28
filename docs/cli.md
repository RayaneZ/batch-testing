# Outils en ligne de commande

Cette page détaille les différents scripts disponibles dans le projet.

## `generate_tests.py`
Convertit les fichiers `.shtest` en scripts shell exécutables stockés dans le dossier configuré.

```bash
python src/generate_tests.py --input-dir src/tests --output output
```

Les chemins peuvent être personnalisés via `--input-dir` et `--output` ou par le fichier `config.ini`.

## `verify_syntax.py`
Vérifie la validité des fichiers `.shtest` et affiche les erreurs rencontrées.

```bash
python src/verify_syntax.py src/tests
```

Si aucune erreur n'est détectée, la commande affiche `Syntax OK` et renvoie le code de sortie `0`.

## `export_to_excel.py`
Génère un fichier Excel récapitulatif de vos scénarios de test.

```bash
python src/export_to_excel.py --input-dir src/tests --output tests.xlsx
```

## `run_all.py`
Enchaîne la vérification, la génération des scripts et l'export Excel en une seule commande :

```bash
python src/run_all.py --input src/tests --output output --excel tests.xlsx
```

Chaque étape peut être désactivée via `--no-shell` ou `--no-excel`.

