# Créer un plugin pour SHTEST

## 1. Structure recommandée

```
src/shtest_compiler/plugins/mon_plugin/
  mon_plugin.py
  config/
    patterns_mon_plugin.yml
```

## 2. Définir les patterns YAML

Dans `config/patterns_mon_plugin.yml` :
```yaml
patterns:
  ma_categorie:
    - handler: mon_handler
      pattern: "ma regex ici"
```

## 3. Écrire le handler Python

Dans `mon_plugin.py` :
```python
from shtest_compiler.ast.shell_framework_ast import ActionNode

class MonAction(ActionNode):
    def __init__(self, param1, param2):
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
- Le nom du handler doit correspondre à la clé `handler` dans le YAML.
- Le handler reçoit un dictionnaire `params` avec les arguments extraits par la regex.
- **Ne pas utiliser `os.environ` ou des variables globales dans vos handlers.**
- Le handler doit retourner un objet `ActionNode` avec une méthode `to_shell()` pour les actions shell.

## 4. Enregistrer le handler

Le handler est automatiquement enregistré via le système de plugins. Assurez-vous que votre plugin a une structure `PLUGIN_HANDLERS` :

```python
PLUGIN_HANDLERS = {
    "mon_handler": mon_handler,
}
```

## 5. Tester

- Ajoute un test `.shtest` qui utilise une action ou validation de ton plugin.
- Compile/parses pour vérifier que le handler est bien appelé.

## 6. Avantages

- Aucun changement à faire dans le parser ou le cœur du framework.
- Ajout/évolution de patterns et de logique métier totalement découplés.

--- 