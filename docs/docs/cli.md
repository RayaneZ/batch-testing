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

### Gestion d'Erreurs

Le compilateur dispose d'un système de validation robuste qui détecte et signale les erreurs :

```bash
# Erreur de syntaxe - fichier invalide
python shtest.py tests/e2e/ko/invalid_syntax_1.shtest
# Sortie: [ERROR] Parse error in file: AST validation failed: Found orphaned action...

# Erreur de validation - fichier vide
python shtest.py tests/e2e/ko/empty_file.shtest
# Sortie: [ERROR] Parse error in file: AST validation failed: File is empty or contains no steps

# Code de sortie non-zéro en cas d'erreur
echo $?  # Affiche 1 en cas d'erreur
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

## `run_all.py` - Pipeline Complet

Enchaîne la vérification, la génération des scripts et l'export Excel en une seule commande :

```bash
python src/run_all.py --input src/tests --output output --excel tests.xlsx
```

### Validation Robuste

Le pipeline inclut une validation complète qui échoue rapidement sur les erreurs :

```bash
# Validation d'un fichier invalide
python src/run_all.py --input tests/e2e/ko/invalid_syntax_1.shtest
# Sortie: [1/3] Vérification de la syntaxe...
#         Erreurs de syntaxe détectées:
#           - tests/e2e/ko/invalid_syntax_1.shtest: AST validation failed: Found orphaned action...

# Validation d'un répertoire mixte
python src/run_all.py --input tests/e2e/
# Sortie: [1/3] Vérification de la syntaxe...
#         Erreurs de syntaxe détectées:
#           - tests/e2e/ko/invalid_syntax_1.shtest: AST validation failed: Found orphaned action...
#         [FAIL] One or more files failed to compile.
```

### Options complètes

```bash
python src/run_all.py [OPTIONS]

Options:
  --input, -i PATH     Répertoire d'entrée ou fichier unique
  --output, -o PATH    Répertoire de sortie
  --excel PATH         Fichier Excel de sortie
  --no-shell           Désactiver la génération de scripts shell
  --no-excel           Désactiver l'export Excel
  --debug, -d          Mode debug avec logs détaillés
```

## `verify_syntax.py` - Vérificateur de Syntaxe

Vérifie la validité des fichiers `.shtest` et affiche les erreurs rencontrées.

```bash
python src/verify_syntax.py src/tests
```

### Validation Avancée

Le vérificateur utilise le système de validation AST pour détecter :

- **Fichiers vides** ou contenant seulement des commentaires
- **Actions orphelines** sans mot-clé `Étape:`
- **Actions malformées** avec commandes vides ou invalides
- **Validations incomplètes** ou malformées
- **Structure invalide** (imbrication incorrecte, etc.)

```bash
# Validation d'un fichier valide
python src/verify_syntax.py tests/e2e/ok/example.shtest
# Sortie: [✔] Syntaxe valide.

# Validation d'un fichier invalide
python src/verify_syntax.py tests/e2e/ko/invalid_syntax_1.shtest
# Sortie: [ERROR] Erreur de syntaxe: AST validation failed: Found orphaned action...

# Mode verbose pour plus de détails
python src/verify_syntax.py tests/e2e/ko/invalid_syntax_1.shtest --verbose
```

### Options avancées

```bash
python src/verify_syntax.py [OPTIONS] <input_path>

Options:
  --verbose, -v        Affichage détaillé des erreurs
  --debug, -d          Mode debug avec tokens et AST
```

## Tests et Validation

### Tests E2E

```bash
# Exécuter tous les tests E2E
python tests/e2e/run_e2e_tests.py

# Tests positifs uniquement
python tests/e2e/run_e2e_tests.py --positive-only

# Tests négatifs uniquement
python tests/e2e/ko/run_ko_tests.py
```

### Tests Négatifs (Validation d'Erreurs)

```bash
# Exécuter la suite de tests négatifs
python tests/e2e/ko/run_ko_tests.py

# Tester un fichier spécifique
python -m shtest_compiler.run_all --input tests/e2e/ko/invalid_syntax_1.shtest
```

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

## Outils de Diagnostic

### Debug Parser

```bash
# Analyser le comportement du parser sur un fichier
python tests/e2e/ko/debug_parser.py

# Debug d'un fichier spécifique
python -c "
import sys
sys.path.insert(0, 'src')
from tests.e2e.ko.debug_parser import debug_file
debug_file('tests/e2e/ko/invalid_syntax_1.shtest')
"
```

### Mode Debug Complet

```bash
# Activer le mode debug global
export SHTEST_DEBUG=1

# Exécuter avec logs détaillés
python src/run_all.py --input tests/example.shtest --debug
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

# Driver SQL par défaut
export SQL_DRIVER="oracle"
```

## Codes de Sortie

Le système utilise des codes de sortie standardisés :

- **0** : Succès - Aucune erreur détectée
- **1** : Erreur de validation ou de compilation
- **2** : Erreur de configuration
- **3** : Erreur système

### Exemples

```bash
# Succès
python src/run_all.py --input tests/e2e/ok/example.shtest
echo $?  # Affiche 0

# Erreur de validation
python src/run_all.py --input tests/e2e/ko/invalid_syntax_1.shtest
echo $?  # Affiche 1

# Erreur de configuration
python src/run_all.py --input nonexistent/
echo $?  # Affiche 2
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

# Vérifier les dépendances
python -c "import yaml, openpyxl, sqlalchemy; print('Dépendances OK')"
```

### Messages d'Erreur Courants

| Erreur | Cause | Solution |
|--------|-------|----------|
| `File is empty or contains no steps` | Fichier vide ou commentaires uniquement | Ajouter au moins une étape |
| `Step 'X' has no actions` | Étape sans actions | Ajouter des actions à l'étape |
| `Found orphaned action` | Action sans mot-clé `Étape:` | Préfixer l'action avec `Étape:` |
| `Action has empty command` | Action sans commande | Ajouter une commande à l'action |
| `Invalid validation phrase` | Validation malformée | Corriger la syntaxe de validation |

