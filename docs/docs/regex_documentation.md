# 🔄 Compatibilité entre Actions et Résultats

Cette section décrit, pour chaque **action**, les **résultats** compatibles attendus.

## 1. Exécution de Scripts

### Action :
- `exécuter.*?\\.sql`
- `(?:exécuter|lancer|traiter)`
- `(?:exécuter|lancer|traiter)\\s+(\\S+\\.sh)`

### Résultats compatibles :
- `le script retourne un code`
- `le script affiche un code`
- `le script s'exécute avec succès`
- `stdout contient ...`
- `stdout=...`
- `stderr=...`
- `retour 0`
- `aucun message d'erreur`

---

## 2. Définition de Variables

### Action :
- `définir la variable ...`

### Résultats compatibles :
- `identifiants configurés`

---

## 3. Fichiers

### Action :
- `créer le fichier ...`
- `fichier créé`
- `mettre à jour la date du fichier`
- `touch ...`

### Résultats compatibles :
- `le fichier est présent`
- `le fichier ... existe`
- `fichier créé`
- `le fichier est initialisé`

---

## 4. Dossiers

### Action :
- `créer le dossier ...`
- `dossier créé`
- `vider/purger le dossier`

### Résultats compatibles :
- `le dossier est prêt`
- `le dossier est copié`
- `le dossier est créé`

---

## 5. Comparaison de fichiers

### Action :
- `comparer le fichier A avec B`

### Résultats compatibles :
- `le fichier A est identique à B`
- `les fichiers sont identiques`

---

## 6. Déplacement et copie

### Action :
- `copier|déplacer fichier|dossier`

### Résultats compatibles :
- `le fichier est copié`
- `le dossier est copié`
- `le fichier est présent`

---

## 7. Lecture de fichiers

### Action :
- `lire/afficher/cat le fichier`

### Résultats compatibles :
- `le contenu est affiché`
- `le contenu est lisible`
- `contenu correct`

---

## 8. Logs

### Action :
- `logs|fichiers de logs`
- `chemin des logs = ...`

### Résultats compatibles :
- `les logs sont accessibles`
- `aucun message d'erreur`
- `le fichier ... existe`

---

## 9. Validation et Résultat

### Action :
- `valider que ...`
- `résultat : ...`

### Résultats compatibles :
- `stdout=...`
- `stderr=...`
- `retour ...`
- `identifiants configurés`
- `base prête`