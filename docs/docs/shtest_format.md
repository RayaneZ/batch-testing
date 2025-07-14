# Construire des fichiers `.shtest`

Ce document décrit la syntaxe utilisée pour écrire les scénarios de test automatisés au format `.shtest`.
Chaque instruction est une **ligne unique** au format :

```sh
Action: ... ; Résultat: ...
```

Les validations sont ensuite traduites en instructions exécutables (shell, SQL, etc.).

---

## Entête des fichiers générés
Les fichiers shell générés contiennent tous la base suivante :

```sh
#!/bin/sh
set -e

run_cmd() {
  local _stdout=$(mktemp)
  local _stderr=$(mktemp)
  /bin/sh -c "$1" >"$_stdout" 2>"_stderr"
  last_ret=$?
  last_stdout=$(cat "$_stdout")
  last_stderr=$(cat "$_stderr")
  rm -f "$_stdout" "$_stderr"
  if [ $last_ret -ne 0 ]; then
    echo "STDERR: $last_stderr"
  fi
}

log_diff() {
  expected="$1"
  actual="$2"
  if [ "$expected" != "$actual" ]; then
    echo 'Différence détectée :'
    echo "- Attendu : $expected"
    echo "- Obtenu : $actual"
  fi
}
```

---


## Manipulation SQL

Ce chapitre couvre la configuration de la connexion à une base de données, ainsi que l’exécution de scripts SQL depuis un scénario.

### Définir la connexion à une base de données

Définissez les variables nécessaires pour accéder à une base de données (driver et chaîne de connexion).
KnightBatch utilise les variables réservées `SQL_DRIVER` et `SQL_CONN` pour générer des instructions compatibles avec votre moteur de base de données.
Il est possible de réécrire la variable SQL_DRIVER plusieurs fois dans le même test si vous utilisez plusieurs bases de données.

Pour définir le moteur de base de données :
```text
Action: Définir la variable SQL_DRIVER = mysql ; Résultat: identifiants configurés.
```
Pour définir la chaine de connexion à la base de données :
```text
Action: Définir la variable SQL_CONN = rootme/ffDDD584R@base_name ; Résultat: identifiants configurés.
```

Les lignes ci-dessus sont traduites en shell de la manière suivante :
```sh
export SQL_DRIVER="mysql"
export SQL_CONN="rootme/ffDDD584R@base_name"

# Attendu : identifiants configurés
if [ -n "$SQL_CONN" ]; then actual="identifiants configurés"; else actual="non configuré"; fi

expected="identifiants configurés"
log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
verdict="KO"
if [ ${cond1} -eq 1 ]; then verdict="OK"; fi

expected="OK"
log_diff "$expected" "$verdict"
```

### Exécuter un script en base de données

Il est possible d'exécuter des scripts SQL de la manière suivante :

```text
Action: Exécuter le script SQL ./init_bdd.sql ; Résultat: La base est prête pour le test.
```
Ce qui produira :
```sh
run_cmd "mysql ${SQL_CONN:-user/password@db} < init_bdd.sql"

# Attendu : base prête
if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi

expected="base prête"
log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond2=1; else cond2=0; fi
verdict="KO"
if [ ${cond2} -eq 1 ]; then verdict="OK"; fi

expected="OK"
log_diff "$expected" "$verdict"
```

S'il ne s'agit pas d'une initialisation, il est également possible d'utiliser des alias tels que :
```text
Action: Exécuter le script SQL verification.sql ; Résultat: Le script s’exécute avec succès.
```
Ce qui produira un script similaire :
```sh
run_cmd "mysql ${SQL_CONN:-user/password@db} < verification.sql"

# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi

expected="retour 0"
log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond4=1; else cond4=0; fi
verdict="KO"
if [ ${cond4} -eq 1 ]; then verdict="OK"; fi

expected="OK"
log_diff "$expected" "$verdict"
```

