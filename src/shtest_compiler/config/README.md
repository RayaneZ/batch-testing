
# 🧩 Hybrid Pattern Integration (YAML + Python)

Ce dossier contient un système hybride permettant de gérer dynamiquement des règles textuelles pour votre parser SHTEST.

---

## 📁 Contenu

### `patterns_hybrid.yml`
Définit une liste de `patterns` regroupés par catégorie (`argument`, `execution`, `validation`), chacun lié à un `handler` par son nom.

### `rule_registry_hybrid.py`
- Charge les patterns depuis le fichier YAML
- Associe chaque `pattern` à une fonction Python (`HANDLERS`)
- Fournit une fonction `load_rules()` qui retourne une liste de `(pattern, handler)`

---

## 🔧 Intégration dans `parser.py`

1. Importer la fonction :
```python
from rule_registry_hybrid import load_rules
```

2. Utiliser les règles dans le parser :
```python
self.rules = [Rule(pattern=p, handler=h) for p, h in load_rules()]
```

---

## ✅ Exemple d’expression reconnue

```text
paramètre db=prod
j'exécute le script run.sh
stdout contient OK
```

---

## 💡 Avantages

- Les `patterns` sont centralisés dans un fichier YAML facilement éditable
- La logique métier est testable et maintenue en Python
- Aucun changement à faire dans le parser si tu ajoutes un nouveau motif YAML + handler

