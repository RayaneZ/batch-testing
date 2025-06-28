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
export SQL_CONN=sqlplus -S rootme/ffDDD584R@base_name
# Attendu : identifiants configurés
actual="non vérifié"
expected="identifiants configurés"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
echo 'Exécuter le script SQL init_bdd.sql'
# Attendu : base prête
if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi
expected="base prête"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
# ---- execution ----
run_cmd "/opt/batch/migration.sh"
# Attendu : retour 0
actual="non vérifié"
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
# ---- verification ----
echo 'Exécuter le script SQL verification.sql'
# Attendu : base prête
if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi
expected="base prête"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"