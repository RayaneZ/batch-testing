# Extension VS Code

Cette page documente l'extension VS Code pour KnightBatch, qui fournit un support complet pour l'édition et la compilation de fichiers `.shtest`.

## Vue d'ensemble

L'extension VS Code KnightBatch offre une expérience de développement intégrée pour créer, éditer et compiler des scénarios de test `.shtest`. Elle supporte la nouvelle architecture modulaire et maintient la compatibilité avec les anciens patterns.

### Fonctionnalités Principales

- ** Coloration syntaxique** : Support complet pour tous les éléments `.shtest`
- **⚡ Commandes intégrées** : Compilation, vérification, visualisation AST
- ** Snippets intelligents** : Templates pour patterns courants
- **⚙️ Configuration flexible** : Paramètres personnalisables
- ** IntelliSense** : Autocomplétion et validation en temps réel

## Installation

### Depuis le Marketplace VS Code

1. Ouvrez VS Code
2. Allez dans Extensions (Ctrl+Shift+X)
3. Recherchez "KnightBatch"
4. Cliquez sur "Installer"

### Depuis un fichier VSIX

1. Téléchargez le fichier `.vsix` depuis les releases
2. Dans VS Code, allez dans Extensions (Ctrl+Shift+X)
3. Cliquez sur "..." et sélectionnez "Installer depuis VSIX..."
4. Sélectionnez le fichier téléchargé

### Depuis les sources

```bash
cd vscode
npm install
npm run compile
npx vsce package
```

Puis installez le fichier `.vsix` généré.

## Commandes Disponibles

### Compilation

#### KnightBatch: Compile Current File
Compile le fichier `.shtest` actuellement ouvert en script shell.

**Utilisation :**
- Ouvrez un fichier `.shtest`
- Appuyez sur Ctrl+Shift+P
- Tapez "KnightBatch: Compile Current File"
- Le script shell sera généré dans le dossier de sortie configuré

**Résultat :**
- Script shell généré dans le dossier de sortie
- Ouverture automatique du fichier généré
- Message de confirmation ou d'erreur

#### KnightBatch: Compile Directory
Compile tous les fichiers `.shtest` du workspace.

**Utilisation :**
- Clic droit sur un dossier dans l'explorateur
- Sélectionnez "KnightBatch: Compile Directory"
- Ou utilisez la palette de commandes

**Résultat :**
- Tous les fichiers `.shtest` sont compilés
- Rapport du nombre de fichiers traités

### Vérification

#### KnightBatch: Verify Syntax
Vérifie la syntaxe du fichier `.shtest` actuel.

**Utilisation :**
- Ouvrez un fichier `.shtest`
- Appuyez sur Ctrl+Shift+P
- Tapez "KnightBatch: Verify Syntax"

**Résultat :**
- Message de succès si la syntaxe est correcte
- Détails des erreurs si la syntaxe est incorrecte

### Analyse

#### KnightBatch: Show AST
Affiche l'Arbre de Syntaxe Abstraite (AST) du fichier actuel.

**Utilisation :**
- Ouvrez un fichier `.shtest`
- Appuyez sur Ctrl+Shift+P
- Tapez "KnightBatch: Show AST"

**Résultat :**
- Nouvel onglet avec l'AST au format JSON
- Structure détaillée des nœuds et relations

#### KnightBatch: Show Tokens
Affiche les tokens générés par le lexer.

**Utilisation :**
- Ouvrez un fichier `.shtest`
- Appuyez sur Ctrl+Shift+P
- Tapez "KnightBatch: Show Tokens"

**Résultat :**
- Nouvel onglet avec la liste des tokens
- Informations sur le type et la valeur de chaque token

### Export

#### KnightBatch: Export to Excel
Exporte tous les scénarios de test vers un fichier Excel.

**Utilisation :**
- Clic droit sur un fichier `.shtest` dans l'explorateur
- Sélectionnez "KnightBatch: Export to Excel"

**Résultat :**
- Fichier Excel généré avec tous les scénarios
- Rapport du nombre de fichiers exportés

## Coloration Syntaxique

