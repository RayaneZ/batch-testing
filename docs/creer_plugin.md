# Créer un plugin pour SHTEST

## 1. Structure recommandée

```
src/shtest_compiler/plugins/mon_plugin/
├── __init__.py
├── config/
│   ├── patterns_actions.yml
│   ├── patterns_validations.yml
│   └── handler_requirements.yml
├── action_handlers/
│   ├── __init__.py
│   └── mon_action.py
└── handlers/
    ├── __init__.py
    └── ma_validation.py
```

## 2. Définir les patterns YAML

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
  - phrase: "Mon action {param1}"
    handler: mon_action
    aliases:
      - "mon action {param1}"
      - "faire {param1}"
      - "^mon action (.+)$"
      - "^faire (.+)$"
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
  - phrase: "Ma validation {param1}"
    handler: ma_validation
    scope: last_action
    aliases:
      - "ma validation {param1}"
      - "vérifier {param1}"
      - "^ma validation (.+)$"
      - "^vérifier (.+)$"
```

### Fichier `config/handler_requirements.yml`
```yaml
# handler_requirements.yml
#
# This file documents the requirements and expected parameters for each handler in the plugin.

mon_action:
  description: "Does something with the given parameter"
  params:
    - name: param1
      type: str
      required: true
      description: "The parameter for the action"

ma_validation:
  description: "Validates something with the given parameter"
  params:
    - name: param1
      type: str
      required: true
      description: "The parameter to validate"
```

## 3. Écrire le handler d'action Python

### Fichier `action_handlers/mon_action.py`
```python
from shtest_compiler.ast.shell_framework_ast import ActionNode

class MonAction(ActionNode):
    def __init__(self, param1, param2="default"):
        self.param1 = param1
        self.param2 = param2

    def to_shell(self):
        # Génère la commande shell correspondante
        return f"echo '{self.param1} {self.param2}' > output.txt"

def handle(params):
    # Le binder garantit que tous les paramètres nécessaires sont présents dans 'params'
    param1 = params["param1"]
    param2 = params.get("param2", "default")
    return MonAction(param1, param2)
```

### Fichier `handlers/ma_validation.py`
```python
from shtest_compiler.ast.shell_framework_ast import ValidationCheck

def handle(params):
    """
    Validation handler: Checks if something is valid.
    """
    param1 = params.get("param1")
    
    # Return atomic command only - no if/then/else logic
    actual_cmd = f"""# Check if {param1} is valid
if [ -f "{param1}" ]; then
    echo "Validation successful"
    exit 0
else
    echo "Validation failed" >&2
    exit 1
fi"""

    return ValidationCheck(
        expected=f"Ma validation {param1}",
        actual_cmd=actual_cmd,
        handler="ma_validation",
        scope="last_action",
        params={"param1": param1}
    )
```

## 4. Point d'entrée du plugin

### Fichier `__init__.py`
```python
"""
Plugin mon_plugin pour le framework KnightBatch.

Ce plugin démontre la nouvelle structure modulaire :
- config/: Fichiers YAML définissant les patterns d'actions et validations
- action_handlers/: Modules Python implémentant les actions
- handlers/: Modules Python implémentant les validations

Pour créer votre propre plugin, copiez cette structure et mettez à jour les fichiers YAML et handlers selon vos besoins.
"""

# Le plugin est automatiquement découvert et chargé par le framework
# Aucun code d'enregistrement supplémentaire n'est nécessaire
```

## 5. Règles importantes

- Le nom du handler doit correspondre à la clé `handler` dans le YAML.
- Le handler reçoit un dictionnaire `params` avec les arguments extraits par la regex.
- **Ne pas utiliser `os.environ` ou des variables globales dans vos handlers.**
- Le handler d'action doit retourner un objet `ActionNode` avec une méthode `to_shell()`.
- Le handler de validation doit retourner un objet `ValidationCheck`.
- Les handlers sont automatiquement enregistrés via le système de plugins.

## 6. Tester

- Ajoute un test `.shtest` qui utilise une action ou validation de ton plugin.
- Compile/parses pour vérifier que le handler est bien appelé.

## 7. Avantages

- Aucun changement à faire dans le parser ou le cœur du framework.
- Ajout/évolution de patterns et de logique métier totalement découplés.
- Structure modulaire claire et extensible.
- Documentation automatique via `handler_requirements.yml`.

## 8. Exemple complet

### Test `.shtest`
```shtest
Étape: Test de mon plugin
  Action: Mon action test.txt
  Résultat: Ma validation test.txt
```

### Compilation
```bash
python src/shtest_compiler/compile_file.py mon_test.shtest
```

### Exécution
```bash
bash mon_test.sh
``` 