> Note : il est possible d'exporter le résultat d'un `SELECT` dans un fichier afin de le comparer à un résultat attendu à l'aide des actions de manipulation de fichiers.
---

## Manipulation de fichiers

Cette section regroupe toutes les actions relatives à la gestion de fichiers : création, copie, modification de dates.

### Créer et copier des fichiers

Vous pouvez créer des fichiers avec des permissions précises ou les dupliquer dans d'autres emplacements.

```text
Action: Créer le fichier /tmp/test.txt avec les droits 0600 ; Résultat: le fichier est présent.
```
```text
Action: Copier le fichier /tmp/a.txt vers /tmp/b.txt ; Résultat: le fichier est copié.
```

### Modifier les métadonnées d’un fichier

Modifiez les dates de fichiers pour simuler des cas de traitement différé ou obsolète.

```text
Action: Toucher le fichier ./ancien.txt -t 202201010000 ; Résultat: date modifiée.
```
```text
Action: Mettre à jour la date du fichier ./nouveau.txt 202401010101 ; Résultat: date modifiée.
```

---

## Exécution de batchs

Ce chapitre montre comment exécuter des scripts batch et tester leur exécution à travers leurs retours ou leurs sorties.

### Lancer un traitement

Voici des instructions pour lancer un script et valider son exécution correcte.

```text
Action: Exécuter ./scripts/purge.sh ; Résultat: retour 0.
Action: Exécuter /opt/batch/migration.sh ; Résultat: retour 0.
```

### Appliquer des validations complexes

Vous pouvez aussi vérifier les sorties standard ou d'erreur pour affiner les vérifications.

```text
Action: Exécuter ./traitement.sh ; Résultat: retour 0 et stdout contient "Succès complet".
Action: Exécuter ./verif.sh ; Résultat: stderr contient "WARNING".
```

---

## Vérifications

Ces instructions permettent de valider l’exactitude des fichiers produits ou des messages retournés.

### Comparaison de fichiers

Compare deux fichiers pour vérifier que le traitement a produit la sortie attendue.

```text
Action: Comparer le fichier ./resultat.txt avec ./attendu.txt ; Résultat: fichiers identiques.
```

### Vérification de sortie

Assurez-vous que les scripts produisent les bons messages sur la sortie standard ou erreur.

```text
Action: Exécuter ./analyse.sh ; Résultat: stdout contient "Analyse terminée".
Action: Exécuter ./check.sh ; Résultat: stderr contient "Erreur détectée".
```

---

## Gestion des erreurs

Il est important de tester les cas d’erreur, qu’ils soient attendus ou bloquants.

### Vérifier les codes de retour non nuls

```text
Action: Exécuter ./script_noncritique.sh ; Résultat: retour 1.
```

### Capturer des erreurs dans la sortie standard ou erreur

```text
Action: Exécuter ./script.sh ; Résultat: stdout contient "Erreur détectée".
Action: Exécuter ./script.sh ; Résultat: stderr contient "Permission denied".
```

### Combiner erreurs et autres validations

```text
Action: Exécuter ./traitement.sh ; Résultat: retour 1 ou stderr contient "Erreur de validation".
```

---

## Nettoyage des ressources

Les scénarios de test doivent parfois remettre l’environnement dans un état propre.

### Supprimer ou purger un dossier

```text
Action: Supprimer le dossier /tmp/test_env ; Résultat: dossier supprimé.
Action: Purger le contenu du dossier ./temp ; Résultat: dossier vidé.
```

### Réinitialiser un fichier ou une base

```text
Action: Réinitialiser le fichier ./data.json ; Résultat: fichier vide.
Action: Exécuter le script SQL cleanup.sql ; Résultat: base réinitialisée.
```

---

## Catalogue complet des actions

Les exemples ci-dessous récapitulent toutes les actions observées dans le dossier `tests`.
Elles sont classées par thème et accompagnées du résultat attendu.

