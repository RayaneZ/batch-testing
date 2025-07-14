# Tutoriel : Créer un Plugin KnightBatch

Ce tutoriel vous guide à travers la création d'un plugin complet pour KnightBatch, depuis la conception jusqu'au déploiement.

## Vue d'Ensemble

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
│   Patterns      │
│   YAML          │
├─────────────────┤
│   Handlers      │
│   (Actions)     │
├─────────────────┤
│   Matchers      │
│   (Validations) │
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

```
src/shtest_compiler/plugins/notification/
├── __init__.py
├── config/
│   └── patterns_notification.yml
├── handlers/
│   ├── __init__.py
│   ├── send_notification.py
│   └── verify_notification.py
└── matchers/
    ├── __init__.py
    └── notification_matcher.py
```

### Créer le Dossier Principal

```bash
mkdir -p src/shtest_compiler/plugins/notification
mkdir -p src/shtest_compiler/plugins/notification/config
mkdir -p src/shtest_compiler/plugins/notification/handlers
mkdir -p src/shtest_compiler/plugins/notification/matchers
```

## Étape 3 : Définir les Patterns YAML

### Fichier `patterns_notification.yml`

```yaml
# Patterns pour les actions de notification
actions:
  send_notification:
    pattern: "Envoyer une notification:\\s*(.+)"
    handler: "notification.handlers.send_notification.send_notification_handler"
    description: "Envoie une notification via le système configuré"

  send_slack_notification:
    pattern: "Envoyer une notification Slack:\\s*(.+)"
    handler: "notification.handlers.send_notification.send_slack_handler"
    description: "Envoie une notification Slack spécifique"

# Patterns pour les validations
validations:
  notification_sent:
    pattern: "La notification a été envoyée"
    handler: "notification.matchers.notification_matcher.verify_notification_sent"
    description: "Vérifie qu'une notification a été envoyée avec succès"

  slack_notification_sent:
    pattern: "La notification Slack a été envoyée"
    handler: "notification.matchers.notification_matcher.verify_slack_sent"
    description: "Vérifie qu'une notification Slack a été envoyée"
```

## Étape 4 : Créer les Handlers d'Action

### Handler Principal (`handlers/send_notification.py`)

```python
from shtest_compiler.ast.shell_framework_ast import ActionNode

class SendNotificationAction(ActionNode):
    def __init__(self, message):
        self.message = message

    def to_shell(self):
        # Génère la commande shell pour envoyer la notification
        return f"echo 'Notification: {self.message}' >> /tmp/notifications.log"

def handle(params):
    message = params["message"]
    return SendNotificationAction(message)
```
- Le handler doit accepter uniquement `params` (pas de `context` sauf besoin avancé).
- Le handler doit retourner un objet `ActionNode` avec une méthode `to_shell()` pour les actions shell.
- **Ne pas utiliser `os.environ` ou des variables globales dans vos handlers.**

## Étape 5 : Créer les Matchers de Validation

### Matcher Principal (`matchers/notification_matcher.py`)

```python
"""
Matchers pour les validations de notification.
"""

import os
from typing import Dict, Any, Optional
from shtest_compiler.core.context import CompileContext


def verify_notification_sent(context: CompileContext, validation_text: str, **kwargs) -> str:
    """
    Vérifie qu'une notification a été envoyée avec succès.

    Args:
        context: Contexte de compilation
        validation_text: Texte de validation
        **kwargs: Arguments supplémentaires

    Returns:
        Code shell pour vérifier la notification
    """
    notification_type = context.get_variable("NOTIFICATION_TYPE", "log")

    if notification_type == "slack":
        return _verify_slack_notification()
    elif notification_type == "email":
        return _verify_email_notification()
    else:
        return _verify_log_notification()


def verify_slack_sent(context: CompileContext, validation_text: str, **kwargs) -> str:
    """
    Vérifie spécifiquement qu'une notification Slack a été envoyée.

    Args:
        context: Contexte de compilation
        validation_text: Texte de validation
        **kwargs: Arguments supplémentaires

    Returns:
        Code shell pour vérifier la notification Slack
    """
    return _verify_slack_notification()


def _verify_slack_notification() -> str:
    """Génère le code shell pour vérifier une notification Slack."""

    return """# Vérifier notification Slack
if [ -f /tmp/slack_notification_sent ]; then
    echo "Notification Slack vérifiée"
    rm /tmp/slack_notification_sent
    exit 0
else
    echo "Notification Slack non trouvée" >&2
    exit 1
fi"""


def _verify_email_notification() -> str:
    """Génère le code shell pour vérifier une notification Email."""

    return """# Vérifier notification Email
if [ -f /tmp/email_notification_sent ]; then
    echo "Notification Email vérifiée"
    rm /tmp/email_notification_sent
    exit 0
else
    echo "Notification Email non trouvée" >&2
    exit 1
fi"""


def _verify_log_notification() -> str:
    """Génère le code shell pour vérifier une notification loggée."""

    return """# Vérifier notification loggée
if [ -f /tmp/notifications.log ] && grep -q "NOTIFICATION:" /tmp/notifications.log; then
    echo "Notification loggée vérifiée"
    exit 0
else
    echo "Notification loggée non trouvée" >&2
    exit 1
fi"""
```

