<p align="center" style="background:#fff">
  <img src="logo.png" alt="KnightBatch logo" width="200"/>
</p>

# KnightBatch - Shell Test Compiler

Ce projet permet de convertir des scénarios `.shtest` en scripts shell exécutables.  
Il comprend une CLI Python et une extension VS Code pour l’écriture de scénarios compréhensibles de type "Action / Résultat".

---

## 🚀 Installation

Assurez-vous d’avoir Python 3.8 ou supérieur.

```bash
python -m venv venv
source venv/bin/activate  # ou `venv\Scripts\activate` sous Windows

pip install -e .
```

> Cela installe la commande `shtest` accessible dans le terminal.

---

## 🛠 Commandes principales

### `compile_expr`

Compile une expression logique de validation :

```bash
shtest compile_expr 'stdout contient OK' --verbose
```

- Affiche les instructions shell générées
- Utilise le parseur et compilateur d'expressions logiques

---

### `compile_file`

Compile un seul fichier `.shtest` en script `.sh`.

```bash
shtest compile_file tests/exemple.shtest --output output/exemple.sh --verbose
```

---

### `generate`

Compile tous les fichiers `.shtest` dans un dossier :

```bash
shtest generate src/tests output/
```

- Génére un fichier `.sh` par scénario `.shtest`
- Crée le dossier `output/` s'il n'existe pas

---

## 📁 Structure des dossiers

```
src/
├── shtest_compiler/
│   ├── compiler/
│   ├── parser/
│   ├── templates/
│   ├── shtest.py
│   └── ...
tests/
output/
```

---

## 🧪 Exemple de scénario `.shtest`

```text
Etant donné le script SQL init.sql
Quand j'exécute le batch process.sh
Alors stdout contient OK
```

---

## 🧩 VS Code Extension

Le dossier `vscode/` contient une extension minimale pour `.shtest`.  
Pour l’installer :

```bash
cd vscode
npm install
npx vsce package
```

Puis installe le `.vsix` dans Visual Studio Code.

---

## 📄 License

Ce projet est publié sous licence MIT.
