# Tutoriel : Créer un Plugin KnightBatch

Ce tutoriel vous guide à travers la création d'un plugin complet pour KnightBatch, depuis la conception jusqu'au déploiement.

## Vue d'Ensemble

![Architecture des plugins](assets/plugin_architecture.png)

> Architecture du système de plugins montrant comment les plugins s'intègrent dans le pipeline principal.

Les plugins KnightBatch permettent d'étendre les fonctionnalités du compilateur avec :
- **Nouveaux types d'actions** personnalisées
- **Validations spécialisées** pour vos besoins
- **Générateurs de code** spécifiques
- **Intégrations externes** (APIs, bases de données, etc.)

## Architecture d'un Plugin

```
┌─────────────────┐
│   Plugin        │
│   Principal     │
├─────────────────┤
│   Config/       │
│   YAML Files    │
├─────────────────┤
│   Action        │
│   Handlers      │
├─────────────────┤
│   Validation    │
│   Handlers      │
└─────────────────┘
```

## Étape 1 : Planifier votre Plugin

### Définir les Fonctionnalités

Avant de commencer, identifiez :

1. **Actions** : Que voulez-vous que votre plugin puisse faire ?
2. **Validations** : Comment voulez-vous vérifier les résultats ?
3. **Patterns** : Quelle syntaxe utiliserez-vous dans les fichiers `.shtest` ?
4. **Dépendances** : Avez-vous besoin de bibliothèques externes ?

### Exemple : Plugin de Notification

Nous allons créer un plugin qui permet d'envoyer des notifications :
- **Action** : Envoyer une notification Slack/Email
- **Validation** : Vérifier que la notification a été envoyée
- **Pattern** : `Envoyer une notification: message`
- **Validation** : `La notification a été envoyée`

## Étape 2 : Créer la Structure du Plugin

### Structure des Dossiers

