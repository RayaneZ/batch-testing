
# KnightBatch - Framework de Tests Automatisés

| <img src="/batch-testing/assets/logo.png" alt="KnightBatch" width="120" style="border-radius: 15px;"/> | Bienvenue dans la documentation de KnightBatch, le framework moderne pour l'automatisation de tests via des scénarios en langage naturel. Transformez vos procédures manuelles en tests automatisés robustes et maintenables. |
|  | --- |

##  Démarrage Rapide

```bash
# Installation
git clone <repository-url>
cd batch-testing
pip install -r src/requirements.txt

# Premier test
echo 'Étape: Test simple
Action: Créer le fichier ./test.txt
Résultat: le fichier existe' > mon_test.shtest

# Compilation et exécution
python src/shtest_compiler/compile_file.py mon_test.shtest
bash mon_test.sh
```

## Objectifs

- **Simplicité** : Écrire des tests en langage naturel, compréhensible par tous
- **Robustesse** : Validation automatique avec détection d'erreurs précise
- **Modularité** : Architecture extensible avec système de plugins YAML
- **Productivité** : Pipeline complet de compilation, validation et exécution
- **Intégration** : Support CI/CD et rapports automatisés

## ️ Architecture Modulaire

KnightBatch utilise une architecture moderne entièrement configurée par YAML :

- ** Core Modulaire** : Système de contexte partagé et gestion d'état
- ** Lexer Configurable** : Tokenisation basée sur patterns YAML
- ** Parser Flexible** : Grammaire extensible avec constructeur AST
- **⚙️ Compilateur YAML** : Génération de code via configuration
- ** Système de Plugins** : Handlers extensibles pour nouvelles actions
- ** Validation Robuste** : Vérification AST et sémantique automatique

##  Pipeline de Compilation

1. ** Tokenisation** : Le fichier `.shtest` est découpé en tokens via patterns YAML
2. ** Parsing** : Les tokens sont analysés pour produire un AST structuré
3. **️ Construction AST** : Validation et normalisation de la structure
4. ** Binding** : Liaison des validations aux actions et résolution du contexte
5. **⚙️ Génération** : Production de scripts shell exécutables via handlers
6. **▶️ Exécution** : Exécution directe des scripts générés

**Avantages** : Pipeline entièrement configurable, validation robuste, génération optimisée

##  Guide Complet

Pour un guide détaillé couvrant toutes les fonctionnalités, consultez le **[Manuel Utilisateur](user_manual.md)**.

### Exemple Rapide

```shtest
Étape: Préparation
Action: Créer le dossier ./demo
Résultat: le dossier est créé

Étape: Vérification
Action: Lister le dossier ./demo
Résultat: stdout contient demo
```

```bash
# Compilation
python src/shtest_compiler/compile_file.py example.shtest

# Exécution
bash example.sh
```

## Outils de Développement

### Extension VS Code
L'extension VS Code KnightBatch offre une expérience de développement intégrée :
- **Coloration syntaxique** complète pour les fichiers `.shtest`
- **Commandes intégrées** pour compilation, vérification et analyse
- **Snippets intelligents** pour accélérer l'écriture
- **IntelliSense** avec autocomplétion et validation en temps réel
- **Validation en temps réel** avec détection d'erreurs

[ Documentation Extension VS Code](vscode_extension.md)

## Système de Plugins

- Ajoutez facilement de nouveaux types de validations ou d'actions via le système de plugins Python.
- Voir [Créer un plugin](../creer_plugin.md) pour un guide étape par étape.

## Structure de la documentation

- **CLI** : Utilisation de l'interface en ligne de commande.
- **Configuration** : Paramétrage du système de test.
- **Format SHTEST** : Syntaxe standardisée des scénarios.
- **Architecture Modulaire** : Documentation technique de l'architecture.
- **Guide Développeur** : Guide de démarrage rapide pour développeurs.
- **Extension VS Code** : Documentation complète de l'extension.
- **Style Guide** : Recommandations rédactionnelles pour les scénarios.
- **Regex** : Détail des expressions régulières utilisées pour le parsing.
- **Tests et Validation** : Documentation des suites de test et validation d'erreurs.

---

Pour commencer, explorez la section sur le [format SHTEST](shtest_format.md) ou consultez les [regex](regex_documentation.md) de parsing. Pour les développeurs, découvrez l'[architecture modulaire](modular_architecture.md) et l'[extension VS Code](vscode_extension.md). Pour tester votre système, consultez la [documentation des tests](testing_and_validation.md).
