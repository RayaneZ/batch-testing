#!/bin/sh

run_cmd() {
  local _stdout=$(mktemp)
  local _stderr=$(mktemp)
  sh -c "$1" >"$_stdout" 2>"$_stderr"
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

# ---- Step 1 - Preparation ----
# Validation des résultats
# Attendu : dossier créé
if [ $last_ret -eq 0 ]; then actual="dossier créé"; else actual="échec création"; fi
expected="dossier créé"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
# Validation des résultats
# Attendu : Le fichier est présent
actual="non vérifié"
expected="Le fichier est présent"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
# ---- Step 2 - Ancien fichier ----
run_cmd "touch -t 202201010000 ./qualification/demo_env/old.txt"
# Validation des résultats
# Attendu : date modifiee
actual="non vérifié"
expected="date modifiee"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
# ---- Step 3 - Nouveau fichier ----
# Validation des résultats
# Attendu : fichier cree
actual="non vérifié"
expected="fichier cree"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
# Validation des résultats
# Attendu : date modifiee
actual="non vérifié"
expected="date modifiee"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
# ---- Step 4 - Execution du batch ----
run_cmd "./qualification/purge.sh"
# Validation des résultats
# Attendu : retour 0
actual="$last_ret"
expected="0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"