## Étape 6 : Créer le Point d'Entrée du Plugin

### Fichier `__init__.py` Principal

```python
"""
Plugin de notification pour KnightBatch.

Ce plugin permet d'envoyer des notifications via différents canaux
(Slack, Email, Log) et de valider leur envoi.
"""

from typing import Dict, Any
from shtest_compiler.core.context import CompileContext


def register_plugin(context: CompileContext) -> None:
    """
    Enregistre le plugin de notification dans le contexte.

    Args:
        context: Contexte de compilation où enregistrer le plugin
    """
    # Enregistrer les handlers d'action
    _register_action_handlers(context)

    # Enregistrer les matchers de validation
    _register_validation_matchers(context)

    # Définir les variables par défaut
    _set_default_variables(context)

    print("Plugin de notification enregistré avec succès")


def _register_action_handlers(context: CompileContext) -> None:
    """Enregistre les handlers d'action."""

    from .handlers.send_notification import (
        send_notification_handler,
        send_slack_handler
    )

    context.register_action_handler("send_notification", send_notification_handler)
    context.register_action_handler("send_slack_notification", send_slack_handler)


def _register_validation_matchers(context: CompileContext) -> None:
    """Enregistre les matchers de validation."""

    from .matchers.notification_matcher import (
        verify_notification_sent,
        verify_slack_sent
    )

    context.register_validation_matcher("notification_sent", verify_notification_sent)
    context.register_validation_matcher("slack_notification_sent", verify_slack_sent)


def _set_default_variables(context: CompileContext) -> None:
    """Définit les variables par défaut du plugin."""

    defaults = {
        "NOTIFICATION_TYPE": "log",
        "NOTIFICATION_URL": "",
        "SLACK_WEBHOOK_URL": "",
        "SLACK_CHANNEL": "#general",
        "NOTIFICATION_EMAIL": ""
    }

    for key, value in defaults.items():
        if not context.get_variable(key):
            context.set_variable(key, value)
```

## Étape 7 : Configurer le Plugin

### Fichier de Configuration

Créez un fichier de configuration pour votre plugin :

```yaml
# config/notification_config.yml
notification:
  # Type de notification par défaut
  default_type: "log"

  # Configuration Slack
  slack:
    webhook_url: "${SLACK_WEBHOOK_URL}"
    default_channel: "#general"
    username: "KnightBatch Bot"

  # Configuration Email
  email:
    smtp_server: "localhost"
    smtp_port: 25
    from_address: "knightbatch@example.com"

  # Configuration Log
  log:
    file_path: "/tmp/notifications.log"
    format: "[{timestamp}] {type}: {message}"
```

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

### Fichier de Test `.shtest`

```shtest
# tests/notification_test.shtest
Étape: Test des notifications
  Action: Envoyer une notification: Test de notification KnightBatch
  Vérifier: La notification a été envoyée

Étape: Test des notifications Slack
  Action: Envoyer une notification Slack: Test Slack depuis KnightBatch
  Vérifier: La notification Slack a été envoyée

Étape: Test avec variables
  Action: Définir la variable: message = "Notification avec variable"
  Action: Envoyer une notification: ${message}
  Vérifier: La notification a été envoyée
```

### Tests Unitaires

