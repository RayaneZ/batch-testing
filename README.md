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
Etape: Step 1 - Preparation
Action: Creer le dossier ./qualification/demo_env
Resultat: le dossier est cree.

Action: Creer le fichier ./qualification/demo_env/initial.txt ; Resultat: le fichier est cree.

Action: Définir la variable SQL_CONN = rootme/ffDDD584R@base_name ; Résultat: Les identifiants sont configurés.


Etape: Step 2 - Ancien fichier
Action: toucher le fichier ./qualification/demo_env/old.txt -t 202201010000 ; Resultat: date modifiee.


Etape: Step 3 - Nouveau fichier
Action: Creer le fichier ./qualification/demo_env/newfile.txt ; Resultat: fichier cree.
Action: Mettre a jour la date du fichier ./qualification/demo_env/newfile.txt 202401010101 ; Resultat: date modifiee.


Etape: Step 4 - Execution du batch
Action: Exécuter ./qualification/purge.sh ; Résultat: Le script retourne un code 0 et (la sortie standard contient "Succès complet" ou la sortie d'erreur contient WARNING).
Action: Exécuter /opt/batch/migration.sh ; Résultat: Le script retourne un code 0.


Step: Step 5 - Vérifier la table en base
Action: Exécuter le script SQL verification.sql ; Résultat: Le script s'execute avec succès.
Action: Comparer le fichier ./output.txt avec ./output_attendu.txt; Résultat: Les fichiers sont identiques
```

---

## Grammaire

```lisp
Programme ::= { Ligne }

Ligne ::= Commentaire
        | Etape
        | LigneActionResultat
        | ActionEtResultatSurDeuxLignes
        | ResultatSeule

Commentaire ::= "#" Texte "\n"

Etape ::= "Step" ":" NomDeStep "\n"

LigneActionResultat ::= "Action" ":" Instruction
                        ";" "Résultat" ":" ExpressionLogique "\n"

ActionEtResultatSurDeuxLignes ::= "Action" ":" [ "\n" ] Instruction "\n"
                                  "Résultat" ":" [ "\n" ] ExpressionLogique "\n"

ResultatSeule ::= "Résultat" ":" [ "\n" ] ExpressionLogique "\n"

NomDeStep ::= Texte
Instruction ::= Texte

ExpressionLogique ::= Terme { OperateurLogique Terme }

Terme ::= ResultatSimple | "(" ExpressionLogique ")"
ResultatSimple ::= Texte

OperateurLogique ::= "et" | "ou"

Texte ::= { Caractere }
Caractere ::= ? tout caractère sauf retour à la ligne ?

```

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
