import re

def parse_test_in_natural_language(test_description):
    """
    Cette fonction analyse la description en langage naturel du test et 
    extrait les étapes nécessaires pour créer un playbook Ansible, y compris 
    les chemins des fichiers logs, les scripts SQL, les commandes touch pour les dates,
    et l'action pour afficher le contenu d'un fichier.
    """
    actions = {
        "initialization": [],
        "execution": [],
        "validation": [],
        "logs_check": [],
        "arguments": {},
        "log_paths": [],
        "sql_scripts": [],
        "file_operations": [],
        "cat_files": []  # Pour l'action cat (afficher le contenu d'un fichier)
    }

    # Expressions régulières pour détecter les actions
    if re.search(r"(initialiser|créer|configurer)", test_description, re.IGNORECASE):
        actions["initialization"].append(test_description)

    if re.search(r"(exécuter|lancer|traiter)", test_description, re.IGNORECASE):
        actions["execution"].append(test_description)

    if re.search(r"(vérifier|valider)", test_description, re.IGNORECASE):
        actions["validation"].append(test_description)

    if re.search(r"(logs|erreurs|fichiers de logs)", test_description, re.IGNORECASE):
        actions["logs_check"].append(test_description)

    # Recherche des arguments pour le batch
    match = re.search(r"(argument|paramètre) (.*)=(.*)", test_description)
    if match:
        actions["arguments"][match.group(2).strip()] = match.group(3).strip()

    # Recherche des chemins de logs spécifiés dans le test
    log_paths_matches = re.findall(r"(chemin|path) des logs\s*=\s*(\S+)", test_description, re.IGNORECASE)
    if log_paths_matches:
        actions["log_paths"] = [path for _, path in log_paths_matches]

    # Recherche des scripts SQL pour Oracle
    sql_scripts = re.findall(r"(script sql) = (.*\.sql)", test_description, re.IGNORECASE)
    if sql_scripts:
        actions["sql_scripts"] = [script for _, script in sql_scripts]

    # Recherche des opérations sur les fichiers et dossiers avec les droits Unix
    file_operations = re.findall(r"(créer|mettre à jour) (fichier|dossier)\s*=\s*(\S+)\s*(avec les droits|mode)\s*=\s*(\S+)", test_description, re.IGNORECASE)
    if file_operations:
        actions["file_operations"] = [(op, path, mode) for op, _, path, _, mode in file_operations]

    # Recherche de l'action "cat" (afficher le contenu d'un fichier)
    cat_files = re.findall(r"afficher le contenu du fichier\s*=\s*(\S+)", test_description, re.IGNORECASE)
    if cat_files:
        actions["cat_files"] = cat_files

    return actions

def generate_ansible_playbook_with_args(actions):
    """
    Cette fonction génère un playbook Ansible à partir des actions extraites et des arguments dynamiques.
    Elle inclut aussi la gestion des scripts SQL, la création de fichiers/dossiers avec les droits Unix, 
    les commandes touch, et l'action pour afficher le contenu d'un fichier.
    """
    playbook = """
---
- name: Playbook généré à partir du test en langage naturel avec arguments, scripts SQL, et gestion de fichiers
  hosts: localhost
  tasks:
  """

    # Générer la partie d'initialisation
    if actions["initialization"]:
        playbook += "\n    # Initialisation de l'environnement"
        for action in actions["initialization"]:
            playbook += f"\n    - name: {action}\n      debug:\n        msg: 'Initialisation effectuée'"
    
    # Générer la partie d'exécution avec arguments
    if actions["execution"]:
        playbook += "\n    # Exécution du batch avec des arguments"
        for action in actions["execution"]:
            arg_str = ' '.join([f'{key}={value}' for key, value in actions["arguments"].items()])
            playbook += f"\n    - name: {action}\n      command: './process_batch.sh {arg_str}'"
    
    # Générer la partie de validation
    if actions["validation"]:
        playbook += "\n    # Validation des résultats"
        for action in actions["validation"]:
            playbook += f"\n    - name: {action}\n      assert:\n        that:\n          - result == 'OK'"
    
    # Générer la vérification des logs avec chemins spécifiés
    if actions["logs_check"]:
        playbook += "\n    # Vérification des logs"
        for log_path in actions["log_paths"]:
            playbook += f"\n    - name: Vérifier les erreurs dans les logs {log_path}\n      shell: grep 'ERROR' {log_path}"

    # Générer l'exécution des scripts SQL pour Oracle
    if actions["sql_scripts"]:
        playbook += "\n    # Exécution des scripts SQL"
        for script in actions["sql_scripts"]:
            playbook += f"\n    - name: Exécuter le script SQL {script}\n      command: 'sqlplus -S user/password@db @{script}'"
    
    # Générer la création des fichiers/dossiers avec les droits Unix et mise à jour de date avec touch
    if actions["file_operations"]:
        playbook += "\n    # Création de fichiers et dossiers avec les droits Unix et mise à jour de date avec touch"
        for operation, path, mode in actions["file_operations"]:
            if "dossier" in operation.lower():
                playbook += f"\n    - name: Créer le dossier {path} avec les droits {mode}\n      file:\n        path: {path}\n        state: directory\n        mode: '{mode}'"
            if "fichier" in operation.lower():
                playbook += f"\n    - name: Créer le fichier {path} avec les droits {mode}\n      file:\n        path: {path}\n        state: touch\n        mode: '{mode}'"
            playbook += f"\n    - name: Mettre à jour la date du fichier {path}\n      shell: touch {path}"

    # Ajouter l'action "afficher le contenu du fichier"
    if actions["cat_files"]:
        playbook += "\n    # Afficher le contenu du fichier"
        for file in actions["cat_files"]:
            playbook += f"\n    - name: Afficher le contenu du fichier {file}\n      shell: cat {file}"

    playbook += "\n"

    return playbook

def main():
    # Exemple de test en langage naturel avec des arguments dynamiques, des chemins de logs, SQL, opérations de fichiers et cat
    test_description = """
    Initialiser la base de données avec des données de test en exécutant le script JDD_Commun.sql.
    Afficher le contenu du fichier = /tmp/JDD_Commun.sql
    Vérifier que les données ont été correctement insérées dans la base de données.
    """

    # Étape 1 : Analyser la description du test
    actions = parse_test_in_natural_language(test_description)
    
    # Étape 2 : Générer le playbook Ansible
    playbook = generate_ansible_playbook_with_args(actions)
    
    # Étape 3 : Afficher le playbook généré
    print(playbook)

if __name__ == "__main__":
    main()
