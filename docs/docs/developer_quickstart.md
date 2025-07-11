# Guide de Démarrage Rapide pour Développeurs

Ce guide vous aide à comprendre rapidement l'architecture modulaire de KnightBatch et à commencer à développer.

## Architecture en 5 Minutes

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Fichier       │    │   Lexer         │    │   Parser        │
│   .shtest       │───▶│   Modulaire     │───▶│   Modulaire     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐           │
│   Script        │    │   Compilateur   │◀──────────┘
│   Shell         │◀───│   Modulaire     │
└─────────────────┘    └─────────────────┘
```

## Composants Principaux

### 1. Core (`core/`)
- **visitor.py** : Pattern Visitor pour parcourir l'AST
- **ast.py** : Nœuds AST de base (ActionNode, ValidationNode, etc.)
- **context.py** : Contexte de compilation partagé

### 2. Lexer Modulaire (`parser/lexer/`)
- **configurable_lexer.py** : Lexer principal
- **pattern_loader.py** : Chargement des patterns YAML
- **filters.py** : Filtres de tokens
- **tokenizers.py** : Tokenizers spécialisés

### 3. Parser Modulaire (`parser/`)
- **configurable_parser.py** : Parser principal
- **ast_builder.py** : Constructeur d'AST
- **grammar.py** : Grammaire configurable

### 4. Compilateur Modulaire (`compiler/`)
- **compiler.py** : Compilateur principal
- **visitors/shell_visitor.py** : Générateur de code shell
- **matchers/** : Matchers pour les validations

## Exemple de Workflow Complet

```python
from shtest_compiler.core.context import CompileContext
from shtest_compiler.parser.lexer.configurable_lexer import ConfigurableLexer
from shtest_compiler.parser.configurable_parser import ConfigurableParser
from shtest_compiler.compiler.compiler import Compiler

# 1. Créer le contexte
context = CompileContext()

# 2. Configurer le lexer
lexer = ConfigurableLexer("config/patterns_hybrid.yml")

# 3. Configurer le parser
parser = ConfigurableParser("config/patterns_hybrid.yml")

# 4. Configurer le compilateur
compiler = Compiler(context)

# 5. Traiter un fichier
with open("test.shtest", "r") as f:
    content = f.read()

# Tokenisation
tokens = lexer.tokenize(content)

# Parsing
ast = parser.parse_tokens(tokens)

# Compilation
shell_script = compiler.compile(ast)
```

## Ajouter un Nouveau Matcher

```python
# 1. Créer la fonction matcher
def custom_matcher(validation_text: str) -> str:
    if "mon validation" in validation_text:
        return "custom_validation_type"
    return None

# 2. Enregistrer dans le contexte
context.add_matcher("custom_matcher", custom_matcher)

# 3. Ajouter dans le shell visitor
class CustomShellVisitor(ShellVisitor):
    def visit_custom_validation(self, node):
        return f"# Validation personnalisée: {node.validation}"
```

## Ajouter un Nouveau Type de Token

```yaml
# Dans config/patterns_hybrid.yml
tokens:
  custom_token:
    pattern: "MonPattern:\\s*(.+)"
    type: "CUSTOM_TOKEN"
    priority: 5
```

```python
# Dans le AST builder
class CustomASTBuilder(ASTBuilder):
    def build_custom_token(self, tokens):
        return CustomNode(tokens[0].value)
```

## Créer un Plugin

```python
# plugins/my_plugin.py
from shtest_compiler.core.context import CompileContext

def register_plugin(context: CompileContext):
    # Ajouter des matchers
    context.add_matcher("my_matcher", my_matcher_function)
    
    # Ajouter des visiteurs
    context.add_visitor("my_visitor", MyVisitor())
    
    # Ajouter des variables
    context.set_variable("MY_VAR", "my_value")

def my_matcher_function(validation_text: str) -> str:
    if "ma validation" in validation_text:
        return "my_validation_type"
    return None

class MyVisitor:
    def visit_my_validation(self, node):
        return f"echo 'Ma validation: {node.validation}'"
```

## Tests

### Tests Unitaires

```python
# tests/unit/test_my_feature.py
import pytest
from shtest_compiler.core.context import CompileContext

def test_my_matcher():
    context = CompileContext()
    context.add_matcher("my_matcher", my_matcher_function)
    
    result = context.get_matcher("my_matcher")("ma validation")
    assert result == "my_validation_type"
```

### Tests d'Intégration

```python
def test_full_pipeline():
    # Test complet du pipeline
    context = CompileContext()
    lexer = ConfigurableLexer("config/patterns_hybrid.yml")
    parser = ConfigurableParser("config/patterns_hybrid.yml")
    compiler = Compiler(context)
    
    content = "Action: test ; Résultat: success"
    tokens = lexer.tokenize(content)
    ast = parser.parse_tokens(tokens)
    result = compiler.compile(ast)
    
    assert "test" in result
    assert "success" in result
```

## Debug et Diagnostic

### Mode Debug

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Tous les composants loggent leurs actions
```

### Inspection de l'AST

```python
# Afficher l'AST
def print_ast(node, indent=0):
    print(" " * indent + str(node))
    if hasattr(node, 'children'):
        for child in node.children:
            print_ast(child, indent + 2)

print_ast(ast)
```

### Validation des Tokens

```python
# Vérifier la tokenisation
tokens = lexer.tokenize(content)
for token in tokens:
    print(f"{token.type}: {token.value}")
```

## Bonnes Pratiques

### 1. Séparation des Responsabilités
- **Lexer** : Seulement la tokenisation
- **Parser** : Seulement la construction d'AST
- **Compiler** : Seulement la génération de code

### 2. Configuration Externe
- Utilisez YAML pour les patterns et alias
- Évitez le code hardcodé dans les patterns

### 3. Extensibilité
- Créez des plugins pour les nouvelles fonctionnalités
- Utilisez le système de matchers pour les validations

### 4. Tests
- Testez chaque composant individuellement
- Testez l'intégration complète
- Utilisez des fixtures pour les données de test

## Problèmes Courants

### 1. Import Errors
```bash
# Solution : Vérifier le PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 2. Patterns Non Reconnus
```yaml
# Vérifier la priorité dans patterns_hybrid.yml
tokens:
  my_token:
    pattern: "MonPattern"
    priority: 1  # Priorité élevée
```

### 3. Matchers Non Appelés
```python
# Vérifier l'enregistrement dans le contexte
context.add_matcher("my_matcher", my_function)
```

## Ressources

- [Architecture Modulaire](modular_architecture.md) : Documentation complète
- [Configuration](configuration.md) : Guide de configuration
- [Format SHTEST](shtest_format.md) : Syntaxe des fichiers de test
- [Tests Unitaires](../tests/unit/) : Exemples de tests

---

Pour des questions spécifiques, consultez la [documentation complète](modular_architecture.md) ou les [tests unitaires](../tests/unit/). 