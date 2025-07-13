# Configuration

KnightBatch utilise un système de configuration hybride combinant des fichiers INI pour les paramètres globaux et des fichiers YAML pour les patterns et alias.

## Configuration Globale (config.ini)

Le fichier `config.ini` situé à la racine du projet permet de définir les chemins par défaut utilisés par les scripts.

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

### Paramètres disponibles

- `input_dir` : Répertoire par défaut contenant les fichiers `.shtest`
- `output_dir` : Répertoire de sortie pour les scripts générés
- `sql_driver` : Moteur SQL par défaut (`mysql`, `oracle`, `postgres`, `redis`)
- `config_path` : Chemin vers le fichier de patterns YAML
- `aliases_path` : Chemin vers le fichier d'alias YAML
- `plugin_path` : Répertoire contenant les plugins
- `debug` : Mode debug (true/false)

## Configuration des Patterns (patterns_hybrid.yml)

Le fichier `config/patterns_hybrid.yml` définit les patterns de reconnaissance pour le lexer et la grammaire pour le parser.

### Structure des Tokens

```yaml
tokens:
  action:
    pattern: "Action:\\s*(.+)"
    type: "ACTION"
    priority: 1
  validation:
    pattern: "Résultat:\\s*(.+)"
    type: "VALIDATION"
    priority: 2
  file_operation:
    pattern: "(créer|copier|toucher|comparer)\\s+le\\s+fichier"
    type: "FILE_OP"
    priority: 3
  sql_operation:
    pattern: "(exécuter|définir)\\s+(le\\s+)?(script\\s+)?sql"
    type: "SQL_OP"
    priority: 4
```

### Grammaire

```yaml
grammar:
  rules:
    - name: "action_validation"
      pattern: "action:validation"
      builder: "action_validation_builder"
      priority: 1
    - name: "file_operation"
      pattern: "file_operation:validation"
      builder: "file_operation_builder"
      priority: 2
    - name: "sql_operation"
      pattern: "sql_operation:validation"
      builder: "sql_operation_builder"
      priority: 3
```

### Filtres de Tokens

```yaml
filters:
  - name: "whitespace_filter"
    type: "whitespace"
    enabled: true
  - name: "comment_filter"
    type: "comment"
    pattern: "#.*"
    enabled: true
```

## Configuration des Alias (aliases.yml)

Le fichier `config/aliases.yml` définit les alias en langage naturel qui sont mappés vers des expressions techniques normalisées.

### Structure des Alias

```yaml
aliases:
  actions:
    execute_script:
      variants:
        - "exécuter le script"
        - "lancer le script"
        - "démarrer le script"
      normalized: "exécuter"
    
    create_file:
      variants:
        - "créer le fichier"
        - "générer le fichier"
        - "fabriquer le fichier"
      normalized: "créer fichier"
    
    copy_file:
      variants:
        - "copier le fichier"
        - "dupliquer le fichier"
        - "reproduire le fichier"
      normalized: "copier fichier"
  
  validations:
    success:
      variants:
        - "succès"
        - "réussi"
        - "ok"
        - "valide"
      normalized: "retour 0"
    
    file_exists:
      variants:
        - "le fichier est présent"
        - "le fichier existe"
        - "fichier créé"
      normalized: "fichier présent"
    
    sql_ready:
      variants:
        - "la base est prête"
        - "base de données prête"
        - "bdd prête"
      normalized: "base prête"
```

## Variables d'Environnement

Vous pouvez surcharger la configuration via des variables d'environnement :

```bash
# Chemin vers les fichiers de configuration
export SHTEST_CONFIG_PATH="config/patterns_hybrid.yml"
export SHTEST_ALIASES_PATH="config/aliases.yml"

# Chemin vers les plugins
export SHTEST_PLUGIN_PATH="plugins/"

# Mode debug
export SHTEST_DEBUG=1

# Moteur SQL par défaut
export SHTEST_SQL_DRIVER="mysql"
```

## Configuration des Plugins

Les plugins peuvent être configurés via des fichiers YAML dans le répertoire `plugins/` :

```yaml
# plugins/custom_plugin.yml
plugin:
  name: "custom_plugin"
  version: "1.0.0"
  enabled: true
  
  matchers:
    - name: "custom_validation"
      function: "custom_matcher"
      priority: 10
  
  visitors:
    - name: "custom_generator"
      class: "CustomGenerator"
      enabled: true
```

## Configuration Avancée

### Chargement Dynamique

```python
from shtest_compiler.config import load_config, load_patterns, load_aliases

# Charger la configuration globale
config = load_config("config.ini")

# Charger les patterns
patterns = load_patterns("config/patterns_hybrid.yml")

# Charger les alias
aliases = load_aliases("config/aliases.yml")
```

### Validation de Configuration

```python
from shtest_compiler.config import validate_config

# Valider la configuration
errors = validate_config(config)
if errors:
    print("Erreurs de configuration:", errors)
```

### Configuration par Projet

Vous pouvez créer des fichiers de configuration spécifiques par projet :

```bash
# Configuration pour le projet A
SHTEST_CONFIG_PATH="projects/project_a/config.yml"
SHTEST_ALIASES_PATH="projects/project_a/aliases.yml"

# Configuration pour le projet B
SHTEST_CONFIG_PATH="projects/project_b/config.yml"
SHTEST_ALIASES_PATH="projects/project_b/aliases.yml"
```

## Migration depuis l'Ancienne Configuration

### Ancien système (Python)

```python
# Ancien code
patterns = {
    "action": r"Action:\s*(.+)",
    "validation": r"Résultat:\s*(.+)"
}
```

### Nouveau système (YAML)

```yaml
# Nouveau code
tokens:
  action:
    pattern: "Action:\\s*(.+)"
    type: "ACTION"
  validation:
    pattern: "Résultat:\\s*(.+)"
    type: "VALIDATION"
```

## Diagnostic de Configuration

### Vérification de la Configuration

```bash
# Vérifier que tous les fichiers de configuration sont présents
python -c "
from shtest_compiler.config import load_config, load_patterns, load_aliases
try:
    config = load_config()
    patterns = load_patterns()
    aliases = load_aliases()
    print('Configuration OK')
except Exception as e:
    print(f'Erreur: {e}')
"
```

### Logs de Configuration

```bash
# Activer les logs de configuration
export SHTEST_DEBUG=1
python shtest.py tests/example.shtest
```

---

Pour plus d'informations sur l'utilisation des patterns et alias, consultez la [documentation des regex](regex_documentation.md).