L'extension fournit une coloration syntaxique complète pour tous les éléments `.shtest` :

### Éléments de Base
- **Actions** : `Action:` en bleu
- **Résultats** : `Résultat:` en vert
- **Étapes** : `Etape:` en violet
- **Commentaires** : `#` en gris

### Opérations SQL
- **Variables SQL** : `SQL_DRIVER`, `SQL_CONN` en orange
- **Moteurs SQL** : `mysql`, `oracle`, `postgres` en cyan
- **Scripts SQL** : `script SQL` en jaune

### Opérations Fichier
- **Actions fichier** : `créer`, `copier`, `toucher` en bleu
- **Permissions** : `0600`, `0644`, `0755` en rouge
- **États fichier** : `présent`, `existe`, `créé` en vert

### Opérateurs Logiques
- **Connecteurs** : `et`, `ou` en violet
- **Flux** : `stdout`, `stderr` en orange
- **Comparaisons** : `contient`, `est`, `identique` en jaune

## Snippets

L'extension fournit des snippets organisés pour accélérer l'écriture :

### Snippets de Base
- `step` - Créer un nouveau bloc d'étape
- `action` - Créer une action avec résultat
- `exec` - Exécuter un script
- `createfile` - Créer un fichier
- `createdir` - Créer un dossier

### Snippets SQL
- `sqlconn` - Configuration de connexion SQL
- `sqlscript` - Exécution de script SQL

### Snippets de Validation
- `fileexists` - Vérifier l'existence d'un fichier
- `filecontent` - Vérifier le contenu d'un fichier
- `noerrors` - Vérifier l'absence d'erreurs
- `complex` - Validation complexe avec opérateurs logiques

### Snippets Avancés
- `execout` - Exécution avec validation de sortie
- `execargs` - Exécution avec arguments
- `checkperm` - Vérification de permissions
- `checkdate` - Vérification de date

**Utilisation :**
1. Tapez le préfixe du snippet
2. Appuyez sur Tab
3. Remplissez les variables `$1`, `$2`, etc.

## Configuration

### Paramètres VS Code

Ajoutez ces paramètres dans vos paramètres VS Code :

```json
{
  "knightbatch.configPath": "config/patterns_hybrid.yml",
  "knightbatch.aliasesPath": "config/aliases.yml",
  "knightbatch.outputDirectory": "output",
  "knightbatch.sqlDriver": "mysql",
  "knightbatch.debugMode": false
}
```

### Paramètres Disponibles

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| `configPath` | Chemin vers le fichier de patterns | `config/patterns_hybrid.yml` |
| `aliasesPath` | Chemin vers le fichier d'alias | `config/aliases.yml` |
| `outputDirectory` | Dossier de sortie pour les scripts | `output` |
| `sqlDriver` | Moteur SQL par défaut | `mysql` |
| `debugMode` | Mode debug pour logs détaillés | `false` |

### Configuration par Workspace

Créez un fichier `.vscode/settings.json` dans votre workspace :

```json
{
  "knightbatch.configPath": "config/custom_patterns.yml",
  "knightbatch.outputDirectory": "generated_scripts",
  "knightbatch.sqlDriver": "oracle"
}
```

## Exemples d'Utilisation

### Scénario de Test Complet

```shtest
# Test d'intégration base de données
Etape: Configuration
Action: Définir la variable SQL_DRIVER = mysql ; Résultat: identifiants configurés.
Action: Définir la variable SQL_CONN = user/pass@testdb ; Résultat: identifiants configurés.

Etape: Préparation
Action: Créer le dossier /tmp/test avec les droits 0755 ; Résultat: le dossier est créé.
Action: Créer le fichier /tmp/test/input.txt avec les droits 0644 ; Résultat: le fichier est présent.

Etape: Exécution
Action: Exécuter le script SQL init.sql ; Résultat: La base est prête.
Action: Exécuter /opt/batch/process.sh ; Résultat: retour 0 et stdout contient "SUCCESS".

Etape: Validation
Action: Vérifier que le fichier /tmp/test/output.txt existe ; Résultat: le fichier existe.
Action: Comparer le fichier /tmp/test/output.txt avec /tmp/test/expected.txt ; Résultat: fichiers identiques.
```

