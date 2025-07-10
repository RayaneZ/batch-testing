# parser/alias_utils.py

class AliasResolver:
    """
    Classe responsable de résoudre des expressions textuelles
    en validations explicites.
    """
    def __init__(self):
        self.aliases = {
            "identifiants configurés": ["variable SQL_CONN définie"],
            "stdout contient OK": ["stdout.contains('OK')"],
            "stderr vide": ["stderr.contains('')"],
            "fichier vide": ["file.empty(fichier)"],
            "fichier existe": ["file.exists(fichier)"],
        }

    def resolve(self, expression: str) -> list[str]:
        """
        Résout une expression en une ou plusieurs validations concrètes.

        :param expression: Expression naturelle
        :return: Liste de validations normalisées
        """
        return self.aliases.get(expression.strip().lower(), [expression.strip()])
