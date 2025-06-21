from parser import Parser


def parse_test_in_natural_language(test_description):
    """Analyse la description du test en utilisant le parseur modulaire."""
    parser = Parser()
    return parser.parse(test_description)

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
