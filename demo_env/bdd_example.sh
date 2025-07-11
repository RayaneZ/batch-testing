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



# ---- preparation ----

run_cmd "export sql_driver="mysql""

# Attendu : variable d'environnement définie

if [ $last_ret -eq 0 ]; then actual="variable d'environnement définie"; else actual="variable d'environnement non définie"; fi

expected="variable d'environnement définie"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond0=1; else cond0=0; fi

run_cmd "export sql_conn="rootme/ffddd584r@base_name""

# Attendu : identifiants configurés

if [ -n "$SQL_CONN" ]; then actual="identifiants configurés"; else actual="non configuré"; fi

expected="identifiants configurés"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi

run_cmd "sqlplus -s ${SQL_CONN:-user/password@db} @init_bdd.sql"

# Attendu : base prête

if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi

expected="base prête"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond2=1; else cond2=0; fi

# ---- execution ----

run_cmd "/opt/batch/migration.sh"

# Attendu : retour 0

if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi

expected="retour 0"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond3=1; else cond3=0; fi

# ---- verification ----

run_cmd "sqlplus -s ${SQL_CONN:-user/password@db} @verification.sql"

# Attendu : script exécuté avec succès

if [ $last_ret -eq 0 ]; then actual="Script exécuté avec succès"; else actual="Échec d'exécution du script"; fi

expected="Script exécuté avec succès"

log_diff "$expected" "$actual"

if [ "$expected" = "$actual" ]; then cond4=1; else cond4=0; fi