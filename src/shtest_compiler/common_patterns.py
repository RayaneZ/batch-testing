# Description générale : ce module charge des motifs regex communs à partir de fichiers YAML de configuration.
"""Common regex patterns loaded from ``regex_config.yml``."""

# Permet d'utiliser certaines fonctionnalités futures de Python (comme les annotations de type différées)
from __future__ import annotations

# Importation de modules standards
import os  # Pour manipuler les chemins de fichiers
import re  # Pour la gestion des expressions régulières
import yaml  # Pour lire des fichiers YAML
from typing import List, Dict

# Chemin vers le fichier de configuration principal contenant les motifs regex
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "regex_config.yml")

# Chemin vers un fichier YAML supplémentaire avec des règles simples
SIMPLE_RULES_PATH = os.path.join(os.path.dirname(__file__), "simple_rules.yml")

# Chargement des motifs regex depuis le fichier YAML
with open(CONFIG_PATH, encoding="utf-8") as f:
    _PATTERNS = yaml.safe_load(
        f
    )  # _PATTERNS est un dictionnaire contenant les motifs regex nommés

# Chargement d'une liste de règles simples depuis un autre fichier YAML
with open(SIMPLE_RULES_PATH, encoding="utf-8") as f:
    SIMPLE_RULES: List[Dict[str, str]] = yaml.safe_load(f)

# Compilation des motifs regex à partir des valeurs du fichier YAML, avec l'option insensible à la casse
STEP_RE = re.compile(
    _PATTERNS["step"], re.IGNORECASE
)  # Pour détecter les lignes de type étape
ACTION_RESULT_RE = re.compile(
    _PATTERNS["action_result"], re.IGNORECASE
)  # Pour les lignes avec action + résultat
ACTION_ONLY_RE = re.compile(
    _PATTERNS["action_only"], re.IGNORECASE
)  # Pour les lignes contenant uniquement une action
RESULT_ONLY_RE = re.compile(
    _PATTERNS["result_only"], re.IGNORECASE
)  # Pour les lignes contenant uniquement un résultat
COMMENT_RE = re.compile(
    _PATTERNS["comment"], re.IGNORECASE
)  # Pour détecter les commentaires

LINE_FORMATS = _PATTERNS.get("line_formats", {})
VALIDATION_KEY = _PATTERNS.get("validation_key", "validation")
TOKEN_TYPES = list(_PATTERNS.keys())  # ['step', 'action_result', ...]