### Consultation de fichiers
```
Action: Afficher le contenu du fichier /tmp/JDD_Commun.sql ; Résultat: Le contenu est affiché.
Action: Afficher le contenu du fichier /tmp/JDD_Extra.sql ; Résultat: Le script est affiché.
Action: Afficher le contenu du fichier /tmp/file.txt ; Résultat: Le contenu est correct.
Action: Afficher le contenu du fichier /tmp/file.txt ; Résultat: contenu correct.
Action: Afficher le contenu du fichier /tmp/output.txt ; Résultat: Le contenu est correct.
Action: Afficher le contenu du fichier /tmp/test.txt ; Résultat: Le contenu est affiché.
Action: Afficher le contenu du fichier /tmp/test.txt ; Résultat: Le script est affiché.
Action: Afficher le contenu du fichier /tmp/test.txt ; Résultat: contenu affiché.
Action: Afficher le contenu du fichier /tmp/test.txt ; Résultat: le contenu est lisible.
Action: Afficher le contenu du fichier /tmp/test_folder/test.txt ; Résultat: le contenu est lisible.
Action: lire le fichier = /tmp/test.txt ; Résultat: contenu affiché.
Action: cat le fichier = /tmp/test.txt ; Résultat: contenu affiché.
Action: afficher le contenu du fichier /tmp/test.txt ; Résultat: contenu affiché.
```

### Création et copie de fichiers
```
Action: Créer le fichier /tmp/output.txt avec les droits = 0644 ; Résultat: Le fichier est présent.
Action: Créer le fichier /tmp/test_folder/test.txt avec les droits = 0600 ; Résultat: le fichier est créé.
Action: créer le fichier /tmp/test.txt avec les droits = 0600 ; Résultat: Le fichier est présent.
Action: copier le fichier /tmp/a.txt vers /tmp/b.txt ; Résultat: le fichier est copié.
Action: déplacer le fichier /tmp/a.txt vers /tmp/b.txt ; Résultat: le fichier est copié.
Action: Copier le fichier /tmp/src.txt vers /tmp/dest.txt ; Résultat: le fichier est copié.
Action: Copier le dossier /tmp/data vers /tmp/backup ; Résultat: le dossier est copié.
Action: copier le dossier /tmp/dir vers /tmp/dir2 ; Résultat: le dossier est copié.
Action: déplacer le dossier /tmp/dir vers /tmp/dir2 ; Résultat: le dossier est copié.
```

### Gestion des dossiers
```
Action: Créer le dossier /tmp/data avec les droits = 0755 ; Résultat: Le dossier est créé.
Action: Créer le dossier /tmp/newdir ; Résultat: Le dossier est créé.
Action: Créer le dossier /tmp/newdir ; Résultat: dossier créé.
Action: Créer le dossier /tmp/newdir ; Résultat: le dossier est prêt.
Action: Créer le dossier /tmp/test_folder avec les droits = 0700 ; Résultat: le dossier est prêt.
```

### Manipulation de dates
```
Action: Toucher le fichier /tmp/init.flag 202501010000 ; Résultat: Le fichier est initialisé.
Action: toucher le fichier /tmp/test.txt -t 202501010101 ; Résultat: date modifiée.
Action: toucher le fichier /tmp/test.txt -t 202501010101 ; Résultat: date modifiée.
Action: Mettre à jour la date du fichier /tmp/file.txt 202501010101 ; Résultat: La date est modifiée.
Action: Mettre à jour la date du fichier /tmp/file.txt 202501010101 ; Résultat: date modifiée.
Action: Mettre à jour la date du fichier /tmp/output.txt 202501021200 ; Résultat: La date est modifiée.
Action: mettre à jour la date du fichier /tmp/test.txt 202501010101 ; Résultat: date modifiée.
```

