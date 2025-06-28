# Guide des règles de reconnaissance (Regex)

Ce document décrit les expressions régulières utilisées pour interpréter automatiquement les instructions d’un scénario `.shtest`.

Chaque ligne de scénario peut déclencher une **action**, une **définition de variable**, ou une **validation de résultat**. Les regex permettent de les reconnaître.

---

## 💡 Exemples simples

```text
Action: exécuter le script setup.sql ; Résultat: retour 0
Action: créer le fichier /tmp/test.log ; Résultat: le fichier est présent
Action: définir la variable ENV = prod
```

---

## 🛠️ Actions reconnues

Ces expressions déclenchent des actions de script ou de préparation.

### Exécution de scripts

```text
exécuter mon_script.sql
lancer clean.sh
traiter le script init.sh
```

Reconnaît :
- `.sql` → exécution SQL
- `.sh` → script shell
- toute action sans extension → générique

### Initialisation

```text
initialiser les paramètres
configurer l’environnement
```

---

## 🧾 Variables et arguments

```text
définir la variable ENV = prod
définir la variable port = 5432
```

Les variables sont extraites et injectées dans les scripts générés.

---

## 📁 Fichiers et dossiers

### Création

```text
créer le fichier = /etc/app.conf
créer le dossier = /var/data
```

Avec droits :
```text
créer dossier = /tmp/logs avec les droits = 0755
```

### Touch / Date

```text
mettre à jour la date du fichier /tmp/test.txt 20250628143000
touch /tmp/file.log -t 20250628120000
```

### Lecture

```text
lire le fichier = /etc/hosts
```

### Copie / Déplacement

```text
copier le fichier /tmp/a vers /var/b
déplacer le dossier /data vers /backup
```

---

## ✅ Résultats attendus

Ces expressions servent à valider l’état après une action.

```text
le script retourne un code 0
le script affiche un code "1"
la sortie standard est success
la sortie d’erreur contient erreur fatale
```

Alias pris en charge :
- `retour 0` = le script a bien été exécuté
- `stdout contient "..."`, `stderr=...`

### Autres validations

```text
le fichier /tmp/x existe
le dossier est prêt
le fichier est initialisé
les identifiants sont configurés
```

---

## 🔗 Compatibilités Action ↔ Résultat

### Exemples

```text
Action: exécuter init.sql ; Résultat: retour 0
Action: créer le fichier /etc/app.conf ; Résultat: le fichier est présent
Action: définir la variable mode = debug ; Résultat: identifiants configurés
```

Chaque action a des résultats compatibles automatiquement reconnus.

---

Pour plus de détails, consultez les fichiers de configuration du moteur de parsing.
