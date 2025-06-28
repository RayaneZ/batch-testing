
# 📘 Batch Testing MkDocs

Ce dépôt contient la documentation automatique des tests batch, construite avec [MkDocs](https://www.mkdocs.org/) et le thème Material.

## ▶️ Installation

```bash
pip install mkdocs mkdocs-material pandas jinja2 openpyxl
```

## 🛠️ Génération automatique

```bash
python generate_docs.py
mkdocs serve
```

## 📂 Contenu

- `docs/` : Pages Markdown des scénarios
- `demo_env/` : Fichiers de tests (`.shtest`, logs, scripts)
- `generate_docs.py` : Script de génération des fichiers
