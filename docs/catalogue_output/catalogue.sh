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

# ---- catalogue ----
run_cmd "cat /tmp/JDD_Commun.sql"
# Attendu : contenu affiché
if [ $last_ret -eq 0 ]; then actual="contenu affiché"; else actual="contenu non affiché"; fi
expected="contenu affiché"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
verdict="KO"
if [ ${cond1} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cat /tmp/JDD_Extra.sql"
# Attendu : le script est affiché
if [ $last_ret -eq 0 ]; then actual="contenu affiché"; else actual="contenu non affiché"; fi
expected="contenu affiché"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond2=1; else cond2=0; fi
verdict="KO"
if [ ${cond2} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cat /tmp/file.txt"
# Attendu : contenu correct
if [ $last_ret -eq 0 ]; then actual="contenu correct"; else actual="contenu incorrect"; fi
expected="contenu correct"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond3=1; else cond3=0; fi
verdict="KO"
if [ ${cond3} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cat /tmp/file.txt"
# Attendu : contenu correct
if [ $last_ret -eq 0 ]; then actual="contenu correct"; else actual="contenu incorrect"; fi
expected="contenu correct"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond4=1; else cond4=0; fi
verdict="KO"
if [ ${cond4} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cat /tmp/output.txt"
# Attendu : contenu correct
if [ $last_ret -eq 0 ]; then actual="contenu correct"; else actual="contenu incorrect"; fi
expected="contenu correct"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond5=1; else cond5=0; fi
verdict="KO"
if [ ${cond5} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cat /tmp/test.txt"
# Attendu : contenu affiché
if [ $last_ret -eq 0 ]; then actual="contenu affiché"; else actual="contenu non affiché"; fi
expected="contenu affiché"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond6=1; else cond6=0; fi
verdict="KO"
if [ ${cond6} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cat /tmp/test.txt"
# Attendu : le script est affiché
if [ $last_ret -eq 0 ]; then actual="contenu affiché"; else actual="contenu non affiché"; fi
expected="contenu affiché"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond7=1; else cond7=0; fi
verdict="KO"
if [ ${cond7} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cat /tmp/test.txt"
# Attendu : contenu affiché
if [ $last_ret -eq 0 ]; then actual="contenu affiché"; else actual="contenu non affiché"; fi
expected="contenu affiché"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond8=1; else cond8=0; fi
verdict="KO"
if [ ${cond8} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cat /tmp/test.txt"
# Attendu : contenu affiché
if [ $last_ret -eq 0 ]; then actual="contenu affiché"; else actual="contenu non affiché"; fi
expected="contenu affiché"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond9=1; else cond9=0; fi
verdict="KO"
if [ ${cond9} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cat /tmp/test_folder/test.txt"
# Attendu : contenu affiché
if [ $last_ret -eq 0 ]; then actual="contenu affiché"; else actual="contenu non affiché"; fi
expected="contenu affiché"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond10=1; else cond10=0; fi
verdict="KO"
if [ ${cond10} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "mv /tmp/data /tmp/backup"
# Attendu : le dossier est copié
if [ $last_ret -eq 0 ]; then actual="le dossier est copié"; else actual="le dossier non copié"; fi
expected="le dossier est copié"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond11=1; else cond11=0; fi
verdict="KO"
if [ ${cond11} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "mv /tmp/src.txt /tmp/dest.txt"
# Attendu : Le fichier est présent
if [ $last_ret -eq 0 ]; then actual="Le fichier est présent"; else actual="Le fichier est absent"; fi
expected="Le fichier est présent"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond12=1; else cond12=0; fi
verdict="KO"
if [ ${cond12} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "mkdir -p /tmp/data && chmod 0755 /tmp/data"
# Attendu : dossier créé
if [ $last_ret -eq 0 ]; then actual="dossier créé"; else actual="échec création"; fi
expected="dossier créé"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond13=1; else cond13=0; fi
verdict="KO"
if [ ${cond13} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "mkdir -p /tmp/newdir && chmod 0755 /tmp/newdir"
# Attendu : dossier créé
if [ $last_ret -eq 0 ]; then actual="dossier créé"; else actual="échec création"; fi
expected="dossier créé"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond14=1; else cond14=0; fi
verdict="KO"
if [ ${cond14} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "mkdir -p /tmp/newdir && chmod 0755 /tmp/newdir"
# Attendu : dossier créé
if [ $last_ret -eq 0 ]; then actual="dossier créé"; else actual="échec création"; fi
expected="dossier créé"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond15=1; else cond15=0; fi
verdict="KO"
if [ ${cond15} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "mkdir -p /tmp/newdir && chmod 0755 /tmp/newdir"
# Attendu : dossier créé
if [ $last_ret -eq 0 ]; then actual="dossier créé"; else actual="échec création"; fi
expected="dossier créé"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond16=1; else cond16=0; fi
verdict="KO"
if [ ${cond16} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch /tmp/test_folder"
# Attendu : dossier créé
if [ $last_ret -eq 0 ]; then actual="dossier créé"; else actual="échec création"; fi
expected="dossier créé"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond17=1; else cond17=0; fi
verdict="KO"
if [ ${cond17} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch /tmp/output.txt"
# Attendu : Le fichier est présent
if [ $last_ret -eq 0 ]; then actual="Le fichier est présent"; else actual="Le fichier est absent"; fi
expected="Le fichier est présent"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond18=1; else cond18=0; fi
verdict="KO"
if [ ${cond18} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch /tmp/test_folder/test.txt"
# Attendu : fichier cree
if [ $last_ret -eq 0 ]; then actual="fichier cree"; else actual="échec création"; fi
expected="fichier cree"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond19=1; else cond19=0; fi
verdict="KO"
if [ ${cond19} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
export SQL_CONN="sqlplus -S user/password@db"
# Attendu : identifiants configurés
if [ -n "$SQL_CONN" ]; then actual="identifiants configurés"; else actual="non configuré"; fi
expected="identifiants configurés"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond20=1; else cond20=0; fi
verdict="KO"
if [ ${cond20} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
export SQL_CONN="sqlplus -S user/password@db"
# Attendu : identifiants configurés
if [ -n "$SQL_CONN" ]; then actual="identifiants configurés"; else actual="non configuré"; fi
expected="identifiants configurés"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond21=1; else cond21=0; fi
verdict="KO"
if [ ${cond21} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "/opt/batch/traitement.sh"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond22=1; else cond22=0; fi
# Attendu : stdout contient "OK"
if echo "$last_stdout" | grep -q 'OK'; then actual='OK'; else actual=""; fi
expected='OK'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond23=1; else cond23=0; fi
# Attendu : stderr contient WARNING
if echo "$last_stderr" | grep -q 'WARNING'; then actual='WARNING'; else actual=""; fi
expected='WARNING'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond24=1; else cond24=0; fi
if [ ${cond23} -eq 1 ] || [ ${cond24} -eq 1 ]; then cond25=1; else cond25=0; fi
if [ ${cond22} -eq 1 ] && [ ${cond25} -eq 1 ]; then cond26=1; else cond26=0; fi
verdict="KO"
if [ ${cond26} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "/opt/batch/traitement.sh"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond27=1; else cond27=0; fi
# Attendu : stdout contient "Succès complet"
if echo "$last_stdout" | grep -q 'Succès complet'; then actual='Succès complet'; else actual=""; fi
expected='Succès complet'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond28=1; else cond28=0; fi
# Attendu : stderr contient WARNING
if echo "$last_stderr" | grep -q 'WARNING'; then actual='WARNING'; else actual=""; fi
expected='WARNING'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond29=1; else cond29=0; fi
if [ ${cond28} -eq 1 ] || [ ${cond29} -eq 1 ]; then cond30=1; else cond30=0; fi
if [ ${cond27} -eq 1 ] && [ ${cond30} -eq 1 ]; then cond31=1; else cond31=0; fi
verdict="KO"
if [ ${cond31} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "/opt/batch/traitement.sh"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond32=1; else cond32=0; fi
# Attendu : stdout contient "OK"
if echo "$last_stdout" | grep -q 'OK'; then actual='OK'; else actual=""; fi
expected='OK'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond33=1; else cond33=0; fi
# Attendu : stderr contient WARNING
if echo "$last_stderr" | grep -q 'WARNING'; then actual='WARNING'; else actual=""; fi
expected='WARNING'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond34=1; else cond34=0; fi
if [ ${cond33} -eq 1 ] || [ ${cond34} -eq 1 ]; then cond35=1; else cond35=0; fi
if [ ${cond32} -eq 1 ] && [ ${cond35} -eq 1 ]; then cond36=1; else cond36=0; fi
verdict="KO"
if [ ${cond36} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
export produit="123"
export quantité="10"
run_cmd "/opt/batch/traitement.sh produit=123 quantité=10"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond37=1; else cond37=0; fi
verdict="KO"
if [ ${cond37} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
export produit="567"
export quantité="20"
run_cmd "/opt/batch/traitement.sh produit=567 quantité=20"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond38=1; else cond38=0; fi
# Attendu : stdout contient "Traitement OK"
if echo "$last_stdout" | grep -q 'Traitement OK'; then actual='Traitement OK'; else actual=""; fi
expected='Traitement OK'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond39=1; else cond39=0; fi
# Attendu : stderr contient WARNING
if echo "$last_stderr" | grep -q 'WARNING'; then actual='WARNING'; else actual=""; fi
expected='WARNING'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond40=1; else cond40=0; fi
if [ ${cond39} -eq 1 ] || [ ${cond40} -eq 1 ]; then cond41=1; else cond41=0; fi
if [ ${cond38} -eq 1 ] && [ ${cond41} -eq 1 ]; then cond42=1; else cond42=0; fi
verdict="KO"
if [ ${cond42} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "sqlplus -S ${SQL_CONN:-user/password@db} <<'EOF'
WHENEVER SQLERROR EXIT 1;
@JDD_Commun.sql
EOF"
# Attendu : base prête
if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi
expected="base prête"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond43=1; else cond43=0; fi
verdict="KO"
if [ ${cond43} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "sqlplus -S ${SQL_CONN:-user/password@db} <<'EOF'
WHENEVER SQLERROR EXIT 1;
@JDD_Commun.sql
EOF"
run_cmd "sqlplus -S ${SQL_CONN:-user/password@db} <<'EOF'
WHENEVER SQLERROR EXIT 1;
@JDD_Extra.sql
EOF"
# Attendu : base prête
if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi
expected="base prête"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond44=1; else cond44=0; fi
verdict="KO"
if [ ${cond44} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "script.sh"
# Attendu : base prête
if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi
expected="base prête"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond45=1; else cond45=0; fi
verdict="KO"
if [ ${cond45} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "script.sh"
# Attendu : base prête
if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi
expected="base prête"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond46=1; else cond46=0; fi
verdict="KO"
if [ ${cond46} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "script.sh"
# Attendu : fichier_identique /tmp/a.txt /tmp/b.txt
if diff -q /tmp/a.txt /tmp/b.txt >/dev/null; then actual="Les fichiers sont identiques"; else actual="Les fichiers sont différents"; fi
expected="Les fichiers sont identiques"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond47=1; else cond47=0; fi
verdict="KO"
if [ ${cond47} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "script.sh"
# Attendu : fichier_identique /tmp/a.txt /tmp/b.txt
if diff -q /tmp/a.txt /tmp/b.txt >/dev/null; then actual="Les fichiers sont identiques"; else actual="Les fichiers sont différents"; fi
expected="Les fichiers sont identiques"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond48=1; else cond48=0; fi
verdict="KO"
if [ ${cond48} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "script.sh"
# Attendu : base prête
if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi
expected="base prête"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond49=1; else cond49=0; fi
verdict="KO"
if [ ${cond49} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "script.sh"
# Attendu : fichier_identique /tmp/a.txt /tmp/b.txt
if diff -q /tmp/a.txt /tmp/b.txt >/dev/null; then actual="Les fichiers sont identiques"; else actual="Les fichiers sont différents"; fi
expected="Les fichiers sont identiques"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond50=1; else cond50=0; fi
verdict="KO"
if [ ${cond50} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : logs accessibles
if [ $last_ret -eq 0 ]; then actual="logs accessibles"; else actual="logs inaccessibles"; fi
expected="logs accessibles"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond51=1; else cond51=0; fi
verdict="KO"
if [ ${cond51} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : logs accessibles
if [ $last_ret -eq 0 ]; then actual="logs accessibles"; else actual="logs inaccessibles"; fi
expected="logs accessibles"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond52=1; else cond52=0; fi
verdict="KO"
if [ ${cond52} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : logs accessibles
if [ $last_ret -eq 0 ]; then actual="logs accessibles"; else actual="logs inaccessibles"; fi
expected="logs accessibles"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond53=1; else cond53=0; fi
verdict="KO"
if [ ${cond53} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch -t 202501010101 /tmp/file.txt"
# Attendu : date modifiée
if [ $last_ret -eq 0 ]; then actual="date modifiée"; else actual="date inchangée"; fi
expected="date modifiée"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond54=1; else cond54=0; fi
verdict="KO"
if [ ${cond54} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch -t 202501010101 /tmp/file.txt"
# Attendu : date modifiée
if [ $last_ret -eq 0 ]; then actual="date modifiée"; else actual="date inchangée"; fi
expected="date modifiée"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond55=1; else cond55=0; fi
verdict="KO"
if [ ${cond55} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch -t 202501021200 /tmp/output.txt"
# Attendu : date modifiée
if [ $last_ret -eq 0 ]; then actual="date modifiée"; else actual="date inchangée"; fi
expected="date modifiée"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond56=1; else cond56=0; fi
verdict="KO"
if [ ${cond56} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch -t 202501010000 /tmp/init.flag"
# Attendu : Le fichier est présent
if [ $last_ret -eq 0 ]; then actual="Le fichier est présent"; else actual="Le fichier est absent"; fi
expected="Le fichier est présent"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond57=1; else cond57=0; fi
verdict="KO"
if [ ${cond57} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "rm -rf /tmp/cache/* && mkdir -p /tmp/cache"
# Attendu : dossier créé
if [ $last_ret -eq 0 ]; then actual="dossier créé"; else actual="échec création"; fi
expected="dossier créé"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond58=1; else cond58=0; fi
verdict="KO"
if [ ${cond58} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : stdout contient 030
if echo "$last_stdout" | grep -q '030'; then actual='030'; else actual=""; fi
expected='030'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond59=1; else cond59=0; fi
verdict="KO"
if [ ${cond59} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : stderr=
actual="$last_stderr"
expected=""
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond60=1; else cond60=0; fi
verdict="KO"
if [ ${cond60} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : stderr=
actual="$last_stderr"
expected=""
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond61=1; else cond61=0; fi
verdict="KO"
if [ ${cond61} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : stderr=
actual="$last_stderr"
expected=""
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond62=1; else cond62=0; fi
verdict="KO"
if [ ${cond62} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : la date du fichier /tmp/test.log est 202501010000
actual=$(date -r /tmp/test.log +%Y%m%d%H%M%S)
expected=202501010000
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond63=1; else cond63=0; fi
verdict="KO"
if [ ${cond63} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : la date du fichier /tmp/test.log est 202501010000
actual=$(date -r /tmp/test.log +%Y%m%d%H%M%S)
expected=202501010000
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond64=1; else cond64=0; fi
verdict="KO"
if [ ${cond64} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le dossier /tmp/testdir a les droits 0755
if [ -d /tmp/testdir ] && [ \$(stat -c '%a' /tmp/testdir) = 0755 ]; then actual="dossier /tmp/testdir a les droits 0755"; else actual="dossier /tmp/testdir droits incorrects"; fi
expected="dossier /tmp/testdir a les droits 0755"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond65=1; else cond65=0; fi
verdict="KO"
if [ ${cond65} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le dossier /tmp/testdir a les droits 0755
if [ -d /tmp/testdir ] && [ \$(stat -c '%a' /tmp/testdir) = 0755 ]; then actual="dossier /tmp/testdir a les droits 0755"; else actual="dossier /tmp/testdir droits incorrects"; fi
expected="dossier /tmp/testdir a les droits 0755"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond66=1; else cond66=0; fi
verdict="KO"
if [ ${cond66} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le dossier /tmp/testdir contient 2 fichiers *.txt
actual=$(find /tmp/testdir -maxdepth 1 -name '*.txt' | wc -l)
expected=2
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond67=1; else cond67=0; fi
verdict="KO"
if [ ${cond67} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le dossier /tmp/testdir contient 2 fichiers *.txt
actual=$(find /tmp/testdir -maxdepth 1 -name '*.txt' | wc -l)
expected=2
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond68=1; else cond68=0; fi
verdict="KO"
if [ ${cond68} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le dossier /tmp/testdir existe
if [ -d /tmp/testdir ]; then actual="le dossier /tmp/testdir existe"; else actual="le dossier /tmp/testdir absent"; fi
expected="le dossier /tmp/testdir existe"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond69=1; else cond69=0; fi
verdict="KO"
if [ ${cond69} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le dossier /tmp/testdir existe
if [ -d /tmp/testdir ]; then actual="le dossier /tmp/testdir existe"; else actual="le dossier /tmp/testdir absent"; fi
expected="le dossier /tmp/testdir existe"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond70=1; else cond70=0; fi
verdict="KO"
if [ ${cond70} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le fichier /tmp/dest.txt existe
if [ -e /tmp/dest.txt ]; then actual="le fichier /tmp/dest.txt existe"; else actual="le fichier /tmp/dest.txt absent"; fi
expected="le fichier /tmp/dest.txt existe"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond71=1; else cond71=0; fi
verdict="KO"
if [ ${cond71} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le fichier /tmp/dest.txt existe
if [ -e /tmp/dest.txt ]; then actual="le fichier /tmp/dest.txt existe"; else actual="le fichier /tmp/dest.txt absent"; fi
expected="le fichier /tmp/dest.txt existe"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond72=1; else cond72=0; fi
verdict="KO"
if [ ${cond72} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le fichier /tmp/dest.txt existe
if [ -e /tmp/dest.txt ]; then actual="le fichier /tmp/dest.txt existe"; else actual="le fichier /tmp/dest.txt absent"; fi
expected="le fichier /tmp/dest.txt existe"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond73=1; else cond73=0; fi
verdict="KO"
if [ ${cond73} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : Le fichier est présent
if [ $last_ret -eq 0 ]; then actual="Le fichier est présent"; else actual="Le fichier est absent"; fi
expected="Le fichier est présent"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond74=1; else cond74=0; fi
# Attendu : le fichier /tmp/dest.txt existe 
if [ -e /tmp/dest.txt ]; then actual="le fichier /tmp/dest.txt existe"; else actual="le fichier /tmp/dest.txt absent"; fi
expected="le fichier /tmp/dest.txt existe"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond75=1; else cond75=0; fi
# Attendu : stderr contient "Erreur de copie"
if echo "$last_stderr" | grep -q 'Erreur de copie'; then actual='Erreur de copie'; else actual=""; fi
expected='Erreur de copie'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond76=1; else cond76=0; fi
if [ ${cond75} -eq 1 ] || [ ${cond76} -eq 1 ]; then cond77=1; else cond77=0; fi
if [ ${cond74} -eq 1 ] && [ ${cond77} -eq 1 ]; then cond78=1; else cond78=0; fi
verdict="KO"
if [ ${cond78} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le fichier /tmp/test.log a les droits 0644
if [ -f /tmp/test.log ] && [ \$(stat -c '%a' /tmp/test.log) = 0644 ]; then actual="fichier /tmp/test.log a les droits 0644"; else actual="fichier /tmp/test.log droits incorrects"; fi
expected="fichier /tmp/test.log a les droits 0644"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond79=1; else cond79=0; fi
verdict="KO"
if [ ${cond79} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le fichier /tmp/test.log a les droits 0644
if [ -f /tmp/test.log ] && [ \$(stat -c '%a' /tmp/test.log) = 0644 ]; then actual="fichier /tmp/test.log a les droits 0644"; else actual="fichier /tmp/test.log droits incorrects"; fi
expected="fichier /tmp/test.log a les droits 0644"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond80=1; else cond80=0; fi
verdict="KO"
if [ ${cond80} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le fichier /tmp/test.log contient OK
if grep -q 'OK' /tmp/test.log; then actual='OK'; else actual=""; fi
expected='OK'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond81=1; else cond81=0; fi
verdict="KO"
if [ ${cond81} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le fichier /tmp/test.log contient OK
if grep -q 'OK' /tmp/test.log; then actual='OK'; else actual=""; fi
expected='OK'
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond82=1; else cond82=0; fi
verdict="KO"
if [ ${cond82} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le fichier /tmp/test.log contient exactement ALLGOOD
actual=$(cat /tmp/test.log)
expected="ALLGOOD"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond83=1; else cond83=0; fi
verdict="KO"
if [ ${cond83} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le fichier /tmp/test.log contient exactement ALLGOOD
actual=$(cat /tmp/test.log)
expected="ALLGOOD"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond84=1; else cond84=0; fi
verdict="KO"
if [ ${cond84} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le fichier /tmp/test.log existe
if [ -e /tmp/test.log ]; then actual="le fichier /tmp/test.log existe"; else actual="le fichier /tmp/test.log absent"; fi
expected="le fichier /tmp/test.log existe"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond85=1; else cond85=0; fi
verdict="KO"
if [ ${cond85} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Attendu : le fichier /tmp/test.log existe
if [ -e /tmp/test.log ]; then actual="le fichier /tmp/test.log existe"; else actual="le fichier /tmp/test.log absent"; fi
expected="le fichier /tmp/test.log existe"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond86=1; else cond86=0; fi
verdict="KO"
if [ ${cond86} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cat /tmp/test.txt"
# Attendu : contenu affiché
if [ $last_ret -eq 0 ]; then actual="contenu affiché"; else actual="contenu non affiché"; fi
expected="contenu affiché"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond87=1; else cond87=0; fi
verdict="KO"
if [ ${cond87} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cat /tmp/test.txt"
# Attendu : contenu affiché
if [ $last_ret -eq 0 ]; then actual="contenu affiché"; else actual="contenu non affiché"; fi
expected="contenu affiché"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond88=1; else cond88=0; fi
verdict="KO"
if [ ${cond88} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Initialisation
run_cmd "echo 'configurer le contexte'"
# Attendu : base prête
if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi
expected="base prête"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond89=1; else cond89=0; fi
verdict="KO"
if [ ${cond89} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cp -r /tmp/dir /tmp/dir2"
# Attendu : le dossier est copié
if [ $last_ret -eq 0 ]; then actual="le dossier est copié"; else actual="le dossier non copié"; fi
expected="le dossier est copié"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond90=1; else cond90=0; fi
verdict="KO"
if [ ${cond90} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cp /tmp/a.txt /tmp/b.txt"
# Attendu : Le fichier est présent
if [ $last_ret -eq 0 ]; then actual="Le fichier est présent"; else actual="Le fichier est absent"; fi
expected="Le fichier est présent"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond91=1; else cond91=0; fi
verdict="KO"
if [ ${cond91} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Initialisation
run_cmd "echo 'créer le contexte'"
# Attendu : base prête
if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi
expected="base prête"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond92=1; else cond92=0; fi
verdict="KO"
if [ ${cond92} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch /tmp/test.txt && chmod 0600 /tmp/test.txt"
# Attendu : Le fichier est présent
if [ $last_ret -eq 0 ]; then actual="Le fichier est présent"; else actual="Le fichier est absent"; fi
expected="Le fichier est présent"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond93=1; else cond93=0; fi
verdict="KO"
if [ ${cond93} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "mv /tmp/dir /tmp/dir2"
# Attendu : le dossier est déplacé
if [ $last_ret -eq 0 ]; then actual="le dossier est déplacé"; else actual="dossier non déplacé"; fi
expected="le dossier est déplacé"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond94=1; else cond94=0; fi
verdict="KO"
if [ ${cond94} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "mv /tmp/a.txt /tmp/b.txt"
# Attendu : le fichier est déplacé
if [ $last_ret -eq 0 ]; then actual="le fichier est déplacé"; else actual="fichier non déplacé"; fi
expected="le fichier est déplacé"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond95=1; else cond95=0; fi
verdict="KO"
if [ ${cond95} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "dummy.sh"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond96=1; else cond96=0; fi
verdict="KO"
if [ ${cond96} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "traitement.sh"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond97=1; else cond97=0; fi
verdict="KO"
if [ ${cond97} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
# Initialisation
run_cmd "echo 'initialiser le contexte'"
# Attendu : base prête
if [ $last_ret -eq 0 ]; then actual="base prête"; else actual="base non prête"; fi
expected="base prête"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond98=1; else cond98=0; fi
verdict="KO"
if [ ${cond98} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "traitement.sh"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond99=1; else cond99=0; fi
verdict="KO"
if [ ${cond99} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "cat /tmp/test.txt"
# Attendu : contenu affiché
if [ $last_ret -eq 0 ]; then actual="contenu affiché"; else actual="contenu non affiché"; fi
expected="contenu affiché"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond100=1; else cond100=0; fi
verdict="KO"
if [ ${cond100} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch -t 202501010101 /tmp/test.txt"
# Attendu : date modifiée
if [ $last_ret -eq 0 ]; then actual="date modifiée"; else actual="date inchangée"; fi
expected="date modifiée"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond101=1; else cond101=0; fi
verdict="KO"
if [ ${cond101} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch /tmp/test.txt"
# Attendu : Le fichier est présent
if [ $last_ret -eq 0 ]; then actual="Le fichier est présent"; else actual="Le fichier est absent"; fi
expected="Le fichier est présent"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond102=1; else cond102=0; fi
verdict="KO"
if [ ${cond102} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "touch -t 202501010101 /tmp/test.txt"
# Attendu : date modifiée
if [ $last_ret -eq 0 ]; then actual="date modifiée"; else actual="date inchangée"; fi
expected="date modifiée"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond103=1; else cond103=0; fi
verdict="KO"
if [ ${cond103} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
run_cmd "traitement.sh"
# Attendu : retour 0
if [ $last_ret -eq 0 ]; then actual="retour 0"; else actual="retour $last_ret"; fi
expected="retour 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond104=1; else cond104=0; fi
verdict="KO"
if [ ${cond104} -eq 1 ]; then verdict="OK"; fi
expected="OK"
log_diff "$expected" "$verdict"