### Exécution de scripts et SQL
```
Action: Exécuter /opt/batch/traitement.sh ; Résultat: Le script retourne un code 0 et (La sortie standard contient "OK" ou La sortie d'erreur contient WARNING).
Action: Exécuter /opt/batch/traitement.sh ; Résultat: retour 0 et (la sortie standard contient "Succès complet" ou la sortie d'erreur contient WARNING).
Action: Exécuter /opt/batch/traitement.sh ; Résultat: retour 0 et (stdout contient "OK" ou stderr contient WARNING).
Action: Exécuter /opt/batch/traitement.sh avec l'argument produit=123 et la quantité=10 ; Résultat: retour 0.
Action: Exécuter /opt/batch/traitement.sh avec l'argument produit=567 et la quantité=20 ; Résultat: retour 0 et (stdout contient "Traitement OK" ou stderr contient WARNING).
Action: exécuter traitement.sh ; Résultat: retour 0.
Action: lancer traitement.sh ; Résultat: retour 0.
Action: traiter traitement.sh ; Résultat: retour 0.
Action: exécuter dummy.sh ; Résultat: retour 0.
Action: Exécuter le script SQL JDD_Commun.sql ; Résultat: La base de test est prête.
Action: Exécuter le script SQL JDD_Commun.sql puis JDD_Extra.sql ; Résultat: La base est prête pour le test.
Action: Exécuter script.sh ; Résultat: La base de test est prête.
Action: Exécuter script.sh ; Résultat: La base est prête pour le test.
Action: Exécuter script.sh ; Résultat: Le fichier /tmp/a.txt est identique a /tmp/b.txt.
Action: Exécuter script.sh ; Résultat: Le fichier /tmp/a.txt est identique à /tmp/b.txt.
Action: Exécuter script.sh ; Résultat: base prête.
Action: Exécuter script.sh ; Résultat: fichier_identique /tmp/a.txt /tmp/b.txt.
```

### Paramétrage et contexte
```
Action: Définir la variable SQL_CONN sqlplus -S user/password@db ; Résultat: Les identifiants sont configurés.
Action: Définir la variable SQL_CONN = sqlplus -S user/password@db ; Résultat: identifiants configurés.
Action: Indiquer le chemin des logs /var/log/sys.log ; Résultat: les logs sont accessibles.
Action: Indiquer le chemin des logs /var/log/sys.log ; Résultat: logs accessibles.
Action: Indiquer le chemin des logs /var/log/system.log ; Résultat: les logs sont accessibles.
Action: configurer le contexte ; Résultat: base prête.
Action: créer le contexte ; Résultat: base prête.
Action: initialiser le contexte ; Résultat: base prête.
```

### Vérifications
```
Action: Vérifier qu'aucune erreur n'apparaît ; Résultat: le script affiche un code "030".
Action: Vérifier qu'il n'y a pas d'erreur ; Résultat: aucun message d'erreur.
Action: Vérifier qu'il n'y a pas d'erreur ; Résultat: stderr=.
Action: Vérifier qu'il n'y a pas d'erreurs dans les logs ; Résultat: aucun message d'erreur.
Action: Vérifier que la date du fichier /tmp/test.log est 202501010000 ; Résultat: la date du fichier /tmp/test.log est 202501010000.
Action: Vérifier que le dossier /tmp/testdir a les droits 0755 ; Résultat: le dossier /tmp/testdir a les droits 0755.
Action: Vérifier que le dossier /tmp/testdir contient 2 fichiers *.txt ; Résultat: le dossier /tmp/testdir contient 2 fichiers *.txt.
Action: Vérifier que le dossier /tmp/testdir existe ; Résultat: le dossier /tmp/testdir existe.
Action: Vérifier que le fichier /tmp/dest.txt existe ; Résultat: le fichier /tmp/dest.txt existe ;
Action: Vérifier que le fichier /tmp/dest.txt existe ; Résultat: le fichier est présent et (le fichier /tmp/dest.txt existe ; ou la sortie d'erreur contient "Erreur de copie").
Action: Vérifier que le fichier /tmp/test.log a les droits 0644 ; Résultat: le fichier /tmp/test.log a les droits 0644.
Action: Vérifier que le fichier /tmp/test.log contient OK ; Résultat: le fichier /tmp/test.log contient OK.
Action: Vérifier que le fichier /tmp/test.log contient exactement ALLGOOD ; Résultat: le fichier /tmp/test.log contient exactement ALLGOOD.
Action: Vérifier que le fichier /tmp/test.log existe ; Résultat: le fichier /tmp/test.log existe.
```