![Structure d'un plugin](assets/plugin_structure.png)

> Structure typique d'un plugin montrant l'organisation des fichiers et dossiers.

```
src/shtest_compiler/plugins/notification/
├── __init__.py
├── config/
│   ├── patterns_actions.yml
│   ├── patterns_validations.yml
│   └── handler_requirements.yml
├── action_handlers/
│   ├── __init__.py
│   └── send_notification.py
└── handlers/
    ├── __init__.py
    └── notification_sent.py
```

### Créer le Dossier Principal

```bash
mkdir -p src/shtest_compiler/plugins/notification
mkdir -p src/shtest_compiler/plugins/notification/config
mkdir -p src/shtest_compiler/plugins/notification/action_handlers
mkdir -p src/shtest_compiler/plugins/notification/handlers
```

## Étape 3 : Définir les Patterns YAML

### Fichier `config/patterns_actions.yml`

```yaml
# patterns_actions.yml
#
# Define action patterns for your plugin here.
# Each entry should have:
#   - phrase: The user-facing pattern to match in .shtest files
#   - handler: The name of the Python function (in action_handlers/) to call
#   - aliases: List of alternative phrases or regexes for user input matching

actions:
  - phrase: "Envoyer une notification {message}"
    handler: send_notification
    aliases:
      - "envoyer une notification {message}"
      - "notifier {message}"
      - "^envoyer une notification (.+)$"
      - "^notifier (.+)$"

  - phrase: "Envoyer une notification Slack {message}"
    handler: send_slack_notification
    aliases:
      - "envoyer une notification slack {message}"
      - "slack {message}"
      - "^envoyer une notification slack (.+)$"
      - "^slack (.+)$"
```

### Fichier `config/patterns_validations.yml`

```yaml
# patterns_validations.yml
#
# Define validation patterns for your plugin here.
# Each entry should have:
#   - phrase: The user-facing pattern to match in .shtest files
#   - handler: The name of the Python function (in handlers/) to call
#   - scope: 'last_action' (local, must follow an action) or 'global' (can be checked independently)
#   - aliases: List of alternative phrases or regexes for user input matching

validations:
  - phrase: "La notification a été envoyée"
    handler: notification_sent
    scope: last_action
    aliases:
      - "la notification a été envoyée"
      - "notification envoyée"
      - "^la notification a été envoyée$"
      - "^notification envoyée$"

  - phrase: "La notification Slack a été envoyée"
    handler: slack_notification_sent
    scope: last_action
    aliases:
      - "la notification slack a été envoyée"
      - "slack envoyé"
      - "^la notification slack a été envoyée$"
      - "^slack envoyé$"
```

### Fichier `config/handler_requirements.yml`

```yaml
# handler_requirements.yml
#
# This file documents the requirements and expected parameters for each handler in the plugin.
# Use this to specify what parameters/actions/validations each handler expects or needs.

send_notification:
  description: "Sends a notification via the configured system"
  params:
    - name: message
      type: str
      required: true
      description: "The message to send in the notification"

send_slack_notification:
  description: "Sends a Slack notification"
  params:
    - name: message
      type: str
      required: true
      description: "The message to send to Slack"

notification_sent:
  description: "Checks if a notification was sent successfully"
  params:
    - name: target_dir
      type: str
      required: false
      default: '.'
      description: "Directory to check for notification logs"

slack_notification_sent:
  description: "Checks if a Slack notification was sent successfully"
  params:
    - name: target_dir
      type: str
      required: false
      default: '.'
      description: "Directory to check for Slack notification logs"
```

## Étape 4 : Créer les Handlers d'Action

### Pattern des Handlers

![Pattern des handlers](assets/handler_pattern.png)

> Flux de données montrant comment les paramètres passent des patterns YAML aux handlers.

### Handler Principal (`action_handlers/send_notification.py`)

```python
import os
from shtest_compiler.ast.shell_framework_ast import ActionNode

class SendNotificationAction(ActionNode):
    """
    ActionNode for sending notifications via the configured system.
    This is a template for plugin developers: extend this pattern for your own actions!
    """
    def __init__(self, message, notification_type="log"):
        self.message = message
        self.notification_type = notification_type

    def to_shell(self):
        # Generates a shell command to send the notification.
        # The actual implementation depends on the notification type.
        if self.notification_type == "slack":
            return self._generate_slack_command()
        elif self.notification_type == "email":
            return self._generate_email_command()
        else:
            return self._generate_log_command()

    def _generate_slack_command(self):
        """Generate shell command for Slack notification."""
        return f"""# Send Slack notification
if [ -n "$SLACK_WEBHOOK_URL" ]; then
    curl -X POST -H 'Content-type: application/json' \\
        --data '{"text":"{self.message}"}' \\
        "$SLACK_WEBHOOK_URL" \\
        && echo "Slack notification sent" \\
        || (echo "Failed to send Slack notification" >&2 && exit 1)
else
    echo "SLACK_WEBHOOK_URL not configured" >&2
    exit 1
fi"""

    def _generate_email_command(self):
        """Generate shell command for email notification."""
        return f"""# Send email notification
if [ -n "$NOTIFICATION_EMAIL" ]; then
    echo "{self.message}" | mail -s "KnightBatch Notification" "$NOTIFICATION_EMAIL" \\
        && echo "Email notification sent" \\
        || (echo "Failed to send email notification" >&2 && exit 1)
else
    echo "NOTIFICATION_EMAIL not configured" >&2
    exit 1
fi"""

    def _generate_log_command(self):
        """Generate shell command for log notification."""
        return f"""# Log notification
echo "[$(date)] NOTIFICATION: {self.message}" >> /tmp/notifications.log \\
    && echo "Notification logged" \\
    || (echo "Failed to log notification" >&2 && exit 1)"""


def handle(params):
    """
    Handler entry point for the action. Expects a 'params' dict with 'message'.
    Returns an ActionNode for shell script generation.
    """
    message = params.get("message", "Default notification message")
    notification_type = params.get("type", "log")
    return SendNotificationAction(message, notification_type)
```

### Handler Slack (`action_handlers/send_slack_notification.py`)

```python
from shtest_compiler.ast.shell_framework_ast import ActionNode

class SendSlackNotificationAction(ActionNode):
    """
    ActionNode for sending Slack notifications.
    """
    def __init__(self, message, channel="#general"):
        self.message = message
        self.channel = channel

    def to_shell(self):
        return f"""# Send Slack notification
if [ -n "$SLACK_WEBHOOK_URL" ]; then
    curl -X POST -H 'Content-type: application/json' \\
        --data '{"text":"{self.message}","channel":"{self.channel}"}' \\
        "$SLACK_WEBHOOK_URL" \\
        && echo "Slack notification sent to {self.channel}" \\
        || (echo "Failed to send Slack notification" >&2 && exit 1)
else
    echo "SLACK_WEBHOOK_URL not configured" >&2
    exit 1
fi"""


def handle(params):
    """
    Handler entry point for Slack notifications.
    """
    message = params.get("message", "Default Slack message")
    channel = params.get("channel", "#general")
    return SendSlackNotificationAction(message, channel)
```

## Étape 5 : Créer les Handlers de Validation

### Handler de Validation (`handlers/notification_sent.py`)

```python
import os
from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    """
    Validation handler: Checks if a notification was sent successfully.
    """
    target_dir = params.get("target_dir", ".")
    log_file = os.path.join(target_dir, "notifications.log")
    
    # Return atomic command only - no if/then/else logic
    actual_cmd = f"""# Check if notification was sent
if [ -f "{log_file}" ] && grep -q "NOTIFICATION:" "{log_file}"; then
    echo "Notification verified"
    exit 0
else
    echo "Notification not found" >&2
    exit 1
fi"""

    return ValidationCheck(
        expected="La notification a été envoyée",
        actual_cmd=actual_cmd,
        handler="notification_sent",
        scope="last_action",
        params={"log_file": log_file}
    )
```

### Handler Slack Validation (`handlers/slack_notification_sent.py`)

```python
import os
from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    """
    Validation handler: Checks if a Slack notification was sent successfully.
    """
    target_dir = params.get("target_dir", ".")
    log_file = os.path.join(target_dir, "slack_notifications.log")
    
    # Return atomic command only - no if/then/else logic
    actual_cmd = f"""# Check if Slack notification was sent
if [ -f "{log_file}" ] && grep -q "Slack notification sent" "{log_file}"; then
    echo "Slack notification verified"
    exit 0
else
    echo "Slack notification not found" >&2
    exit 1
fi"""

    return ValidationCheck(
        expected="La notification Slack a été envoyée",
        actual_cmd=actual_cmd,
        handler="slack_notification_sent",
        scope="last_action",
        params={"log_file": log_file}
    )
```

## Étape 6 : Créer le Point d'Entrée du Plugin

### Fichier `__init__.py` Principal

```python
"""
Plugin de notification pour KnightBatch.

Ce plugin permet d'envoyer des notifications via différents canaux
(Slack, Email, Log) et de valider leur envoi.

Structure:
- config/: YAML files defining action and validation patterns
- action_handlers/: Python modules implementing actions
- handlers/: Python modules implementing validations

To create your own plugin, copy this structure and update the YAML and handler files as needed.
"""

# The plugin is automatically discovered and loaded by the framework
# No additional registration code is needed
```

## Étape 7 : Configurer le Plugin

### Variables d'Environnement

```bash
# Configuration Slack
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export SLACK_CHANNEL="#alerts"

# Configuration Email
export NOTIFICATION_EMAIL="admin@example.com"
export SMTP_SERVER="smtp.example.com"

# Type de notification par défaut
export NOTIFICATION_TYPE="slack"
```

## Étape 8 : Tester votre Plugin

### Workflow de Tests

![Workflow de tests](assets/testing_workflow.png)

> Workflow complet de tests montrant le processus de validation, compilation et exécution.

### Fichier de Test `.shtest`

```shtest
# tests/notification_test.shtest
Étape: Test des notifications
  Action: Envoyer une notification: Test de notification KnightBatch
  Résultat: La notification a été envoyée

Étape: Test des notifications Slack
  Action: Envoyer une notification Slack: Test Slack depuis KnightBatch
  Résultat: La notification Slack a été envoyée

Étape: Test avec variables
  Action: Définir la variable: message = "Notification avec variable"
  Action: Envoyer une notification: ${message}
  Résultat: La notification a été envoyée
```

### Tests Unitaires

```python
# tests/unit/test_notification_plugin.py
import pytest
from shtest_compiler.plugins.notification.action_handlers.send_notification import handle

def test_notification_handler():
    """Test le handler de notification."""
    params = {"message": "Test message"}
    result = handle(params)
    
    assert result is not None
    assert hasattr(result, 'to_shell')
    assert "Test message" in result.to_shell()

def test_slack_handler():
    """Test le handler Slack."""
    from shtest_compiler.plugins.notification.action_handlers.send_slack_notification import handle as slack_handle
    
    params = {"message": "Test Slack"}
    result = slack_handle(params)
    
    assert result is not None
    assert hasattr(result, 'to_shell')
    assert "curl" in result.to_shell()
```

### Tests E2E

```bash
# Compiler et tester le plugin
python -m shtest_compiler.run_all --input tests/notification_test.shtest

# Vérifier la syntaxe
python src/shtest_compiler/verify_syntax.py tests/notification_test.shtest

# Exécuter le script généré
bash output/notification_test.sh
```

## Étape 9 : Déployer votre Plugin

### Installation

1. **Copier le plugin** dans le répertoire des plugins :
```bash
cp -r src/shtest_compiler/plugins/notification /path/to/knightbatch/plugins/
```

2. **Configurer les variables** d'environnement :
```bash
export SLACK_WEBHOOK_URL="your_webhook_url"
export NOTIFICATION_TYPE="slack"
```

### Utilisation

```shtest
# Exemple d'utilisation du plugin
Étape: Notifier le succès d'un test
  Action: Exécuter le script: ./my_test.sh
  Résultat: Le code de retour est 0
  Action: Envoyer une notification: Test réussi - $(date)
  Résultat: La notification a été envoyée
```

## Bonnes Pratiques

### Conception du Plugin

1. **Séparation des responsabilités** : Handlers, validations, et configuration séparés
2. **Gestion d'erreurs** : Toujours gérer les cas d'erreur et retourner des codes appropriés
3. **Configuration flexible** : Utiliser des variables d'environnement et des valeurs par défaut
4. **Documentation** : Documenter chaque fonction et paramètre

### Tests

1. **Tests unitaires** : Tester chaque fonction individuellement
2. **Tests d'intégration** : Tester l'interaction avec le système principal
3. **Tests E2E** : Tester avec des fichiers `.shtest` réels
4. **Tests négatifs** : Tester les cas d'erreur et d'échec

### Performance

1. **Validation légère** : Les validations doivent être rapides
2. **Gestion des ressources** : Libérer les ressources (connexions, fichiers)
3. **Cache** : Mettre en cache les résultats coûteux
4. **Logging** : Logger les opérations importantes pour le debug

### Sécurité

1. **Validation des entrées** : Valider tous les paramètres d'entrée
2. **Échappement** : Échapper les caractères spéciaux dans les commandes shell
3. **Permissions** : Vérifier les permissions avant les opérations sensibles
4. **Secrets** : Ne pas exposer les secrets dans les logs

## Exemples Avancés

### Plugin avec Base de Données

```python
from shtest_compiler.ast.shell_framework_ast import ActionNode

class DatabaseQueryAction(ActionNode):
    def __init__(self, query, database_url):
        self.query = query
        self.database_url = database_url

    def to_shell(self):
        return f"""# Execute database query
psql "{self.database_url}" -c "{self.query}" \\
  && echo "Query executed successfully" \\
  || (echo "Database query failed" >&2 && exit 1)"""

def handle(params):
    query = params.get("query")
    database_url = params.get("database_url", "$DATABASE_URL")
    return DatabaseQueryAction(query, database_url)
```

### Plugin avec API REST

```python
from shtest_compiler.ast.shell_framework_ast import ActionNode

class APICallAction(ActionNode):
    def __init__(self, endpoint, method="GET", api_key=None):
        self.endpoint = endpoint
        self.method = method
        self.api_key = api_key

    def to_shell(self):
        headers = f"-H 'Authorization: Bearer {self.api_key}'" if self.api_key else ""
        return f"""# API REST call
curl -X {self.method} {headers} "$API_BASE_URL{self.endpoint}" \\
  && echo "API call successful" \\
  || (echo "API call failed" >&2 && exit 1)"""

def handle(params):
    endpoint = params.get("endpoint")
    method = params.get("method", "GET")
    api_key = params.get("api_key", "$API_KEY")
    return APICallAction(endpoint, method, api_key)
```

## Dépannage

### Problèmes Courants

1. **Plugin non trouvé** : Vérifier le chemin et la structure des dossiers
2. **Handler non appelé** : Vérifier les patterns YAML et les noms de handlers
3. **Variables non définies** : Vérifier la configuration et les variables d'environnement
4. **Erreurs de syntaxe** : Vérifier les commandes shell générées

### Debug

```python
# Activer le debug pour le plugin
import logging
logging.basicConfig(level=logging.DEBUG)

# Vérifier l'enregistrement
from shtest_compiler.command_loader import discover_plugins
plugins = discover_plugins()
print("Plugins trouvés:", plugins)
```

## Conclusion

Ce tutoriel vous a guidé à travers la création complète d'un plugin KnightBatch. Les plugins sont un moyen puissant d'étendre les fonctionnalités du système selon vos besoins spécifiques.

Pour plus d'informations, consultez :
- [Architecture Modulaire](modular_architecture.md)
- [Guide Développeur](developer_quickstart.md)
- [Tests et Validation](testing_and_validation.md)