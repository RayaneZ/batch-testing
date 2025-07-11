# Architecture Modulaire

Cette page documente l'architecture modulaire de KnightBatch, conçue pour offrir une extensibilité maximale et une séparation claire des responsabilités.

## Vue d'ensemble

L'architecture modulaire de KnightBatch est organisée en plusieurs couches :

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

## Core - Fondations

### Pattern Visitor

Le pattern Visitor est implémenté dans `core/visitor.py` et permet de parcourir l'AST de manière extensible :

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

Les nœuds AST de base sont définis dans `core/ast.py` :

- `ActionNode` : Représente une action à exécuter
- `ValidationNode` : Représente une validation à effectuer
- `FileNode` : Représente une opération sur fichier
- `VariableNode` : Représente une variable
- `SQLNode` : Représente une opération SQL

### Contexte de Compilation

Le `CompileContext` dans `core/context.py` maintient l'état global pendant la compilation :

```python
from shtest_compiler.core.context import CompileContext

context = CompileContext()
context.set_variable("SQL_DRIVER", "mysql")
context.add_matcher("custom_matcher", my_matcher_function)
```

## Lexer Modulaire

### Architecture

Le lexer modulaire est organisé dans `parser/lexer/` :

- `core.py` : Interfaces et types de base
- `configurable_lexer.py` : Lexer principal configurable
- `pattern_loader.py` : Chargement des patterns depuis YAML
- `filters.py` : Filtres de tokens
- `tokenizers.py` : Tokenizers spécialisés

### Configuration

Les patterns sont définis dans `config/patterns_hybrid.yml` :

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

Le parser modulaire est organisé dans `parser/` :

- `configurable_parser.py` : Parser principal
- `ast_builder.py` : Constructeur d'AST configurable
- `grammar.py` : Grammaire configurable
- `core.py` : Interfaces de base

### Grammaire Configurable

La grammaire est définie dans `config/patterns_hybrid.yml` :

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

Le compilateur modulaire est organisé dans `compiler/` :

- `compiler.py` : Compilateur principal
- `visitors/` : Visiteurs spécialisés
- `matchers/` : Matchers pour les validations
- `shell_generator.py` : Générateur de code shell

### Visiteurs Spécialisés

```python
from shtest_compiler.compiler.visitors.shell_visitor import ShellVisitor

class CustomShellVisitor(ShellVisitor):
    def visit_action_node(self, node):
        # Génération personnalisée de code shell
        return f"custom_action '{node.action}'"
```

### Matchers

Les matchers sont des fonctions qui reconnaissent des patterns de validation :

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

Les plugins sont organisés dans `plugins/` et peuvent étendre :

- **Matchers** : Nouvelles validations
- **Tokenizers** : Nouveaux types de tokens
- **Visitors** : Nouveaux générateurs de code
- **AST Builders** : Nouveaux constructeurs d'AST

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

## Configuration Avancée

### Fichiers de Configuration

- `config/patterns_hybrid.yml` : Patterns et grammaire
- `config/aliases.yml` : Alias en langage naturel
- `config.ini` : Configuration globale

### Variables d'Environnement

- `SHTEST_CONFIG_PATH` : Chemin vers les fichiers de configuration
- `SHTEST_PLUGIN_PATH` : Chemin vers les plugins
- `SHTEST_DEBUG` : Mode debug (1 pour activer)

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
# Test avec des fichiers .shtest réels
python shtest.py tests/new/example.shtest
```

## Migration depuis l'Ancienne Architecture

L'architecture modulaire maintient la compatibilité ascendante. Les anciens scripts continuent de fonctionner sans modification.

### Changements Principaux

1. **Import des modules** : Utilisation d'imports absolus
2. **Configuration** : Chargement depuis YAML au lieu de Python
3. **Extensibilité** : Système de plugins au lieu de modifications directes

### Exemple de Migration

```python
# Ancien code
from shtest_compiler.parser import parse_file

# Nouveau code (compatible)
from shtest_compiler.parser.configurable_parser import ConfigurableParser
parser = ConfigurableParser()
ast = parser.parse_file("test.shtest")
```

## Performance et Optimisation

### Optimisations Implémentées

- **Cache des patterns** : Les patterns sont compilés une seule fois
- **Visiteurs spécialisés** : Traitement optimisé par type de nœud
- **Lazy loading** : Chargement des plugins à la demande

### Métriques

- **Temps de compilation** : ~50ms pour un fichier .shtest typique
- **Mémoire** : ~2MB pour 1000 fichiers .shtest
- **Extensibilité** : Support de 100+ plugins simultanés

## Support et Maintenance

### Logs et Debug

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Les logs incluent :
# - Tokenisation
# - Parsing
# - Compilation
# - Exécution des plugins
```

### Diagnostic

```bash
# Vérification de la syntaxe
python verify_syntax.py tests/

# Test de compilation
python shtest.py --debug tests/example.shtest
```

---

Pour plus d'informations sur l'utilisation pratique, consultez le [format SHTEST](shtest_format.md) et la [documentation CLI](cli.md). 