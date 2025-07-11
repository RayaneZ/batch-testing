# Outils en ligne de commande

Cette page détaille les différents scripts disponibles dans le projet KnightBatch.

## `shtest.py` - Compilateur Principal

Le compilateur principal utilise l'architecture modulaire pour convertir les fichiers `.shtest` en scripts shell exécutables.

### Utilisation de base

```bash
# Compiler un fichier .shtest
python shtest.py tests/example.shtest

# Compiler avec sortie personnalisée
python shtest.py tests/example.shtest --output output/script.sh

# Mode debug pour voir les détails de compilation
python shtest.py tests/example.shtest --debug
```

### Options disponibles

```bash
python shtest.py [OPTIONS] <input_file>

Options:
  --output, -o PATH     Chemin de sortie pour le script généré
  --debug, -d          Mode debug avec logs détaillés
  --config PATH        Chemin vers le fichier de configuration
  --help, -h           Afficher l'aide
```

### Exemples d'utilisation

```bash
# Compilation simple
python shtest.py tests/new/example.shtest

# Compilation avec configuration personnalisée
python shtest.py tests/legacy/test_case_1.shtest --config custom_config.yml

# Mode debug pour diagnostiquer les problèmes
python shtest.py tests/new/sql_script_test.shtest --debug
```

## `generate_tests.py` - Générateur de Tests (Legacy)

Convertit les fichiers `.shtest` en scripts shell exécutables stockés dans le dossier configuré.

```bash
python src/generate_tests.py --input-dir src/tests --output output
```

Les chemins peuvent être personnalisés via `--input-dir` et `--output` ou par le fichier `config.ini`.

## `verify_syntax.py` - Vérificateur de Syntaxe

Vérifie la validité des fichiers `.shtest` et affiche les erreurs rencontrées.

```bash
python src/verify_syntax.py src/tests
```

Si aucune erreur n'est détectée, la commande affiche `Syntax OK` et renvoie le code de sortie `0`.

### Options avancées

```bash
python src/verify_syntax.py [OPTIONS] <input_path>

Options:
  --config PATH        Fichier de configuration YAML
  --verbose, -v        Affichage détaillé des erreurs
  --format FORMAT      Format de sortie (text, json, xml)
```

## `export_to_excel.py` - Export Excel

Génère un fichier Excel récapitulatif de vos scénarios de test.

```bash
python src/export_to_excel.py --input-dir src/tests --output tests.xlsx
```

### Options

```bash
python src/export_to_excel.py [OPTIONS]

Options:
  --input-dir, -i PATH  Répertoire contenant les fichiers .shtest
  --output, -o PATH     Fichier Excel de sortie
  --template PATH       Template Excel personnalisé
  --format FORMAT       Format de sortie (xlsx, csv, json)
```

## `run_all.py` - Pipeline Complet

Enchaîne la vérification, la génération des scripts et l'export Excel en une seule commande :

```bash
python src/run_all.py --input src/tests --output output --excel tests.xlsx
```

Chaque étape peut être désactivée via `--no-shell` ou `--no-excel`.

### Options complètes

```bash
python src/run_all.py [OPTIONS]

Options:
  --input, -i PATH     Répertoire d'entrée
  --output, -o PATH    Répertoire de sortie
  --excel PATH         Fichier Excel de sortie
  --no-verify          Désactiver la vérification de syntaxe
  --no-shell           Désactiver la génération de scripts shell
  --no-excel           Désactiver l'export Excel
  --config PATH        Fichier de configuration
  --debug, -d          Mode debug
```

## Tests et Validation

### Tests Unitaires

```bash
# Tests du core
python -m pytest tests/unit/test_core.py

# Tests du lexer modulaire
python -m pytest tests/unit/test_modular_lexer.py

# Tests du parser modulaire
python -m pytest tests/unit/test_modular_parser.py

# Tests du système complet
python -m pytest tests/unit/test_modular_system.py

# Tous les tests
python -m pytest tests/unit/
```

### Tests d'Intégration

```bash
# Test avec des fichiers .shtest réels
python shtest.py tests/new/example.shtest

# Test de tous les fichiers dans un répertoire
for file in tests/new/*.shtest; do
    python shtest.py "$file"
done
```

## Configuration

### Fichier config.ini

Le fichier `config.ini` situé à la racine du projet permet de définir les chemins par défaut :

```ini
[application]
input_dir = demo_env
output_dir = demo_env
sql_driver = oracle
config_path = config/patterns_hybrid.yml
aliases_path = config/aliases.yml
```

### Variables d'Environnement

```bash
# Chemin vers les fichiers de configuration
export SHTEST_CONFIG_PATH="config/patterns_hybrid.yml"

# Chemin vers les plugins
export SHTEST_PLUGIN_PATH="plugins/"

# Mode debug
export SHTEST_DEBUG=1
```

## Diagnostic et Dépannage

### Logs de Debug

```bash
# Activer les logs détaillés
export SHTEST_DEBUG=1
python shtest.py tests/example.shtest --debug
```

### Vérification de l'Installation

```bash
# Vérifier que tous les modules sont installés
python -c "import shtest_compiler; print('Installation OK')"

# Vérifier la configuration
python -c "from shtest_compiler.config import load_config; print(load_config())"
```

### Problèmes Courants

1. **Erreur d'import** : Vérifiez que vous êtes dans le bon répertoire (`src/`)
2. **Fichier de configuration manquant** : Vérifiez le chemin dans `config.ini`
3. **Patterns non reconnus** : Vérifiez `config/patterns_hybrid.yml` et `config/aliases.yml`

## Intégration avec VS Code

L'extension VS Code pour KnightBatch fournit :

- **Syntax highlighting** pour les fichiers `.shtest`
- **IntelliSense** pour les actions et validations
- **Compilation intégrée** via la palette de commandes
- **Validation en temps réel** de la syntaxe

### Commandes VS Code

- `KnightBatch: Compile Current File` : Compile le fichier actuel
- `KnightBatch: Verify Syntax` : Vérifie la syntaxe du fichier actuel
- `KnightBatch: Show AST` : Affiche l'AST du fichier actuel

---

Pour plus d'informations sur l'architecture modulaire, consultez la [documentation technique](modular_architecture.md).

