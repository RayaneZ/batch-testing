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

# ---- Step 1 - Preparation ----
run_cmd "mkdir -p ./qualification/demo_env && chmod 0755 ./qualification/demo_env"
# Attendu : dossier créé
if [ $last_ret -eq 0 ]; then actual="dossier créé"; else actual="échec création"; fi
expected="dossier créé"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
verdict="KO"
if [ ${cond1} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch ./qualification/demo_env/initial.txt && chmod 0644 ./qualification/demo_env/initial.txt"
# Attendu : fichier cree
if [ $last_ret -eq 0 ]; then actual="fichier cree"; else actual="échec création"; fi
expected="fichier cree"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond2=1; else cond2=0; fi
verdict="KO"
if [ ${cond2} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
export SQL_CONN="rootme/ffDDD584R@base_name"
# ---- Step 2 - Ancien fichier ----
run_cmd "touch -t 202201010000 ./qualification/demo_env/old.txt"
# Attendu : date modifiee
if [ $last_ret -eq 0 ]; then actual="date modifiée"; else actual="date inchangée"; fi
expected="date modifiée"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond3=1; else cond3=0; fi
verdict="KO"
if [ ${cond3} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# ---- Step 3 - Nouveau fichier ----
run_cmd "touch ./qualification/demo_env/newfile.txt && chmod 0644 ./qualification/demo_env/newfile.txt"
# Attendu : fichier cree
if [ $last_ret -eq 0 ]; then actual="fichier cree"; else actual="échec création"; fi
expected="fichier cree"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond4=1; else cond4=0; fi
verdict="KO"
if [ ${cond4} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch -t 202401010101 ./qualification/demo_env/newfile.txt"
# Attendu : date modifiee
if [ $last_ret -eq 0 ]; then actual="date modifiée"; else actual="date inchangée"; fi
expected="date modifiée"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond5=1; else cond5=0; fi
verdict="KO"
if [ ${cond5} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# ---- Step 4 - Execution du batch ----
run_cmd "./qualification/purge.sh"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond6=1; else cond6=0; fi
# Attendu : stdout contient "Succès complet"
if echo "$last_stdout" | grep -q 'Succès complet'; then actual='Succès complet'; else actual=""; fi
expected='Succès complet'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond7=1; else cond7=0; fi
# Attendu : stderr contient WARNING
if echo "$last_stderr" | grep -q 'WARNING'; then actual='WARNING'; else actual=""; fi
expected='WARNING'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond8=1; else cond8=0; fi
if [ ${cond7} -eq 1 ] || [ ${cond8} -eq 1 ]; then cond9=1; else cond9=0; fi
if [ ${cond6} -eq 1 ] && [ ${cond9} -eq 1 ]; then cond10=1; else cond10=0; fi
verdict="KO"
if [ ${cond10} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "/opt/batch/migration.sh"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond11=1; else cond11=0; fi
verdict="KO"
if [ ${cond11} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# ---- Step 5 - Vérifier la table en base ----
run_cmd "sqlplus -S ${SQL_CONN:-user/password@db} <<'EOF'
WHENEVER SQLERROR EXIT 1;
@verification.sql
EOF"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond12=1; else cond12=0; fi
verdict="KO"
if [ ${cond12} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : fichier_identique ./output.txt ./output_attendu.txt
if diff -q ./output.txt ./output_attendu.txt >/dev/null; then actual="Les fichiers sont identiques"; else actual="Les fichiers sont différents"; fi
expected="Les fichiers sont identiques"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond13=1; else cond13=0; fi
verdict="KO"
if [ ${cond13} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"