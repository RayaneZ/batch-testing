#!/bin/sh

set -e



run_cmd() {

  local _stdout=$(mktemp)

  local _stderr=$(mktemp)

  /bin/sh -c "$1" >"$_stdout" 2>"$_stderr"

  last_ret=$?

  last_stdout=$(cat "$_stdout")

  last_stderr=$(cat "$_stderr")

  rm -f "$_stdout" "_stderr"

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



# ---- Step 1 - Preparation ----

run_cmd "mkdir -p ./qualification/demo_env"

# Validations globales:

# Erreur parsing validation: Aucune règle de validation ne correspond à : le dossier est cree

# Attendu : le dossier est cree

echo "[ERREUR] Aucun matcher trouvé pour: 'le dossier est cree'" 1>&2

actual="non vérifié"

expected="le dossier est cree"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi

run_cmd "touch ./qualification/demo_env/initial.txt"

# Validations globales:

# Erreur parsing validation: Aucune règle de validation ne correspond à : le fichier est cree

# Attendu : le fichier est cree

echo "[ERREUR] Aucun matcher trouvé pour: 'le fichier est cree'" 1>&2

actual="non vérifié"

expected="le fichier est cree"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond3=1; else cond3=0; fi

export SQL_CONN=rootme/ffDDD584R@base_name

# Validations globales:

# Erreur parsing validation: Aucune règle de validation ne correspond à : Les identifiants sont configurés

# Attendu : Les identifiants sont configurés

if [ $last_ret -eq 0 ]; then actual="Identifiants configurés"; else actual="Identifiants non configurés"; fi

expected="Identifiants configurés"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond5=1; else cond5=0; fi

# ---- Step 2 - Ancien fichier ----

run_cmd "touch -t 202201010000 ./qualification/demo_env/old.txt"

# Validations globales:

# Erreur parsing validation: Aucune règle de validation ne correspond à : date modifiee

# Attendu : date modifiee

if [ $last_ret -eq 0 ]; then actual="date modifiée"; else actual="date inchangée"; fi

expected="date modifiée"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond7=1; else cond7=0; fi

# ---- Step 3 - Nouveau fichier ----

run_cmd "touch ./qualification/demo_env/newfile.txt"

# Validations globales:

# Erreur parsing validation: Aucune règle de validation ne correspond à : fichier crée

# Attendu : fichier crée

if [ $last_ret -eq 0 ]; then actual="fichier créé"; else actual="échec création"; fi

expected="fichier créé"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond9=1; else cond9=0; fi

run_cmd "touch -t 202401010101 ./qualification/demo_env/newfile.txt"

# Validations globales:

# Erreur parsing validation: Aucune règle de validation ne correspond à : date modifiee

# Attendu : date modifiee

if [ $last_ret -eq 0 ]; then actual="date modifiée"; else actual="date inchangée"; fi

expected="date modifiée"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond11=1; else cond11=0; fi

# ---- Step 4 - Execution du batch ----

run_cmd "./qualification/purge.sh"

# Validations globales:

# Erreur parsing validation: Aucune règle de validation ne correspond à : la sortie standard contient "Succès complet"

# Attendu : Le script retourne un code 0

echo "[ERREUR] Aucun matcher trouvé pour: 'Le script retourne un code 0'" 1>&2

actual="non vérifié"

expected="Le script retourne un code 0"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond14=1; else cond14=0; fi

# Attendu : la sortie standard contient "Succès complet"

echo "[ERREUR] Aucun matcher trouvé pour: 'la sortie standard contient "Succès complet"'" 1>&2

actual="non vérifié"

expected="la sortie standard contient "Succès complet""

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond15=1; else cond15=0; fi

# Attendu : la sortie d'erreur contient WARNING

echo "[ERREUR] Aucun matcher trouvé pour: 'la sortie d'erreur contient WARNING'" 1>&2

actual="non vérifié"

expected="la sortie d'erreur contient WARNING"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond16=1; else cond16=0; fi

if [ ${cond15} -eq 1 ] || [ ${cond16} -eq 1 ]; then cond17=1; else cond17=0; fi

if [ ${cond14} -eq 1 ] && [ ${cond17} -eq 1 ]; then cond18=1; else cond18=0; fi

run_cmd "/opt/batch/migration.sh"

# Validations globales:

if [ $last_ret -eq 0 ]; then cond19=1; else cond19=0; fi

# Attendu : Le script retourne un code 0

echo "[ERREUR] Aucun matcher trouvé pour: 'Le script retourne un code 0'" 1>&2

actual="non vérifié"

expected="Le script retourne un code 0"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond20=1; else cond20=0; fi

# ---- Step 5 - Vérifier la table en base ----

run_cmd "le script SQL verification.sql"

# Validations globales:

# Erreur parsing validation: Aucune règle de validation ne correspond à : Le script s'execute avec succès

# Attendu : Le script s'execute avec succès

if [ $last_ret -eq 0 ]; then actual="Script exécuté avec succès"; else actual="Échec d'exécution du script"; fi

expected="Script exécuté avec succès"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond22=1; else cond22=0; fi

run_cmd "diff ./output.txt ./output_attendu.txt"

# Validations globales:

# Erreur parsing validation: Aucune règle de validation ne correspond à : Les fichiers sont identiques

# Attendu : Les fichiers sont identiques

echo "[ERREUR] Aucun matcher trouvé pour: 'Les fichiers sont identiques'" 1>&2

actual="non vérifié"

expected="Les fichiers sont identiques"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond24=1; else cond24=0; fi