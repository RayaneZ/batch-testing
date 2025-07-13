# Changelog

Ce document liste les améliorations et nouvelles fonctionnalités apportées à KnightBatch.

## [2.0.0] - 2025-01-13

### 🛡️ Validation Robuste et Gestion d'Erreurs

#### Nouveau Système de Validation AST
- **Validateurs intégrés** pour détecter les erreurs structurelles et sémantiques
- **Messages d'erreur clairs** avec localisation précise des problèmes
- **Codes de sortie standardisés** pour l'intégration CI/CD
- **Validation en temps réel** pendant le parsing

#### Types d'Erreurs Détectées
- ✅ Fichiers vides ou contenant seulement des commentaires
- ✅ Actions orphelines (sans mot-clé `Étape:`)
- ✅ Actions malformées (commandes vides ou invalides)
- ✅ Validations incomplètes ou malformées
- ✅ Structure invalide (imbrication incorrecte)
- ✅ Variables malformées ou invalides
- ✅ Opérations SQL invalides
- ✅ Chemins de fichiers invalides

#### Amélioration de la Gestion d'Erreurs
- **Propagation d'erreurs** : Les erreurs remontent correctement jusqu'au CLI
- **Sortie d'erreur structurée** : Messages formatés pour stderr
- **Codes de sortie appropriés** : 0=succès, 1=erreur validation, 2=erreur config, 3=erreur système
- **Debugging intégré** : Mode debug avec informations détaillées

### 🧪 Suite de Tests E2E Complète

#### Organisation des Tests
```
src/tests/
├── unit/           # Tests unitaires des modules individuels
├── integration/    # Tests d'intégration entre composants
├── e2e/           # Tests end-to-end avec fichiers .shtest
│   ├── ko/        # Tests négatifs (fichiers invalides)
│   └── ok/        # Tests positifs (fichiers valides)
└── legacy/        # Tests de compatibilité avec l'ancien format
```

#### Tests Négatifs (KO)
- **13 fichiers de test invalides** couvrant tous les cas d'erreur
- **Test runner automatisé** (`run_ko_tests.py`)
- **Validation des messages d'erreur** et codes de sortie
- **Documentation complète** des cas de test

#### Tests Positifs (OK)
- **Tests de fonctionnalités** avec fichiers valides
- **Tests SQL avancés** avec comparaison de résultats
- **Tests d'intégration** entre composants
- **Validation du comportement attendu**

#### Outils de Test
- **Script de debug** (`debug_parser.py`) pour analyser le parsing
- **Test runner E2E** (`run_e2e_tests.py`) pour la suite complète
- **Tests unitaires** avec pytest
- **Tests d'intégration** automatisés

### 🔧 Améliorations Techniques

#### Architecture Modulaire
- **Parser configurable** avec validation intégrée
- **AST Builder** avec système de validateurs extensible
- **Compilateur modulaire** avec gestion d'erreurs robuste
- **Système de plugins** amélioré

#### CLI Amélioré
- **Gestion des fichiers uniques** vs répertoires
- **Validation en temps réel** avec messages clairs
- **Mode debug** avec logs détaillés
- **Codes de sortie** appropriés pour l'automatisation

#### SQL Avancé
- **Comparaison de résultats** avec export Excel
- **Gestion de l'ordre** (ignorer l'ordre lors de la comparaison)
- **Tolérance** pour les différences mineures
- **Validation intégrée** avec le système de tests

### 📚 Documentation Complète

#### Nouvelle Documentation
- **Guide de tests et validation** (`testing_and_validation.md`)
- **Changelog** détaillé des améliorations
- **Documentation CLI** mise à jour avec gestion d'erreurs
- **Guide développeur** enrichi avec exemples de tests

#### Améliorations de la Documentation
- **Exemples pratiques** pour tous les cas d'usage
- **Troubleshooting** avec messages d'erreur courants
- **Bonnes pratiques** pour l'écriture de tests
- **Intégration CI/CD** documentée

### 🚀 Fonctionnalités Nouvelles

#### Validation en Temps Réel
- **Détection immédiate** des erreurs de syntaxe
- **Messages contextuels** avec localisation précise
- **Suggestions de correction** pour les erreurs courantes

#### Outils de Diagnostic
- **Debug parser** pour analyser le comportement
- **Inspection AST** avec visualisation de la structure
- **Validation des tokens** avec affichage détaillé

#### Intégration CI/CD
- **Codes de sortie** appropriés pour l'automatisation
- **Tests automatisés** pour validation continue
- **Documentation** des bonnes pratiques d'intégration

## [1.x.x] - Versions Précédentes

### Fonctionnalités de Base
- Architecture modulaire avec lexer, parser et compilateur
- Support des fichiers `.shtest` avec syntaxe en langage naturel
- Génération de scripts shell exécutables
- Export Excel des scénarios de test
- Extension VS Code avec coloration syntaxique
- Système de plugins extensible

### Composants Principaux
- Parser configurable avec patterns YAML
- AST Builder avec nœuds spécialisés
- Compilateur modulaire avec visiteurs
- Matchers pour validations personnalisées
- Support SQL avec drivers multiples

---

## Migration Guide

### Pour les Utilisateurs Existants
1. **Aucun changement requis** pour les fichiers `.shtest` valides
2. **Validation automatique** : Les erreurs sont maintenant détectées et signalées
3. **Messages d'erreur améliorés** : Diagnostic plus précis des problèmes
4. **Codes de sortie** : Vérifiez les scripts d'automatisation

### Pour les Développeurs
1. **Tests obligatoires** : Ajoutez des tests pour les nouvelles fonctionnalités
2. **Validation** : Utilisez le système de validation AST pour les nouveaux composants
3. **Gestion d'erreurs** : Respectez les codes de sortie et messages d'erreur
4. **Documentation** : Mettez à jour la documentation pour les nouvelles fonctionnalités

### Pour les Intégrations CI/CD
1. **Codes de sortie** : Utilisez les nouveaux codes de sortie pour la détection d'erreurs
2. **Tests automatisés** : Intégrez la suite de tests E2E dans vos pipelines
3. **Validation** : Utilisez la validation en temps réel pour la qualité du code
4. **Reporting** : Exploitez les messages d'erreur structurés pour les rapports 