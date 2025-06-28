
# 📄 Scénario de test : demo_long_test

**Fichier test** : `demo_long_test.shtest`  
**Script associé** : `demo_long_test.sh`

---

## 🧩 Étapes du scénario

| Étape        | Action | Résultat attendu |
|--------------|--------|------------------|

| Step 1 - Preparation | Creer le dossier ./qualification/demo_env ;
Creer le fichier ./qualification/demo_env/initial.txt ; | dossier créé
fichier cree |

| Step 2 - Ancien fichier | toucher le fichier ./qualification/demo_env/old.txt -t 202201010000 ; | date modifiee |

| Step 3 - Nouveau fichier | Creer le fichier ./qualification/demo_env/newfile.txt ;
Mettre a jour la date du fichier ./qualification/demo_env/newfile.txt 202401010101 ; | fichier cree
date modifiee |

| Step 4 - Execution du batch | Exécuter ./qualification/purge.sh ;
Exécuter /opt/batch/migration.sh ; | retour 0 et (stdout contient "Succès complet" ou stderr contient WARNING)
retour 0 |

| Step 5 - Vérifier la table en base | Exécuter le script SQL verification.sql ;
Comparer le fichier ./output.txt avec ./output_attendu.txt; | retour 0
les fichiers sont identiques |


---

## 🧷 Commentaires
_Scénario documenté automatiquement depuis `tests_summary.xlsx` et les fichiers de test._