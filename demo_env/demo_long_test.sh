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

run_cmd "mkdir -p "./qualification/demo_env""

# Attendu : dossier créé

if [ $last_ret -eq 0 ]; then actual="dossier créé"; else actual="échec création"; fi

expected="dossier créé"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond0=1; else cond0=0; fi

run_cmd "touch "./qualification/demo_env/initial.txt""

# Attendu : fichier créé

if [ $last_ret -eq 0 ]; then actual="fichier créé"; else actual="échec création"; fi

expected="fichier créé"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi

run_cmd "export sql_conn="rootme/ffddd584r@base_name""

# Attendu : identifiants configurés

if [ -n "$SQL_CONN" ]; then actual="identifiants configurés"; else actual="non configuré"; fi

expected="identifiants configurés"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond2=1; else cond2=0; fi

# ---- Step 2 - Ancien fichier ----

run_cmd "touch -t 202201010000 "./qualification/demo_env/old.txt""

# Attendu : date modifiée

if [ $last_ret -eq 0 ]; then actual="date modifiée"; else actual="date inchangée"; fi

expected="date modifiée"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond3=1; else cond3=0; fi

# ---- Step 3 - Nouveau fichier ----

run_cmd "touch "./qualification/demo_env/newfile.txt""

# Attendu : fichier cree

if [ $last_ret -eq 0 ]; then actual="fichier créé"; else actual="échec création"; fi

expected="fichier créé"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond4=1; else cond4=0; fi

run_cmd "Mettre a jour la date du fichier ./qualification/demo_env/newfile.txt 202401010101"

# Attendu : date modifiée

if [ $last_ret -eq 0 ]; then actual="date modifiée"; else actual="date inchangée"; fi

expected="date modifiée"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond5=1; else cond5=0; fi

# ---- Step 4 - Execution du batch ----

run_cmd "./qualification/purge.sh"

# Attendu : retour 0

if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi

expected="retour 0"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond6=1; else cond6=0; fi

# Attendu : stdout contient "succès complet"

if echo "$last_stdout" | grep -q 'succès complet'; then actual='succès complet'; else actual=""; fi

expected='succès complet'

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond7=1; else cond7=0; fi

# Attendu : stderr contient warning

if echo "$last_stderr" | grep -q 'warning'; then actual='warning'; else actual=""; fi

expected='warning'

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond8=1; else cond8=0; fi

if [ ${cond7} -eq 1 ] || [ ${cond8} -eq 1 ]; then cond9=1; else cond9=0; fi

if [ ${cond6} -eq 1 ] && [ ${cond9} -eq 1 ]; then cond10=1; else cond10=0; fi

run_cmd "/opt/batch/migration.sh"

# Attendu : retour 0

if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi

expected="retour 0"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond11=1; else cond11=0; fi

# ---- Step 5 - Vérifier la table en base ----

run_cmd "sqlplus -s ${SQL_CONN:-user/password@db} @verification.sql"

# Attendu : script exécuté avec succès

if [ $last_ret -eq 0 ]; then actual="Script exécuté avec succès"; else actual="Échec d'exécution du script"; fi

expected="Script exécuté avec succès"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond12=1; else cond12=0; fi

run_cmd "diff "./output.txt" "./output_attendu.txt""

# Attendu : fichiers identiques

if [ $last_ret -eq 0 ]; then actual="fichiers identiques"; else actual="fichiers différents"; fi

expected="fichiers identiques"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond13=1; else cond13=0; fi