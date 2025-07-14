# Architecture Modulaire

Cette page documente l'architecture modulaire de KnightBatch, conçue pour offrir une extensibilité maximale et une séparation claire des responsabilités.

## Vue d'ensemble

L'architecture modulaire de KnightBatch est organisée en plusieurs couches :

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

## Pipeline de Compilation

1. **Tokenisation** : Le fichier `.shtest` est découpé en tokens par le lexer configurable.
2. **Parsing** : Les tokens sont analysés par le parser modulaire pour produire un AST (arbre syntaxique).
3. **Construction de l'AST** : L'AST builder valide et normalise la structure.
4. **Binding** :
   - Le binder relie chaque validation à la bonne action (notamment pour `scope: last_action`).
   - Résout les variables et le contexte.
   - Prépare l'AST pour la génération de code.
   - **Pourquoi c'est important ?** Sans binding, certaines validations seraient orphelines ou mal appliquées, ce qui fausserait les résultats des tests.
5. **Génération de code** : Le générateur de shell parcourt l'AST lié et produit un script shell exécutable.
6. **Exécution** : Le script shell généré peut être exécuté directement.

### Détail du Binding

Le **binding** est une étape clé qui garantit la cohérence logique du scénario :
- Associe chaque validation à la bonne action (surtout pour les validations locales)
- Résout les références de variables et de contexte
- Détecte et signale les validations orphelines ou mal placées
- Prépare l'AST pour une génération de code fiable

**Exemple : sans binding, une validation `stdout contient OK` pourrait être appliquée à la mauvaise action, ou rester sans effet.**

## Core - Fondations

### Pattern Visitor

Le pattern Visitor est implémenté dans `core/visitor.py` et permet de parcourir l'AST de manière extensible :

```python
from shtest_compiler.core.visitor import Visitor

class MyVisitor(Visitor):
    def visit_action_node(self, node):
        # Traitement personnalisé pour les nœuds d'action
        pass

    def visit_validation_node(self, node):
        # Traitement personnalisé pour les nœuds de validation
        pass
```

### Nœuds AST

Les nœuds AST de base sont définis dans `core/ast.py` :

- `ActionNode` : Représente une action à exécuter
- `ValidationNode` : Représente une validation à effectuer
- `FileNode` : Représente une opération sur fichier
- `VariableNode` : Représente une variable
- `SQLNode` : Représente une opération SQL

### Contexte de Compilation

Le `CompileContext` dans `core/context.py` maintient l'état global pendant la compilation :

```python
from shtest_compiler.core.context import CompileContext

context = CompileContext()
context.set_variable("SQL_DRIVER", "mysql")
context.add_matcher("custom_matcher", my_matcher_function)
```

## Lexer Modulaire

### Architecture

Le lexer modulaire est organisé dans `parser/lexer/` :

- `core.py` : Interfaces et types de base
- `configurable_lexer.py` : Lexer principal configurable
- `pattern_loader.py` : Chargement des patterns depuis YAML
- `filters.py` : Filtres de tokens
- `tokenizers.py` : Tokenizers spécialisés

### Configuration

Les patterns sont définis dans `config/patterns_hybrid.yml` :

```yaml
tokens:
  action:
    pattern: "Action:\\s*(.+)"
    type: "ACTION"
  validation:
    pattern: "Résultat:\\s*(.+)"
    type: "VALIDATION"
```

### Utilisation

```python
from shtest_compiler.parser.lexer.configurable_lexer import ConfigurableLexer

lexer = ConfigurableLexer("config/patterns_hybrid.yml")
tokens = lexer.tokenize("Action: test ; Résultat: success")
```

## Parser Modulaire

### Architecture

Le parser modulaire est organisé dans `parser/` :

- `configurable_parser.py` : Parser principal
- `ast_builder.py` : Constructeur d'AST configurable
- `grammar.py` : Grammaire configurable
- `core.py` : Interfaces de base

### Grammaire Configurable

La grammaire est définie dans `config/patterns_hybrid.yml` :

```yaml
grammar:
  rules:
    - name: "action_validation"
      pattern: "action:validation"
      builder: "action_validation_builder"
```

### Constructeur AST

```python
from shtest_compiler.parser.ast_builder import ASTBuilder

class CustomASTBuilder(ASTBuilder):
    def build_action_validation(self, action_tokens, validation_tokens):
        # Construction personnalisée d'un nœud action-validation
        return ActionValidationNode(action_tokens, validation_tokens)
```

## Compilateur Modulaire

### Architecture

Le compilateur modulaire est organisé dans `compiler/` :

- `compiler.py` : Compilateur principal
- `visitors/` : Visiteurs spécialisés
- `matchers/` : Matchers pour les validations
- `shell_generator.py` : Générateur de code shell

### Visiteurs Spécialisés

```python
from shtest_compiler.compiler.visitors.shell_visitor import ShellVisitor

class CustomShellVisitor(ShellVisitor):
    def visit_action_node(self, node):
        # Génération personnalisée de code shell
        return f"custom_action '{node.action}'"
```

### Matchers

Les matchers sont des fonctions qui reconnaissent des patterns de validation :

```python
def sql_matcher(validation_text):
    if "base prête" in validation_text:
        return "sql_ready"
    return None

# Enregistrement du matcher
context.add_matcher("sql_matcher", sql_matcher)
```

## Système de Plugins

### Architecture des Plugins

Les plugins sont organisés dans `plugins/` et peuvent étendre :

- **Matchers** : Nouvelles validations
- **Tokenizers** : Nouveaux types de tokens
- **Visitors** : Nouveaux générateurs de code
- **AST Builders** : Nouveaux constructeurs d'AST

### Création d'un Plugin

```python
# plugins/custom_plugin.py
from shtest_compiler.core.context import CompileContext

def register_plugin(context: CompileContext):
    # Enregistrer de nouveaux matchers
    context.add_matcher("custom_validation", custom_validation_matcher)

    # Enregistrer de nouveaux visiteurs
    context.add_visitor("custom_generator", CustomGenerator())
```

### Chargement des Plugins

```python
from shtest_compiler.plugins import load_plugins

context = CompileContext()
load_plugins(context)
```

## Handler Requirements Documentation

Each handler (action or validation) can have its requirements documented in a `handler_requirements.yml` file in the `config/` directory of the core or any plugin.

- The loader merges all these YAMLs into a single requirements dictionary.
- This allows for automatic documentation, validation, and introspection of handler parameters.

**Example:**
```yaml
example_handler:
  description: "Does something."
  params:
    - name: foo
      type: str
      required: true
      description: "A required parameter."
```

**Access in code:**
```python
from shtest_compiler.command_loader import get_handler_requirements
reqs = get_handler_requirements()
```

## Configuration Avancée

### Fichiers de Configuration

- `config/patterns_hybrid.yml` : Patterns et grammaire
- `config/aliases.yml` : Alias en langage naturel
- `config.ini` : Configuration globale

### Variables d'Environnement

- `SHTEST_CONFIG_PATH` : Chemin vers les fichiers de configuration
- `SHTEST_PLUGIN_PATH` : Chemin vers les plugins
- `SHTEST_DEBUG` : Mode debug (1 pour activer)

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
```

### Tests d'Intégration

```bash
# Exécuter tous les scripts shell générés
for test in tests/integration/*.sh; do
    bash "$test"
done
```