# Tests et Validation

Cette section documente les capacités de test et de validation de KnightBatch, incluant les suites de tests E2E, la validation d'erreurs, et les outils de diagnostic.

## Vue d'ensemble

KnightBatch dispose d'une suite de tests complète et d'un système de validation robuste pour garantir la qualité et la fiabilité du compilateur de tests.

## Structure des Tests

### Organisation des Tests

```
src/tests/
├── unit/           # Tests unitaires des modules individuels
├── integration/    # Tests d'intégration entre composants
├── e2e/           # Tests end-to-end avec fichiers .shtest
│   ├── ko/        # Tests négatifs (fichiers invalides)
│   └── ok/        # Tests positifs (fichiers valides)
└── legacy/        # Tests de compatibilité avec l'ancien format
```

### Types de Tests

#### Tests Unitaires
- **Objectif** : Valider le comportement des modules individuels
- **Couverture** : Parser, lexer, AST builder, compilateur, plugins
- **Exécution** : `python -m pytest tests/unit/`

#### Tests d'Intégration
- **Objectif** : Valider les interactions entre composants
- **Couverture** : Flux complet de parsing à génération de code
- **Exécution** : `python -m pytest tests/integration/`

#### Tests E2E (End-to-End)
- **Objectif** : Valider le comportement complet avec des fichiers réels
- **Couverture** : Compilation, génération de scripts, export Excel
- **Exécution** : `python tests/e2e/run_e2e_tests.py`

## Tests Négatifs (KO)

### Objectif
Les tests négatifs vérifient que le compilateur détecte et rejette correctement les fichiers invalides avec des messages d'erreur appropriés.

### Cas de Test Couverts

#### Syntaxe Invalide
- **Fichiers vides** : Détection des fichiers sans contenu
- **Fichiers commentaires uniquement** : Rejet des fichiers sans étapes
- **Actions orphelines** : Actions sans mot-clé `Étape:`
- **Actions malformées** : Actions vides ou incomplètes
- **Validations malformées** : Validations sans contenu ou invalides

#### Opérations Invalides
- **Chemins de fichiers invalides** : Caractères spéciaux, permissions
- **Opérations SQL invalides** : Requêtes malformées, tables inexistantes
- **Variables invalides** : Noms incorrects, assignations vides
- **Plugins inexistants** : Références à des plugins non disponibles

#### Structure Invalide
- **Imbrication incorrecte** : Étapes dans des étapes
- **Validations conflictuelles** : Validations contradictoires
- **Encodage invalide** : Caractères non-UTF8

### Exécution des Tests Négatifs

```bash
# Exécuter tous les tests négatifs
python tests/e2e/ko/run_ko_tests.py

# Tester un fichier spécifique
python -m shtest_compiler.run_all --input tests/e2e/ko/invalid_syntax_1.shtest
```

### Critères de Succès
Un test négatif est réussi si :
- Le compilateur détecte l'erreur et affiche un message clair
- Aucun script shell n'est généré (ou le script généré échoue)
- Le processus se termine avec un code de sortie non-zéro
- Le message d'erreur est utile et pointe vers le problème spécifique

## Validation d'Erreurs

### Système de Validation AST

Le compilateur utilise un système de validation AST pour détecter les erreurs structurelles et sémantiques.

#### Validateurs Disponibles

```python
# Validation des étapes
def _validate_steps(self, ast: ShtestFile) -> List[str]:
    """Valide que les étapes ont une structure appropriée."""
    
# Validation des actions
def _validate_actions(self, ast: ShtestFile) -> List[str]:
    """Valide que les actions ont une structure appropriée."""
    
# Validation des fichiers non-vides
def _validate_nonempty_file(self, ast: ShtestFile) -> List[str]:
    """Valide que le fichier n'est pas vide."""
    
# Validation des commandes d'action
def _validate_action_commands(self, ast: ShtestFile) -> List[str]:
    """Valide que les actions ont des commandes non-vides et significatives."""
    
# Validation des phrases de validation
def _validate_validation_phrases(self, ast: ShtestFile) -> List[str]:
    """Valide que les phrases de validation sont bien formées."""
    
# Validation des actions orphelines
def _validate_no_orphaned_actions(self, ast: ShtestFile) -> List[str]:
    """Valide qu'il n'y a pas d'actions orphelines."""
```