### Nettoyage
```
Action: Vider le répertoire /tmp/cache ; Résultat: le dossier est prêt.
```

### Extrait du script généré
Pour illustrer la transformation, toutes ces actions ont été réunies dans un unique fichier `.shtest` puis converties en script shell :

```bash
python src/run_all.py --input docs/catalogue_tests --output docs/catalogue_output --no-excel
```

Les premières lignes du script obtenu sont :

```sh
    }

    # ---- catalogue ----
    run_cmd "cat /tmp/JDD_Commun.sql"
    # Attendu : contenu affiché
    if [ $last_ret -eq 0 ]; then actual="contenu affiché"; else actual="contenu non affiché"; fi
    expected="contenu affiché"
    log_diff "$expected" "$actual"
    if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
    verdict="KO"
    if [ ${cond1} -eq 1 ]; then verdict="OK"; fi
    expected="OK"
    log_diff "$expected" "$verdict"
    run_cmd "cat /tmp/JDD_Extra.sql"
    # Attendu : le script est affiché
    if [ $last_ret -eq 0 ]; then actual="contenu affiché"; else actual="contenu non affiché"; fi
    expected="contenu affiché"
    log_diff "$expected" "$actual"
    if [ "$expected" = "$actual" ]; then cond2=1; else cond2=0; fi
    verdict="KO"
    if [ ${cond2} -eq 1 ]; then verdict="OK"; fi
```

Après amélioration des règles de conversion, toutes les validations sont désormais vérifiées dans le script généré.

## Utilisation de SQL_CONN pour les scripts SQL multi-SGBD

Pour tous les SGBD, la variable d'environnement `SQL_CONN` doit être définie dans le `.shtest` avant toute action SQL. Le format attendu dépend du SGBD sélectionné via `SQL_DRIVER`.

### Exemples d'utilisation dans un `.shtest` :

**Oracle**
```text
Action: Définir la variable SQL_DRIVER = oracle ;
Action: Définir la variable SQL_CONN = user/password@db ;
Action: Exécuter le script SQL mon_script.sql ;
# Commande générée :
#   sqlplus -s user/password@db @mon_script.sql
```

**PostgreSQL**
```text
Action: Définir la variable SQL_DRIVER = postgres ;
Action: Définir la variable SQL_CONN = postgres://user:password@host:5432/dbname ;
Action: Exécuter le script SQL mon_script.sql ;
# Commande générée :
#   psql "postgres://user:password@host:5432/dbname" -f mon_script.sql
```

**MySQL**
```text
Action: Définir la variable SQL_DRIVER = mysql ;
Action: Définir la variable SQL_CONN = mysql://user:password@host:3306/dbname ;
Action: Exécuter le script SQL mon_script.sql ;
# Commande générée :
#   mysql "mysql://user:password@host:3306/dbname" < mon_script.sql
```

**Redis**
```text
Action: Définir la variable SQL_DRIVER = redis ;
Action: Définir la variable SQL_CONN = -h myhost -p 6380 -a mypass ;
Action: Exécuter le script SQL mon_script.redis ;
# Commande générée :
#   redis-cli -h myhost -p 6380 -a mypass < mon_script.redis
```

> **Note :**
> - Il n'est pas nécessaire de générer ou d'exporter SQL_DRIVER dans le shell, il sert uniquement à la génération du script.
> - Adaptez la valeur de SQL_CONN selon le SGBD utilisé.
