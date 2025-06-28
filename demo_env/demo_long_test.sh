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

# ---- Step 1 - Preparation ----
run_cmd "mkdir -p ./qualification/demo_env && chmod 0755 ./qualification/demo_env"
# Attendu : le dossier est cree
actual="non vérifié"
expected="le dossier est cree"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
run_cmd "touch ./qualification/demo_env/initial.txt && chmod 0644 ./qualification/demo_env/initial.txt"
# Attendu : le fichier est cree
actual="non vérifié"
expected="le fichier est cree"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
# ---- Step 2 - Ancien fichier ----
run_cmd "touch -t 202201010000 ./qualification/demo_env/old.txt"
# Attendu : date modifiee
actual="non vérifié"
expected="date modifiee"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
# ---- Step 3 - Nouveau fichier ----
run_cmd "touch ./qualification/demo_env/newfile.txt && chmod 0644 ./qualification/demo_env/newfile.txt"
# Attendu : fichier cree
if [ $last_ret -eq 0 ]; then actual="fichier cree"; else actual="échec création"; fi
expected="fichier cree"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
if [ ${cond1} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"
run_cmd "touch -t 202401010101 ./qualification/demo_env/newfile.txt"
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
# Attendu : retour 0
actual="non vérifié"
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
# Attendu : stdout contient Succès complet"
if echo $last_stdout | grep -q 'Succès complet'; then actual='Succès complet'; else actual=""; fi
expected='Succès complet'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond2=1; else cond2=0; fi
# Attendu : stderr contient WARNING
if echo $last_stderr | grep -q 'WARNING'; then actual='WARNING'; else actual=""; fi
expected='WARNING'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond3=1; else cond3=0; fi
if [ ${cond2} -eq 1 ] || [ ${cond3} -eq 1 ]; then cond4=1; else cond4=0; fi
if [ ${cond1} -eq 1 ] && [ ${cond4} -eq 1 ]; then cond5=1; else cond5=0; fi
if [ ${cond5} -eq 1 ]; then actual="OK"; else actual="KO"; fi
expected="OK"
log_diff "$expected" "$actual"