```python
# tests/unit/test_notification_plugin.py
import pytest
from shtest_compiler.core.context import CompileContext
from shtest_compiler.plugins.notification import register_plugin


def test_notification_plugin_registration():
    """Test l'enregistrement du plugin de notification."""
    context = CompileContext()
    register_plugin(context)

    # Vérifier que les handlers sont enregistrés
    assert context.get_action_handler("send_notification") is not None
    assert context.get_action_handler("send_slack_notification") is not None

    # Vérifier que les matchers sont enregistrés
    assert context.get_validation_matcher("notification_sent") is not None
    assert context.get_validation_matcher("slack_notification_sent") is not None


def test_notification_handler():
    """Test le handler de notification."""
    context = CompileContext()
    register_plugin(context)

    handler = context.get_action_handler("send_notification")
    result = handler(context, "Test message")

    assert "Test message" in result
    assert "echo" in result


def test_slack_handler():
    """Test le handler Slack."""
    context = CompileContext()
    context.set_variable("SLACK_WEBHOOK_URL", "https://test.com")
    register_plugin(context)

    handler = context.get_action_handler("send_slack_notification")
    result = handler(context, "Test Slack")

    assert "curl" in result
    assert "Test Slack" in result
```

### Tests E2E

```bash
# Compiler et tester le plugin
python -m shtest_compiler.run_all --input tests/notification_test.shtest

# Vérifier la syntaxe
python src/verify_syntax.py tests/notification_test.shtest

# Exécuter le script généré
bash output/notification_test.sh
```

## Étape 9 : Déployer votre Plugin

### Installation

1. **Copier le plugin** dans le répertoire des plugins :
```bash
cp -r src/shtest_compiler/plugins/notification /path/to/knightbatch/plugins/
```

2. **Enregistrer le plugin** dans la configuration principale :
```yaml
# config/plugins.yml
plugins:
  - notification
  - file
  - sql
```

3. **Configurer les variables** d'environnement :
```bash
export SLACK_WEBHOOK_URL="your_webhook_url"
export NOTIFICATION_TYPE="slack"
```

### Utilisation

```shtest
# Exemple d'utilisation du plugin
Étape: Notifier le succès d'un test
  Action: Exécuter le script: ./my_test.sh
  Vérifier: Le code de retour est 0
  Action: Envoyer une notification: Test réussi - $(date)
  Vérifier: La notification a été envoyée
```

## Bonnes Pratiques

### Conception du Plugin

1. **Séparation des responsabilités** : Handlers, matchers, et configuration séparés
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
def database_handler(context: CompileContext, query: str, **kwargs) -> str:
    """Handler pour exécuter des requêtes de base de données."""

    db_url = context.get_variable("DATABASE_URL")
    if not db_url:
        return "echo 'Database URL not configured' >&2 && exit 1"

    return f"""# Exécuter requête base de données
psql "{db_url}" -c "{query}" \\
  && echo "Query executed successfully" \\
  || (echo "Database query failed" >&2 && exit 1)"""
```

### Plugin avec API REST

```python
def api_handler(context: CompileContext, endpoint: str, method: str = "GET", **kwargs) -> str:
    """Handler pour appeler des APIs REST."""

    base_url = context.get_variable("API_BASE_URL")
    api_key = context.get_variable("API_KEY")

    headers = f"-H 'Authorization: Bearer {api_key}'" if api_key else ""

    return f"""# Appel API REST
curl -X {method} {headers} "{base_url}{endpoint}" \\
  && echo "API call successful" \\
  || (echo "API call failed" >&2 && exit 1)"""
```

## Dépannage

### Problèmes Courants

1. **Plugin non trouvé** : Vérifier le chemin et l'enregistrement
2. **Handler non appelé** : Vérifier les patterns YAML
3. **Variables non définies** : Vérifier la configuration
4. **Erreurs de syntaxe** : Vérifier les commandes shell générées

### Debug

```python
# Activer le debug pour le plugin
import logging
logging.basicConfig(level=logging.DEBUG)

# Vérifier l'enregistrement
context = CompileContext()
register_plugin(context)
print("Handlers:", list(context.action_handlers.keys()))
print("Matchers:", list(context.validation_matchers.keys()))
```

## Conclusion

Ce tutoriel vous a guidé à travers la création complète d'un plugin KnightBatch. Les plugins sont un moyen puissant d'étendre les fonctionnalités du système selon vos besoins spécifiques.

Pour plus d'informations, consultez :
- [Architecture Modulaire](modular_architecture.md)
- [Guide Développeur](developer_quickstart.md)
- [Tests et Validation](testing_and_validation.md)