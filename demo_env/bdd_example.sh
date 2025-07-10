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

# ---- preparation ----
export SQL_DRIVER="mysql"
# Attendu : La variable d'environnement à été définie
actual="non vérifié"
expected="La variable d'environnement à été définie"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
verdict="KO"
if [ ${cond1} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
export SQL_CONN="rootme/ffDDD584R@base_name"
# Attendu : identifiants configurés
if [ -n "$SQL_CONN" ]; then actual="identifiants configurés"; else actual="non configuré"; fi
expected="identifiants configurés"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond2=1; else cond2=0; fi
verdict="KO"
if [ ${cond2} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "mysql ${SQL_CONN:-user/password@db} < init_bdd.sql"
# Attendu : base prête
if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi
expected="base prête"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond3=1; else cond3=0; fi
verdict="KO"
if [ ${cond3} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# ---- execution ----
run_cmd "/opt/batch/migration.sh"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond4=1; else cond4=0; fi
verdict="KO"
if [ ${cond4} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# ---- verification ----
run_cmd "mysql ${SQL_CONN:-user/password@db} < verification.sql"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond5=1; else cond5=0; fi
verdict="KO"
if [ ${cond5} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"