### Utilisation des Snippets

1. **Créer une étape** : Tapez `step` + Tab
2. **Ajouter une action** : Tapez `action` + Tab
3. **Configurer SQL** : Tapez `sqlconn` + Tab
4. **Valider un fichier** : Tapez `fileexists` + Tab

### Compilation Rapide

1. Ouvrez un fichier `.shtest`
2. Appuyez sur Ctrl+Shift+P
3. Tapez "KnightBatch: Compile Current File"
4. Le script shell est généré automatiquement

## Intégration avec l'Architecture Modulaire

L'extension supporte pleinement la nouvelle architecture modulaire :

### Support des Patterns Configurables
- Utilise les patterns définis dans `patterns_hybrid.yml`
- Support des alias définis dans `aliases.yml`
- Chargement dynamique de la configuration

### Support des Plugins
- Les plugins sont automatiquement détectés
- Les nouveaux matchers sont disponibles dans l'IntelliSense
- Les nouvelles validations sont reconnues

### Debug et Diagnostic
- Mode debug pour logs détaillés
- Affichage AST pour diagnostic
- Affichage tokens pour débogage

## Dépannage

### Problèmes Courants

#### Extension ne se charge pas
1. Vérifiez que vous êtes dans un workspace avec des fichiers `.shtest`
2. Redémarrez VS Code
3. Vérifiez les logs d'extension (Help > Toggle Developer Tools)

#### Commandes non disponibles
1. Vérifiez que l'extension est activée
2. Ouvrez un fichier `.shtest`
3. Vérifiez que vous êtes dans le bon workspace

#### Erreurs de compilation
1. Activez le mode debug dans les paramètres
2. Vérifiez les chemins de configuration
3. Vérifiez que KnightBatch est installé dans le workspace

#### Snippets ne fonctionnent pas
1. Vérifiez que le fichier a l'extension `.shtest`
2. Vérifiez que la langue est détectée comme "shtest"
3. Redémarrez VS Code

### Mode Debug

Activez le mode debug pour obtenir des informations détaillées :

```json
{
  "knightbatch.debugMode": true
}
```

Les logs apparaîtront dans la console de développement (Help > Toggle Developer Tools).

### Logs d'Extension

Pour voir les logs de l'extension :
1. Appuyez sur Ctrl+Shift+P
2. Tapez "Developer: Show Logs"
3. Sélectionnez "Extension Host"

## Développement

### Structure du Projet

```
vscode/
├── src/
│   ├── extension.ts          # Point d'entrée principal
│   └── test/                 # Tests unitaires
├── syntaxes/
│   └── shtest.tmLanguage.json # Coloration syntaxique
├── snippets/
│   └── shtest.code-snippets  # Snippets
├── themes/
│   └── shellTest.colorTheme.json # Thème de couleur
└── package.json              # Configuration de l'extension
```

### Ajouter de Nouveaux Snippets

1. Éditez `snippets/shtest.code-snippets`
2. Ajoutez un nouveau snippet :

```json
{
  "Nouveau Snippet": {
    "prefix": "newsnippet",
    "body": [
      "Action: $1 ; Résultat: $2"
    ],
    "description": "Description du nouveau snippet"
  }
}
```

### Modifier la Coloration Syntaxique

1. Éditez `syntaxes/shtest.tmLanguage.json`
2. Ajoutez de nouveaux patterns dans la section appropriée
3. Testez avec Ctrl+Shift+P > "Developer: Reload Window"

### Tests

Exécutez les tests de l'extension :

```bash
cd vscode
npm test
```

## Ressources

- [Documentation de l'architecture modulaire](modular_architecture.md)
- [Guide de configuration](configuration.md)
- [Format SHTEST](shtest_format.md)
- [Repository GitHub](https://github.com/knightbatch/shtest-compiler)

---

Pour plus d'informations sur l'utilisation pratique, consultez les [exemples d'utilisation](shtest_format.md) et la [documentation CLI](cli.md).