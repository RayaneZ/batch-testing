#!/bin/sh

run_cmd() {
  local _stdout=$(mktemp)
  local _stderr=$(mktemp)
  /bin/sh -c "$1" >"$_stdout" 2>"_stderr"
  last_ret=$?
  last_stdout=$(cat "$_stdout")
  last_stderr=$(cat "$_stderr")
  rm -f "$_stdout" "$_stderr"
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
export SQL_CONN="rootme/ffDDD584R@base_name"
# Attendu : identifiants configurés
if [ -n "$SQL_CONN" ]; then actual="identifiants configurés"; else actual="non configuré"; fi
expected="identifiants configurés"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
run_cmd "sqlplus -S ${SQL_CONN:-user/password@db} @init_bdd.sql"
# Attendu : La base est prête pour le test
actual="non vérifié"
expected="La base est prête pour le test"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond2=1; else cond2=0; fi
if [ ${cond2} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
# ---- execution ----
run_cmd "/opt/batch/migration.sh"
# Attendu : retour 0
actual="non vérifié"
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond3=1; else cond3=0; fi
if [ ${cond3} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
# ---- verification ----
run_cmd "sqlplus -S ${SQL_CONN:-user/password@db} @verification.sql"
# Attendu : Le script s'execute avec succès
actual="non vérifié"
expected="Le script s'execute avec succès"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond4=1; else cond4=0; fi
if [ ${cond4} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"