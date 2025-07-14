# Outils en ligne de commande

Cette page détaille les différents scripts disponibles dans le projet KnightBatch, tous basés sur l'architecture modulaire moderne.

KnightBatch propose une CLI simple et puissante pour compiler, valider et exécuter des scénarios `.shtest` :
- **Compilation** : Conversion d'un fichier `.shtest` en script shell exécutable
- **Validation** : Vérification de la syntaxe et de la structure
- **Pipeline complet** : Compilation, export Excel, et vérification en une seule commande
- **Tests** : Exécution automatisée des tests unitaires, E2E et d'intégration

---

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

Le compilateur dispose d'un système de validation robuste qui détecte et signale les erreurs :

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

---

## `run_all.py` - Pipeline Complet

Enchaîne la vérification, la génération des scripts et l'export Excel en une seule commande :

```bash
python src/run_all.py --input src/tests --output output --excel tests.xlsx
```

### Validation Robuste

Le pipeline inclut une validation complète qui échoue rapidement sur les erreurs :

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

---

## `verify_syntax.py` - Vérificateur de Syntaxe

Vérifie la validité des fichiers `.shtest` et affiche les erreurs rencontrées.

```bash
python src/verify_syntax.py src/tests
```

### Validation Avancée

Le vérificateur utilise le système de validation AST pour détecter :

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

---

## Tests et Validation

### Tests E2E

```bash
# Compiler et exécuter tous les tests E2E
python src/shtest_compiler/run_tests.py --all
```

### Tests Unitaires

```bash
# Tous les tests unitaires
python -m pytest tests/unit/
```

### Tests d'Intégration

```bash
# Exécuter tous les scripts shell générés
for test in tests/integration/*.sh; do
    bash "$test"
done
```

---

## Outils de Diagnostic

### Debug Parser

```bash
# Analyser le comportement du parser sur un fichier
python tests/e2e/ko/debug_parser.py
```

### Mode Debug Complet

```bash
# Activer le mode debug global
export SHTEST_DEBUG=1

# Exécuter avec logs détaillés
python src/run_all.py --input tests/example.shtest --debug
```

---

## Configuration

### Fichier config.ini

Le fichier `config.ini` situé à la racine du projet permet de définir les chemins par défaut :

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
export SHTEST_PLUGIN_PATH="src/shtest_compiler/plugins"
```

