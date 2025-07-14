# Manuel Utilisateur KnightBatch

| <img src="assets/logo.png" alt="KnightBatch" width="120" style="border-radius: 15px;"/> | Ce manuel complet guide l'utilisateur à travers toutes les fonctionnalités du framework KnightBatch, de l'installation à l'utilisation avancée. |
|  | --- |

## Table des Matières

1. [Installation et Configuration](#installation-et-configuration)
2. [Premiers Pas](#premiers-pas)
3. [Écriture de Tests](#écriture-de-tests)
4. [Compilation et Exécution](#compilation-et-exécution)
5. [Validation et Debug](#validation-et-debug)
6. [Fonctionnalités Avancées](#fonctionnalités-avancées)
7. [Intégration Continue](#intégration-continue)
8. [Dépannage](#dépannage)

---

## Installation et Configuration

### Prérequis

- **Python 3.8+** : Le framework est développé en Python moderne
- **Bash** : Pour l'exécution des scripts générés
- **Git** : Pour la gestion des versions

### Installation

```bash
# Cloner le repository
git clone <repository-url>
cd batch-testing

# Installer les dépendances
pip install -r src/requirements.txt

# Vérifier l'installation
python src/shtest_compiler/compile_file.py --help
```

### Configuration Initiale

Le fichier `src/config.ini` configure les paramètres par défaut :

```ini
[application]
input_dir = tests
output_dir = output
sql_driver = oracle
```

---

## Premiers Pas

### 1. Créer votre Premier Test

Créez un fichier `mon_premier_test.shtest` :

```shtest
Étape: Préparation de l'environnement
Action: Créer le dossier ./test_data
Résultat: le dossier est créé

Étape: Test de création de fichier
Action: Créer le fichier ./test_data/example.txt avec le contenu "Hello World"
Résultat: le fichier existe
Résultat: le fichier contient "Hello World"

Étape: Vérification finale
Action: Lister le dossier ./test_data
Résultat: stdout contient "example.txt"
```

### 2. Compiler le Test

```bash
# Compilation simple
python src/shtest_compiler/compile_file.py mon_premier_test.shtest

# Compilation avec sortie personnalisée
python src/shtest_compiler/compile_file.py mon_premier_test.shtest --output mon_script.sh
```

### 3. Exécuter le Test

```bash
# Exécution directe
bash mon_premier_test.sh

# Exécution avec logs détaillés
bash -x mon_premier_test.sh
```

---

## Écriture de Tests

### Structure de Base

Un fichier `.shtest` suit cette structure :

```shtest
Étape: Nom de l'étape
Action: Commande ou action à exécuter
Résultat: Validation attendue
Résultat: Autre validation attendue

Étape: Étape suivante
Action: Nouvelle action
Résultat: Validation
```

### Types d'Actions

#### Actions de Fichiers

```shtest
# Création de fichiers
Action: Créer le fichier ./data/config.json
Action: Créer le fichier ./logs/app.log avec le contenu "Démarrage"

# Copie et déplacement
Action: Copier le fichier ./source.txt vers ./dest.txt
Action: Déplacer le fichier ./old.txt vers ./archive/

# Suppression
Action: Supprimer le fichier ./temp.txt
Action: Purger le dossier ./cache/
```

#### Actions de Dossiers

```shtest
# Création de dossiers
Action: Créer le dossier ./output
Action: Créer le dossier ./logs avec les droits 755

# Opérations sur dossiers
Action: Copier le dossier ./src vers ./backup
Action: Déplacer le dossier ./old vers ./archive
```

#### Actions de Scripts

```shtest
# Exécution de scripts
Action: Exécuter le script ./setup.sh
Action: Exécuter le script ./deploy.sh avec les arguments "prod" "v1.2.3"

# Exécution avec variables d'environnement
Action: Exécuter le script ./test.sh avec la variable ENV=staging
```

#### Actions SQL

```shtest
# Requêtes SQL
Action: Exécuter la requête SQL "SELECT COUNT(*) FROM users"
Action: Exécuter le script SQL ./migration.sql
```

### Types de Validations

#### Validations de Fichiers

```shtest
# Existence et contenu
Résultat: le fichier existe
Résultat: le fichier est vide
Résultat: le fichier contient "texte recherché"
Résultat: le fichier contient exactement "contenu exact"

# Comparaisons
Résultat: les fichiers sont identiques
Résultat: le fichier a été copié
Résultat: le fichier a été déplacé
```

#### Validations de Dossiers

```shtest
# Existence et contenu
Résultat: le dossier existe
Résultat: le dossier est vide
Résultat: le dossier contient 5 fichiers
Résultat: le dossier contient "nom_fichier.txt"
```

#### Validations de Sortie

```shtest
# Sortie standard
Résultat: stdout contient "message attendu"
Résultat: stdout contient exactement "sortie exacte"

# Sortie d'erreur
Résultat: stderr contient "message d'erreur"
Résultat: aucun message d'erreur
```

#### Validations de Code de Retour

```shtest
# Codes de retour
Résultat: le code de retour est 0
Résultat: le code de retour est différent de 0
```

#### Validations de Variables

```shtest
# Variables d'environnement
Résultat: la variable ENV est définie
Résultat: la variable VERSION égale "1.2.3"
```

### Variables et Contexte

#### Variables d'Environnement

```shtest
Étape: Configuration
Action: Définir la variable ENV avec la valeur "production"
Résultat: la variable est définie

Étape: Utilisation
Action: Exécuter le script ./deploy.sh
Résultat: stdout contient "Deploying to production"
```

#### Variables de Contexte

```shtest
Étape: Préparation
Action: Créer le fichier ./config.json
Résultat: le fichier existe

Étape: Utilisation du contexte
Action: Exécuter le script ./process.sh
Résultat: le fichier config.json a été modifié
```

---

## Compilation et Exécution

### Compilation Simple

```bash
# Compiler un fichier
python src/shtest_compiler/compile_file.py test.shtest

# Compiler avec options
python src/shtest_compiler/compile_file.py test.shtest --output mon_script.sh --debug
```

### Pipeline Complet

```bash
# Compilation, validation et export Excel
python src/shtest_compiler/run_all.py --input tests/ --output output/ --excel rapport.xlsx

# Options disponibles
python src/shtest_compiler/run_all.py --help
```

### Exécution de Tests

```bash
# Exécuter tous les tests
python src/shtest_compiler/run_tests.py --all

# Tests spécifiques
python src/shtest_compiler/run_tests.py --unit
python src/shtest_compiler/run_tests.py --e2e
python src/shtest_compiler/run_tests.py --integration
```

---

## Validation et Debug

### Validation de Syntaxe

```bash
# Validation d'un fichier
python src/shtest_compiler/verify_syntax.py test.shtest

# Validation d'un répertoire
python src/shtest_compiler/verify_syntax.py tests/

# Mode verbose
python src/shtest_compiler/verify_syntax.py test.shtest --verbose
```

### Mode Debug

```bash
# Activer le debug global
export SHTEST_DEBUG=1

# Compilation avec debug
python src/shtest_compiler/compile_file.py test.shtest --debug

# Pipeline avec debug
python src/shtest_compiler/run_all.py --input tests/ --debug
```

### Outils de Diagnostic

```bash
# Analyser un fichier problématique
python tests/e2e/ko/debug_parser.py

# Vérifier la structure AST
python -c "
from shtest_compiler.parser.configurable_parser import ConfigurableParser
parser = ConfigurableParser(debug=True)
with open('test.shtest') as f:
    ast = parser.parse(f.read())
print('AST valide')
"
```

---

## Fonctionnalités Avancées

### Plugins Personnalisés

#### Créer un Plugin

```python
# plugins/mon_plugin.py
from shtest_compiler.core.handlers.base import BaseHandler

class MonHandler(BaseHandler):
    def can_handle(self, action):
        return "mon_action" in action.lower()

    def handle(self, action, context):
        # Logique de traitement
        return f"echo 'Action personnalisée: {action}'"
```

#### Configuration YAML

```yaml
# config/patterns_actions.yml
mon_action:
  handler: mon_plugin.MonHandler
  description: "Action personnalisée"
  examples:
    - "Action: mon_action avec paramètre"
```

### Validation Avancée

#### Validations Combinées

```shtest
Étape: Test complexe
Action: Créer le fichier ./data.json avec le contenu '{"status": "ok"}'
Résultat: le fichier existe
Résultat: le fichier contient "status"
Résultat: stdout contient "Fichier créé avec succès"
```

#### Validations Conditionnelles

```shtest
Étape: Test conditionnel
Action: Exécuter le script ./check_status.sh
Résultat: le code de retour est 0 OU stdout contient "warning"
```

### Intégration avec Base de Données

```shtest
Étape: Test base de données
Action: Exécuter la requête SQL "SELECT COUNT(*) FROM users WHERE active = 1"
Résultat: stdout contient "5"
```

---

## Intégration Continue

### Configuration CI/CD

#### GitHub Actions

```yaml
# .github/workflows/test.yml
name: KnightBatch Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r src/requirements.txt
      - name: Run tests
        run: |
          python src/shtest_compiler/run_tests.py --all
```

#### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r src/requirements.txt'
                sh 'python src/shtest_compiler/run_tests.py --all'
            }
        }
    }
}
```

### Rapports Automatisés

```bash
# Générer un rapport complet
python src/shtest_compiler/run_all.py \
  --input tests/ \
  --output reports/ \
  --excel rapport_$(date +%Y%m%d).xlsx
```

---

## Dépannage

### Erreurs Communes

#### Erreur de Syntaxe

```
[ERROR] Parse error in file: AST validation failed: Found orphaned action...
```

**Solution :** Vérifiez que chaque action est précédée d'un mot-clé `Étape:`.

#### Erreur de Validation

```
[ERROR] Validation failed: File is empty or contains no steps
```

**Solution :** Assurez-vous que le fichier contient au moins une étape complète.

#### Erreur de Plugin

```
[ERROR] Handler not found for action: action_inconnue
```

**Solution :** Vérifiez que l'action est définie dans `config/patterns_actions.yml`.

### Debug Avancé

#### Analyser les Tokens

```bash
# Activer le debug du lexer
export SHTEST_DEBUG=1
python src/shtest_compiler/compile_file.py test.shtest --debug
```

#### Vérifier l'AST

```python
from shtest_compiler.parser.configurable_parser import ConfigurableParser
import json

parser = ConfigurableParser(debug=True)
with open('test.shtest') as f:
    ast = parser.parse(f.read())

# Afficher la structure AST
print(json.dumps(ast.to_dict(), indent=2))
```

### Support

- **Documentation** : Consultez les autres sections de cette documentation
- **Tests d'exemple** : Explorez le dossier `tests/e2e/` pour des exemples
- **Logs de debug** : Utilisez le mode `--debug` pour des informations détaillées

---

## Conclusion

KnightBatch offre un framework puissant et flexible pour l'automatisation de tests. Ce manuel couvre les fonctionnalités essentielles et avancées. Pour plus d'informations :

- [Format SHTEST](shtest_format.md) - Syntaxe détaillée
- [Architecture Modulaire](modular_architecture.md) - Documentation technique
- [Guide Développeur](developer_quickstart.md) - Pour les contributeurs
- [Extension VS Code](vscode_extension.md) - Outils de développement