"""
Command translator that converts natural language actions into actual shell commands.
"""

import re
from typing import Optional


class CommandTranslator:
    """Translates natural language actions into shell commands."""
    
    def __init__(self):
        # Patterns for different types of actions - using list of tuples to preserve order
        self.patterns = [
            # Variable definitions
            (r"définir la variable (\w+)\s*=\s*(.+)", "export {var}=\"{value}\""),
            
            # Directory creation
            (r"créer le dossier (.+)", "mkdir -p \"{path}\""),
            (r"creer le dossier (.+)", "mkdir -p \"{path}\""),
            (r"faire un dossier (.+)", "mkdir -p \"{path}\""),
            (r"nouveau dossier (.+)", "mkdir -p \"{path}\""),
            
            # File creation
            (r"créer le fichier (.+)", "touch \"{path}\""),
            (r"creer le fichier (.+)", "touch \"{path}\""),
            (r"faire un fichier (.+)", "touch \"{path}\""),
            (r"nouveau fichier (.+)", "touch \"{path}\""),
            
            # File touch with timestamp
            (r"toucher le fichier (.+?)\s+-t\s+(\d+)", "touch -t {timestamp} \"{path}\""),
            (r"mettre à jour la date du fichier (.+?)\s+(\d+)", "touch -t {timestamp} \"{path}\""),
            (r"modifier la date du fichier (.+?)\s+(\d+)", "touch -t {timestamp} \"{path}\""),
            
            # File touch without timestamp
            (r"toucher le fichier (.+)", "touch \"{path}\""),
            (r"mettre à jour la date du fichier (.+)", "touch \"{path}\""),
            (r"modifier la date du fichier (.+)", "touch \"{path}\""),
            
            # File copy
            (r"copier le fichier (.+?)\s+vers\s+(.+)", "cp \"{src}\" \"{dest}\""),
            (r"copier le fichier (.+?)\s+à\s+(.+)", "cp \"{src}\" \"{dest}\""),
            (r"dupliquer le fichier (.+?)\s+vers\s+(.+)", "cp \"{src}\" \"{dest}\""),
            
            # Directory copy
            (r"copier le dossier (.+?)\s+vers\s+(.+)", "cp -r \"{src}\" \"{dest}\""),
            (r"copier le dossier (.+?)\s+à\s+(.+)", "cp -r \"{src}\" \"{dest}\""),
            (r"dupliquer le dossier (.+?)\s+vers\s+(.+)", "cp -r \"{src}\" \"{dest}\""),
            
            # File move
            (r"déplacer le fichier (.+?)\s+vers\s+(.+)", "mv \"{src}\" \"{dest}\""),
            (r"déplacer le fichier (.+?)\s+à\s+(.+)", "mv \"{src}\" \"{dest}\""),
            
            # Directory move
            (r"déplacer le dossier (.+?)\s+vers\s+(.+)", "mv \"{src}\" \"{dest}\""),
            (r"déplacer le dossier (.+?)\s+à\s+(.+)", "mv \"{src}\" \"{dest}\""),
            
            # File deletion
            (r"supprimer le fichier (.+)", "rm \"{path}\""),
            (r"effacer le fichier (.+)", "rm \"{path}\""),
            (r"enlever le fichier (.+)", "rm \"{path}\""),
            
            # Directory deletion
            (r"supprimer le dossier (.+)", "rm -rf \"{path}\""),
            (r"effacer le dossier (.+)", "rm -rf \"{path}\""),
            (r"enlever le dossier (.+)", "rm -rf \"{path}\""),
            
            # Directory purge
            (r"vider le répertoire (.+)", "rm -rf \"{path}\"/*"),
            (r"nettoyer le répertoire (.+)", "rm -rf \"{path}\"/*"),
            (r"purger le répertoire (.+)", "rm -rf \"{path}\"/*"),
            
            # File content display
            (r"afficher le contenu du fichier (.+)", "cat \"{path}\""),
            (r"voir le contenu du fichier (.+)", "cat \"{path}\""),
            (r"lire le fichier (.+)", "cat \"{path}\""),
            (r"consulter le fichier (.+)", "cat \"{path}\""),
            (r"ouvrir le fichier (.+)", "cat \"{path}\""),
            
            # Script execution
            (r"exécuter (.+)", "{script}"),
            (r"executer (.+)", "{script}"),
            (r"lancer (.+)", "{script}"),
            (r"démarrer (.+)", "{script}"),
            (r"faire tourner (.+)", "{script}"),
            
            # SQL script execution
            (r"exécuter le script sql (.+)", "sqlplus -s ${SQL_CONN:-user/password@db} @{script}"),
            (r"executer le script sql (.+)", "sqlplus -s ${SQL_CONN:-user/password@db} @{script}"),
            (r"exécuter le script SQL (.+)", "sqlplus -s ${SQL_CONN:-user/password@db} @{script}"),
            (r"executer le script SQL (.+)", "sqlplus -s ${SQL_CONN:-user/password@db} @{script}"),
            
            # File comparison
            (r"comparer le fichier (.+?)\s+avec\s+(.+)", "diff \"{file1}\" \"{file2}\""),
            (r"comparer le fichier (.+?)\s+et\s+(.+)", "diff \"{file1}\" \"{file2}\""),
        ]
    
    def translate(self, action: str) -> Optional[str]:
        """
        Translate a natural language action into a shell command.
        
        Args:
            action: The natural language action string
            
        Returns:
            The translated shell command, or None if no translation found
        """
        action_lower = action.lower()
        
        for pattern, template in self.patterns:
            match = re.match(pattern, action_lower, re.IGNORECASE)
            if match:
                groups = match.groups()
                
                # Handle different template types
                if "{var}" in template and "{value}" in template:
                    return template.format(var=groups[0], value=groups[1])
                elif "{path}" in template and "{timestamp}" in template:
                    return template.format(path=groups[0], timestamp=groups[1])
                elif "{path}" in template:
                    return template.format(path=groups[0])
                elif "{src}" in template and "{dest}" in template:
                    return template.format(src=groups[0], dest=groups[1])
                elif "{file1}" in template and "{file2}" in template:
                    return template.format(file1=groups[0], file2=groups[1])
                elif "{script}" in template:
                    return template.format(script=groups[0])
                else:
                    # Fallback: use the original action
                    return action
        
        # If no pattern matches, return the original action
        return action


# Global instance
command_translator = CommandTranslator()


def translate_command(action: str) -> str:
    """
    Convenience function to translate a command.
    
    Args:
        action: The natural language action string
        
    Returns:
        The translated shell command
    """
    result = command_translator.translate(action)
    return result if result is not None else action 