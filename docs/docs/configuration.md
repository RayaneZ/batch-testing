# Configuration

Le fichier `config.ini` situé à la racine du projet permet de définir les chemins par défaut utilisés par les scripts.

```ini
[application]
input_dir = demo_env
output_dir = demo_env
sql_driver = oracle
```

Vous pouvez modifier ces valeurs pour adapter l'outil à votre environnement. La clé `sql_driver` permet de choisir quel moteur SQL utiliser parmi `mysql`, `oracle`, `postgres` ou `redis`. Chaque script dispose également d'options en ligne de commande pour surcharger ces paramètres.

