# Documentation du projet Batch Testing

Bienvenue sur la documentation officielle de l'outil **Batch Testing**. Ce projet permet d'écrire des scénarios de test simples en français puis de les transformer en scripts shell exécutables.

Les pages suivantes expliquent comment prendre en main l'application et personnaliser son fonctionnement.

## Démarrage rapide

1. Créez vos scénarios dans `src/tests` au format `.shtest`.
2. Exécutez `python src/generate_tests.py` pour produire les scripts dans le dossier `output/`.
3. (Optionnel) Lancez `python src/verify_syntax.py` pour vérifier la syntaxe de vos scénarios.
4. (Optionnel) Utilisez `python src/export_to_excel.py` pour obtenir un tableau récapitulatif.

Les chemins par défaut sont définis dans [`config.ini`](configuration.md).

## Pages importantes
- [Outils en ligne de commande](cli.md)
- [Configuration](configuration.md)
- [Construire les fichiers `.shtest`](shtest_format.md)

Pour consulter l'ancienne documentation HTML, référez-vous aux fichiers présents dans ce même dossier.

