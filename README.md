<p align="center" style="background:#fff">
  <img src="logo.png" alt="KnightBatch logo" width="200"/>
</p>

# KnightBatch - Shell Test Compiler

Ce projet permet de convertir des scénarios `.shtest` en scripts shell exécutables.  
Il comprend une CLI Python et une extension VS Code pour l'écriture de scénarios compréhensibles de type "Action / Résultat".

**Nouveau : Architecture modulaire avec système de plugins pour une extensibilité maximale !**

---

## 🚀 Installation

Assurez-vous d'avoir Python 3.8 ou supérieur.

```bash
python -m venv venv
source venv/bin/activate  # ou `venv\Scripts\activate` sous Windows

pip install -e .
```

> Cela installe la commande `shtest` accessible dans le terminal.

---

## 🛠 Commandes principales

### `shtest.py` - Compilateur Principal (Nouveau)

Le compilateur principal utilise l'architecture modulaire pour convertir les fichiers `.shtest` :

```bash
# Compiler un fichier .shtest
python shtest.py tests/example.shtest

# Compiler avec sortie personnalisée
python shtest.py tests/example.shtest --output output/script.sh

# Mode debug pour voir les détails de compilation
python shtest.py tests/example.shtest --debug
```

---

## 🏗 Architecture Modulaire

KnightBatch utilise une architecture modulaire moderne :

```
┌─────────────────────────────────────────────────────────────┐
│                    Interface Utilisateur                    │
│  (CLI, VS Code Extension, API)                             │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Compilateur Modulaire                    │
│  (Visiteurs spécialisés, générateurs de code)              │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Parser Modulaire                        │
│  (Grammaire configurable, constructeur AST)                │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Lexer Modulaire                         │
│  (Tokenisation configurable, patterns, filtres)            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                         Core                                │
│  (Pattern Visitor, AST nodes, contexte)                    │
└─────────────────────────────────────────────────────────────┘
```

### Composants Principaux

- **Core** : Pattern Visitor, nœuds AST de base, contexte de compilation partagé
- **Lexer Modulaire** : Tokenisation configurable avec patterns et filtres
- **Parser Modulaire** : Grammaire configurable avec constructeur AST
- **Compilateur Modulaire** : Visiteurs spécialisés et générateurs de code
- **Système de Plugins** : Matchers extensibles pour nouvelles validations

---

## 📁 Structure des dossiers

```
src/
├── shtest_compiler/
│   ├── core/                    # Fondations (Visitor, AST, Context)
│   ├── parser/
│   │   ├── lexer/              # Lexer modulaire
│   │   └── ...                 # Parser modulaire
│   ├── compiler/               # Compilateur modulaire
│   ├── config/                 # Configuration YAML
│   ├── plugins/                # Système de plugins
│   ├── shtest.py              # Compilateur principal
│   └── ...
tests/
├── new/                       # Tests avec nouvelle architecture
├── legacy/                    # Tests legacy
└── unit/                      # Tests unitaires
output/
```

---

## 🧪 Exemple de scénario `.shtest`

```text
Etape: Step 1 - Preparation
Action: Creer le dossier ./qualification/demo_env
Resultat: le dossier est cree.

Action: Creer le fichier ./qualification/demo_env/initial.txt ; Resultat: le fichier est cree.

Action: Définir la variable SQL_CONN = rootme/ffDDD584R@base_name ; Résultat: Les identifiants sont configurés.


Etape: Step 2 - Ancien fichier
Action: toucher le fichier ./qualification/demo_env/old.txt -t 202201010000 ; Resultat: date modifiee.


Etape: Step 3 - Nouveau fichier
Action: Creer le fichier ./qualification/demo_env/newfile.txt ; Resultat: fichier cree.
Action: Mettre a jour la date du fichier ./qualification/demo_env/newfile.txt 202401010101 ; Resultat: date modifiee.


Etape: Step 4 - Execution du batch
Action: Exécuter ./qualification/purge.sh ; Résultat: Le script retourne un code 0 et (la sortie standard contient "Succès complet" ou la sortie d'erreur contient WARNING).
Action: Exécuter /opt/batch/migration.sh ; Résultat: Le script retourne un code 0.


Step: Step 5 - Vérifier la table en base
Action: Exécuter le script SQL verification.sql ; Résultat: Le script s'execute avec succès.
Action: Comparer le fichier ./output.txt avec ./output_attendu.txt; Résultat: Les fichiers sont identiques
```

---

## ⚙️ Configuration

### Fichier config.ini

```ini
[application]
input_dir = demo_env
output_dir = demo_env
sql_driver = oracle
config_path = config/patterns_hybrid.yml
aliases_path = config/aliases.yml
plugin_path = plugins/
debug = false
```

### Configuration YAML

Les patterns et alias sont configurés via des fichiers YAML :

- `config/patterns_hybrid.yml` : Patterns de reconnaissance et grammaire
- `config/aliases.yml` : Alias en langage naturel

---

## 🔌 Système de Plugins

Créez des plugins pour étendre les fonctionnalités :

```python
# plugins/my_plugin.py
from shtest_compiler.core.context import CompileContext

def register_plugin(context: CompileContext):
    context.add_matcher("my_matcher", my_matcher_function)
    context.add_visitor("my_visitor", MyVisitor())

def my_matcher_function(validation_text: str) -> str:
    if "ma validation" in validation_text:
        return "my_validation_type"
    return None
```

---

## Plugin Handler Requirements

Each plugin (and the core) can provide a `handler_requirements.yml` file in its `config/` directory. This YAML file documents the expected parameters and requirements for each handler.

- Example location: `src/shtest_compiler/plugins/my_plugin/config/handler_requirements.yml`
- Example format:

```yaml
create_example_file:
  description: "Creates an example file in the target directory."
  params:
    - name: target_dir
      type: str
      required: false
      default: '.'
      description: "Directory where the example file will be created."
```

### How it works
- The loader automatically discovers and merges all `handler_requirements.yml` files from core and plugins.
- You can access the merged requirements dictionary in Python:

```python
from shtest_compiler.command_loader import get_handler_requirements
requirements = get_handler_requirements()
# requirements is a dict keyed by handler name
```

This makes it easy to document, validate, or inspect handler requirements across your system.

---

## 🧪 Tests

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
```

### Tests d'Intégration

```bash
# Test avec des fichiers .shtest réels
python shtest.py tests/new/example.shtest
```

---

## 📚 Documentation

- [Documentation complète](docs/) : Guide utilisateur et technique
- [Architecture modulaire](docs/docs/modular_architecture.md) : Documentation technique
- [Guide développeur](docs/docs/developer_quickstart.md) : Démarrage rapide
- [Configuration](docs/docs/configuration.md) : Guide de configuration

---

## 🧩 VS Code Extension

Le dossier `vscode/` contient une extension minimale pour `.shtest`.  
Pour l'installer :

```bash
cd vscode
npm install
npx vsce package
```

Puis installe le `.vsix` dans Visual Studio Code.

---

## 📄 License

Ce projet est publié sous licence MIT.
