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
            (r"définir la variable (\w+)\s*=\s*['\"]?([^'\"]+)['\"]?", "export {var}={value}"),
            
            # Directory creation
            (r"cr[ée]er le dossier\s+['\"]?([^'\"]+)['\"]?", "mkdir -p {path}"),
            (r"faire un dossier\s+['\"]?([^'\"]+)['\"]?", "mkdir -p {path}"),
            (r"nouveau dossier\s+['\"]?([^'\"]+)['\"]?", "mkdir -p {path}"),
            
            # File creation
            (r"cr[ée]er le fichier\s+['\"]?([^'\"]+)['\"]?", "touch {path}"),
            (r"faire un fichier\s+['\"]?([^'\"]+)['\"]?", "touch {path}"),
            (r"nouveau fichier\s+['\"]?([^'\"]+)['\"]?", "touch {path}"),
            
            # File touch with timestamp
            (r"toucher le fichier\s+['\"]?([^'\"]+)['\"]?\s+-t\s+(\d+)", "touch -t {timestamp} {path}"),
            (r"mettre à jour la date du fichier\s+['\"]?([^'\"]+)['\"]?\s+(\d+)", "touch -t {timestamp} {path}"),
            (r"modifier la date du fichier\s+['\"]?([^'\"]+)['\"]?\s+(\d+)", "touch -t {timestamp} {path}"),
            
            # File touch without timestamp
            (r"toucher le fichier\s+['\"]?([^'\"]+)['\"]?", "touch {path}"),
            (r"mettre à jour la date du fichier\s+['\"]?([^'\"]+)['\"]?", "touch {path}"),
            (r"modifier la date du fichier\s+['\"]?([^'\"]+)['\"]?", "touch {path}"),
            
            # File copy
            (r"copier le fichier\s+['\"]?([^'\"]+)['\"]?\s+vers\s+['\"]?([^'\"]+)['\"]?", "cp {src} {dest}"),
            (r"copier le fichier\s+['\"]?([^'\"]+)['\"]?\s+à\s+['\"]?([^'\"]+)['\"]?", "cp {src} {dest}"),
            (r"dupliquer le fichier\s+['\"]?([^'\"]+)['\"]?\s+vers\s+['\"]?([^'\"]+)['\"]?", "cp {src} {dest}"),
            
            # Directory copy
            (r"copier le dossier\s+['\"]?([^'\"]+)['\"]?\s+vers\s+['\"]?([^'\"]+)['\"]?", "cp -r {src} {dest}"),
            (r"copier le dossier\s+['\"]?([^'\"]+)['\"]?\s+à\s+['\"]?([^'\"]+)['\"]?", "cp -r {src} {dest}"),
            (r"dupliquer le dossier\s+['\"]?([^'\"]+)['\"]?\s+vers\s+['\"]?([^'\"]+)['\"]?", "cp -r {src} {dest}"),
            
            # File move
            (r"déplacer le fichier\s+['\"]?([^'\"]+)['\"]?\s+vers\s+['\"]?([^'\"]+)['\"]?", "mv {src} {dest}"),
            (r"déplacer le fichier\s+['\"]?([^'\"]+)['\"]?\s+à\s+['\"]?([^'\"]+)['\"]?", "mv {src} {dest}"),
            
            # Directory move
            (r"déplacer le dossier\s+['\"]?([^'\"]+)['\"]?\s+vers\s+['\"]?([^'\"]+)['\"]?", "mv {src} {dest}"),
            (r"déplacer le dossier\s+['\"]?([^'\"]+)['\"]?\s+à\s+['\"]?([^'\"]+)['\"]?", "mv {src} {dest}"),
            
            # File deletion
            (r"supprimer le fichier\s+['\"]?([^'\"]+)['\"]?", "rm {path}"),
            (r"effacer le fichier\s+['\"]?([^'\"]+)['\"]?", "rm {path}"),
            (r"enlever le fichier\s+['\"]?([^'\"]+)['\"]?", "rm {path}"),
            
            # Directory deletion
            (r"supprimer le dossier\s+['\"]?([^'\"]+)['\"]?", "rm -rf {path}"),
            (r"effacer le dossier\s+['\"]?([^'\"]+)['\"]?", "rm -rf {path}"),
            (r"enlever le dossier\s+['\"]?([^'\"]+)['\"]?", "rm -rf {path}"),
            
            # Directory purge
            (r"vider le répertoire\s+['\"]?([^'\"]+)['\"]?", "rm -rf {path}/*"),
            (r"nettoyer le répertoire\s+['\"]?([^'\"]+)['\"]?", "rm -rf {path}/*"),
            (r"purger le répertoire\s+['\"]?([^'\"]+)['\"]?", "rm -rf {path}/*"),
            
            # File content display
            (r"afficher le contenu du fichier\s+['\"]?([^'\"]+)['\"]?", "cat {path}"),
            (r"voir le contenu du fichier\s+['\"]?([^'\"]+)['\"]?", "cat {path}"),
            (r"lire le fichier\s+['\"]?([^'\"]+)['\"]?", "cat {path}"),
            (r"consulter le fichier\s+['\"]?([^'\"]+)['\"]?", "cat {path}"),
            (r"ouvrir le fichier\s+['\"]?([^'\"]+)['\"]?", "cat {path}"),
            
            # Script execution
            (r"ex[ée]cuter\s+['\"]?([^'\"]+)['\"]?", "{script}"),
            (r"lancer\s+['\"]?([^'\"]+)['\"]?", "{script}"),
            (r"démarrer\s+['\"]?([^'\"]+)['\"]?", "{script}"),
            (r"faire tourner\s+['\"]?([^'\"]+)['\"]?", "{script}"),
            
            # SQL script execution
            (r"ex[ée]cuter le script sql\s+['\"]?([^'\"]+)['\"]?", "sqlplus -s ${SQL_CONN:-user/password@db} @{script}"),
            (r"ex[ée]cuter le script SQL\s+['\"]?([^'\"]+)['\"]?", "sqlplus -s ${SQL_CONN:-user/password@db} @{script}"),
            
            # File comparison
            (r"comparer le fichier\s+['\"]?([^'\"]+)['\"]?\s+avec\s+['\"]?([^'\"]+)['\"]?", "diff {file1} {file2}"),
            (r"comparer le fichier\s+['\"]?([^'\"]+)['\"]?\s+et\s+['\"]?([^'\"]+)['\"]?", "diff {file1} {file2}"),
        ]
    
    def _strip_quotes(self, s):
        return s.strip().strip('"').strip("'")

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
                groups = tuple(self._strip_quotes(g) for g in match.groups())
                
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