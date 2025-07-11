# parser/alias_utils.py

import yaml
import os
import re

class AliasResolver:
    """
    Classe responsable de résoudre des expressions textuelles
    en validations explicites, en chargeant les alias depuis un fichier YAML.
    """
    def __init__(self):
        # Chemin du fichier d'alias
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, 'config', 'aliases.yml')
        self.aliases = {}
        try:
            with open(config_path, encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict):
                    self.aliases = {k.strip().lower(): v for k, v in data.items()}
        except Exception as e:
            # Fallback minimal si le fichier n'existe pas ou est mal formé
            self.aliases = {}

    def resolve(self, expression: str) -> list[str]:
        """
        Résout une expression en une ou plusieurs validations concrètes.
        :param expression: Expression naturelle
        :return: Liste de validations normalisées
        """
        normalized = expression.strip().lower()
        
        # Vérifier d'abord les correspondances exactes
        if normalized in self.aliases:
            resolved = self.aliases[normalized]
            if isinstance(resolved, list):
                return resolved
            return [resolved]
        
        # Gérer les expressions avec paramètres dynamiques
        # Pattern: "la sortie standard contient "paramètre""
        stdout_pattern = r'la sortie standard contient "([^"]+)"'
        match = re.match(stdout_pattern, normalized)
        if match:
            param = match.group(1)
            return [f'stdout contient "{param}"']
        
        # Pattern: "la sortie d'erreur contient paramètre"
        stderr_pattern = r'la sortie d\'erreur contient (.+)'
        match = re.match(stderr_pattern, normalized)
        if match:
            param = match.group(1).strip('"')
            return [f'stderr contient {param}']
        
        # Pattern: "le script affiche un code "paramètre""
        code_pattern = r'le script affiche un code "([^"]+)"'
        match = re.match(code_pattern, normalized)
        if match:
            param = match.group(1)
            return [f'stdout contient "{param}"']
        
        # Aucune correspondance trouvée
        return [expression.strip()]
