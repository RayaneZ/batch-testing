# Format YAML des patterns d'actions et validations

Depuis la version X, le système de compilation shtest utilise une structure YAML centralisée pour décrire toutes les actions et validations reconnues, avec :
- **Phrase canonique** : la formulation de référence (utilisée pour l'export, la documentation, etc.)
- **Handler** : le nom du handler Python (plugin) qui implémente la logique
- **Alias** : toutes les variantes acceptées, y compris des regex (pour matcher des commandes shell ou des formulations libres)

## Exemple de structure YAML (actions)
```yaml
actions:
  - phrase: "Créer le dossier {path}"
    handler: create_dir
    aliases:
      - "créer un dossier {path}"
      - "faire un dossier {path}"
      - "nouveau dossier {path}"
      - "cr[ée]er le dossier (.+)"   # regex
      - "^mkdir (.+)$"               # regex
  - phrase: "Supprimer le fichier {path}"
    handler: delete_file
    aliases:
      - "effacer le fichier {path}"
      - "^rm (.+)$"                  # regex
```

## Exemple de structure YAML (validations)
```yaml
validations:
  - phrase: "Le contenu est affiché"
    handler: content_displayed
    aliases:
      - "contenu affiché"
      - "Le script est affiché"
      - "^contenu affiché$"
  - phrase: "Retour 0"
    handler: return_0
    aliases:
      - "retour 0"
      - "^retour 0$"
      - "le script retourne un code 0"
```

## Règles sur les alias
- Les alias peuvent être des chaînes exactes ou des regex (préfixées par `^` et/ou suffixées par `$` pour matcher toute la phrase).
- Pour les regex, il est recommandé d'utiliser des guillemets simples dans le YAML pour éviter les problèmes d'échappement.
- Les variables `{path}`, `{src}`, `{dest}`, etc. sont extraites et transmises au handler Python.

## Canonisation et matching
- Lors de la compilation, chaque phrase d'action/validation est d'abord comparée à la phrase canonique (après normalisation).
- Si aucun match exact, chaque alias est testé :
  - D'abord comme chaîne exacte
  - Puis comme regex (avec `re.match`)
- Si un alias matche, la phrase canonique et le handler sont retrouvés, et le bon plugin est appelé.

## Alignement avec les plugins
- Chaque handler du YAML doit exister dans le mapping `PLUGIN_HANDLERS` du plugin concerné.
- Les handlers Python reçoivent les arguments extraits par la regex (via `groups` ou `**kwargs`).
- Toute la logique de matching est centralisée dans le YAML : les plugins ne font que la logique métier.

## Bonnes pratiques
- Ajouter toutes les variantes rencontrées dans les tests comme alias (exact ou regex).
- Utiliser des regex pour couvrir des familles de variantes (ex : `^cat (.+)$` pour toutes les commandes cat).
- Utiliser l'outil `verify_handlers` pour vérifier la cohérence YAML <-> plugins.
- Utiliser la commande `export_to_excel` pour générer une documentation/extraction de toutes les phrases reconnues.

## Exemples d'utilisation

- Compilation d'un test :
  ```sh
  shtest compile_file mon_test.shtest --verbose
  ```
- Vérification de la cohérence YAML/plugins :
  ```sh
  verify_handlers
  ```
- Export des patterns vers Excel :
  ```sh
  export_to_excel src/shtest_compiler/config/patterns_actions.yml src/shtest_compiler/config/patterns_validations.yml output.xlsx
  ``` 