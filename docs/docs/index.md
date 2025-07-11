
# Scénarios de Test

| <img src="assets/logo.png" alt="KnightBatch" width="120" style="border-radius: 15px;"/> | Bienvenue dans la documentation des scénarios de test automatisés. Ce site documente l'ensemble des règles, formats et procédures utilisés pour décrire, exécuter et valider des scénarios techniques via des instructions en langage naturel. |
| :--: | --- |

## Objectifs

- Faciliter l'écriture de scénarios lisibles par les humains et interprétables par des outils automatisés.
- Définir une grammaire structurée à base de **regex** pour reconnaître les actions, fichiers, variables et validations attendues.
- Fournir une référence claire pour tous les contributeurs (dev, QA, ops).
- Architecture modulaire extensible avec système de plugins pour personnaliser le comportement.

## Architecture Modulaire

KnightBatch utilise une architecture modulaire moderne avec :

- **Core** : Pattern Visitor, nœuds AST de base, contexte de compilation partagé
- **Lexer Modulaire** : Tokenisation configurable avec patterns et filtres
- **Parser Modulaire** : Grammaire configurable avec constructeur AST
- **Compilateur Modulaire** : Visiteurs spécialisés et générateurs de code
- **Système de Plugins** : Matchers extensibles pour nouvelles validations

## Outils de Développement

### Extension VS Code
L'extension VS Code KnightBatch offre une expérience de développement intégrée :
- **Coloration syntaxique** complète pour les fichiers `.shtest`
- **Commandes intégrées** pour compilation, vérification et analyse
- **Snippets intelligents** pour accélérer l'écriture
- **IntelliSense** avec autocomplétion et validation en temps réel

[📖 Documentation Extension VS Code](vscode_extension.md)

## Structure de la documentation

- **CLI** : Utilisation de l'interface en ligne de commande.
- **Configuration** : Paramétrage du système de test.
- **Format SHTEST** : Syntaxe standardisée des scénarios.
- **Architecture Modulaire** : Documentation technique de l'architecture.
- **Guide Développeur** : Guide de démarrage rapide pour développeurs.
- **Extension VS Code** : Documentation complète de l'extension.
- **Style Guide** : Recommandations rédactionnelles pour les scénarios.
- **Regex** : Détail des expressions régulières utilisées pour le parsing.

---

Pour commencer, explorez la section sur le [format SHTEST](shtest_format.md) ou consultez les [regex](regex_documentation.md) de parsing. Pour les développeurs, découvrez l'[architecture modulaire](modular_architecture.md) et l'[extension VS Code](vscode_extension.md).
