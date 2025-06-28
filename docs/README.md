# Documentation du projet Batch Testing

Ce dossier contient les fichiers HTML générés ainsi qu'une version 
markdown pour une lecture rapide. Le projet permet d'écrire des 
scénarios de tests en utilisant une syntaxe `Action/Résultat` puis de
les convertir en scripts shell exécutables.

## Démarrage rapide
1. Créez vos scénarios dans `src/tests` au format `.shtest`.
2. Exécutez `python src/generate_tests.py` pour produire des scripts dans `output/`.
3. (Optionnel) Lancez `python src/export_to_excel.py` pour obtenir un
   résumé au format Excel.

Les chemins par défaut peuvent être ajustés dans `config.ini`.

## Outils
- **generate_tests.py** : génère les scripts shell à partir des fichiers `.shtest`.
- **export_to_excel.py** : crée un tableau récapitulatif des scénarios.

Pour plus d'informations, consultez les pages HTML de ce dossier.
