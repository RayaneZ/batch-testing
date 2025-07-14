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
def mon_handler(actions, *args):
    # Implémente la logique de ton plugin ici
    pass
```
- Le nom du handler doit correspondre à la clé `handler` dans le YAML.
- Le handler reçoit le dictionnaire d’actions et les arguments extraits par la regex.

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