### Messages d'Erreur

Le système génère des messages d'erreur clairs et localisés :

```
AST validation failed: 
- File is empty or contains no steps
- Step 'Test Step' has no actions
- Action 2 in step 'Test Step' has empty or comment-only command
- Found orphaned action without proper step context
```

### Gestion des Erreurs

#### Propagation des Erreurs
1. **Parser** : Détecte les erreurs de syntaxe et lève `ParseError`
2. **AST Builder** : Valide la structure et lève `ParseError` sur échec
3. **CLI** : Capture les erreurs et affiche les messages appropriés
4. **Code de Sortie** : Retourne un code non-zéro en cas d'erreur

#### Codes de Sortie
- **0** : Succès
- **1** : Erreur de validation ou de compilation
- **2** : Erreur de configuration
- **3** : Erreur système

## Outils de Diagnostic

### Script de Debug

Le script `debug_parser.py` permet d'analyser le comportement du parser :

```bash
python tests/e2e/ko/debug_parser.py
```

#### Fonctionnalités
- **Analyse des tokens** : Affichage des tokens générés
- **Structure AST** : Visualisation de l'arbre syntaxique
- **Validation** : Test des validateurs sur des fichiers spécifiques
- **Comparaison** : Test des parsers legacy et modulaire

### Mode Debug

Activer le mode debug pour des informations détaillées :

```bash
python -m shtest_compiler.run_all --input file.shtest --debug
```

#### Informations Disponibles
- **Tokens générés** : Détail de la tokenisation
- **Étapes de parsing** : Progression du parsing
- **Validations** : Résultats des validations AST
- **Erreurs détaillées** : Stack traces et contexte

## Tests SQL Avancés

### Comparaison de Résultats

KnightBatch supporte la comparaison avancée de résultats SQL :

```shtest
Étape: Comparer les résultats de deux requêtes
  Action: Exécuter la requête SQL: SELECT * FROM users WHERE active = 1
  Action: Exporter les résultats vers: results1.xlsx
  Action: Exécuter la requête SQL: SELECT * FROM users WHERE status = 'active'
  Action: Exporter les résultats vers: results2.xlsx
  Action: Comparer les résultats de la requête results1.xlsx avec results2.xlsx (ignorer l'ordre lors de la comparaison)
  Vérifier: Les résultats sont identiques
```

### Fonctionnalités
- **Export Excel** : Export automatique des résultats SQL
- **Comparaison flexible** : Support de l'ignorance d'ordre
- **Tolérance** : Gestion des différences mineures
- **Validation** : Intégration avec le système de validation

## Intégration CI/CD

### Exécution Automatisée

```yaml
# Exemple GitHub Actions
- name: Run KnightBatch Tests
  run: |
    python -m shtest_compiler.run_all --input tests/
    python tests/e2e/ko/run_ko_tests.py
    python tests/e2e/run_e2e_tests.py
```

### Critères de Qualité
- **Tous les tests positifs passent** : Validation du comportement attendu
- **Tous les tests négatifs échouent** : Validation de la gestion d'erreurs
- **Couverture de code** : Tests unitaires pour tous les modules
- **Performance** : Temps d'exécution acceptable

## Bonnes Pratiques

### Écriture de Tests
1. **Tests positifs** : Un test par fonctionnalité
2. **Tests négatifs** : Un test par type d'erreur
3. **Tests d'intégration** : Validation des flux complets
4. **Documentation** : Commentaires clairs sur l'intention

### Validation
1. **Messages d'erreur** : Clairs et actionnables
2. **Localisation** : Indication précise de l'erreur
3. **Codes de sortie** : Appropriés pour l'automatisation
4. **Performance** : Validation rapide même sur gros fichiers

### Maintenance
1. **Mise à jour régulière** : Ajout de tests pour nouvelles fonctionnalités
2. **Révision des erreurs** : Amélioration des messages d'erreur
3. **Documentation** : Mise à jour de la documentation des tests
4. **Performance** : Optimisation des temps d'exécution 