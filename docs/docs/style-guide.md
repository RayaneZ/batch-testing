# Guide de Style KnightBatch

Ce guide définit les conventions de style et les bonnes pratiques pour le développement avec KnightBatch.

## Structure des fichiers .shtest

### Format général

```yaml
Étape: Nom de l'étape
Action: Description de l'action en français
Résultat: Expression de validation attendue
```

### Conventions de nommage

- **Étapes** : Utilisez des noms descriptifs en français
  - ✅ `Étape: Préparation de l'environnement`
  - ❌ `Étape: setup`

- **Actions** : Décrivez clairement l'action à effectuer
  - ✅ `Action: Créer le dossier /tmp/test`
  - ❌ `Action: mkdir /tmp/test`

- **Résultats** : Utilisez les expressions de validation standard
  - ✅ `Résultat: Le dossier est créé`
  - ❌ `Résultat: folder exists`

## Expressions de validation

### Validations de base

| Expression | Description |
|------------|-------------|
| `Retour 0` | Vérifie que la commande retourne un code de sortie 0 |
| `Le fichier existe` | Vérifie l'existence d'un fichier |
| `Le dossier est créé` | Vérifie l'existence d'un dossier |
| `Le contenu est affiché` | Vérifie que du contenu est affiché sur stdout |

### Validations avancées

```yaml
Résultat: stdout contient 'succès'
Résultat: stderr ne contient pas 'erreur'
Résultat: Le fichier /path/to/file contient 'texte attendu'
```

## Variables et arguments

### Définition de variables

```yaml
Action: Définir la variable SQL_DRIVER = oracle
Action: Définir la variable CONFIG_PATH = /etc/config
```

### Utilisation d'arguments

```yaml
Action: Exécuter le script {script} avec l'argument {arg}
```

## Scripts SQL

### Format des scripts SQL

```yaml
Action: Exécuter le script SQL {script}
Résultat: Le script SQL s'exécute sans erreur
```

### Variables SQL

```yaml
Action: Définir la variable SQL_CONN = user/pass@host:port/service
Action: Définir la variable SQL_DRIVER = oracle
```

## Opérations sur les fichiers

### Création

```yaml
Action: Créer le fichier /path/to/file
Action: Créer le dossier /path/to/directory
```

### Manipulation

```yaml
Action: Copier le fichier source vers destination
Action: Déplacer le fichier source vers destination
Action: Supprimer le fichier /path/to/file
```

### Validation

```yaml
Résultat: Le fichier est copié
Résultat: Le fichier est déplacé
Résultat: Le fichier est supprimé
```

## Commentaires et documentation

### Commentaires dans les tests

```yaml
# Ce test vérifie la création d'un environnement de test
Étape: Préparation de l'environnement
Action: Créer le dossier /tmp/test_env
Résultat: Le dossier est créé

# Vérification de la configuration
Étape: Configuration
Action: Copier le fichier config.ini vers /tmp/test_env/
Résultat: Le fichier est copié
```

### Documentation des plugins

Chaque plugin doit inclure :

1. **Description** : Ce que fait le plugin
2. **Patterns** : Les expressions reconnues
3. **Arguments** : Les paramètres attendus
4. **Exemples** : Cas d'usage typiques

## Bonnes pratiques

### Lisibilité

- Utilisez des noms d'étapes descriptifs
- Évitez les abréviations
- Commentez les sections complexes

### Maintenabilité

- Groupez les actions logiquement
- Réutilisez les variables pour les chemins
- Testez chaque étape individuellement

### Robustesse

- Vérifiez toujours les résultats
- Gérez les cas d'erreur
- Utilisez des chemins absolus quand possible

## Exemples complets

### Test simple

```yaml
Étape: Test de création de fichier
Action: Créer le fichier /tmp/test.txt
Résultat: Le fichier existe

Étape: Test de contenu
Action: Écrire 'Hello World' dans /tmp/test.txt
Résultat: Le fichier contient 'Hello World'
```

### Test avec variables

```yaml
Action: Définir la variable TEST_DIR = /tmp/knightbatch_test
Action: Créer le dossier {TEST_DIR}
Résultat: Le dossier est créé

Action: Créer le fichier {TEST_DIR}/config.ini
Résultat: Le fichier existe
```

### Test SQL

```yaml
Action: Définir la variable SQL_DRIVER = oracle
Action: Définir la variable SQL_CONN = user/pass@host:1521/service
Action: Exécuter le script SQL scripts/test.sql
Résultat: Le script SQL s'exécute sans erreur
Résultat: stdout contient 'SUCCESS'
```

## Ressources

- [Format SHTEST](shtest_format.md) - Documentation complète du format
- [Expressions régulières](regex_documentation.md) - Patterns reconnus
- [Tutoriel des plugins](plugin_tutorial.md) - Création de plugins personnalisés 