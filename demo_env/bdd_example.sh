# Attendu : La variable d'environnement à été définie
actual="non vérifié"
expected="La variable d'environnement à été définie"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond1=1; else cond1=0; fi
# Attendu : Les identifiants sont configurés
actual="non vérifié"
expected="Les identifiants sont configurés"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond2=1; else cond2=0; fi
# Attendu : La base est prête pour le test
actual="non vérifié"
expected="La base est prête pour le test"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond3=1; else cond3=0; fi
# Attendu : Le script retourne un code 0
actual="non vérifié"
expected="Le script retourne un code 0"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond4=1; else cond4=0; fi
# Attendu : Le script s'execute avec succès
actual="non vérifié"
expected="Le script s'execute avec succès"
log_diff "$expected" "$actual"
if [ "$expected" = "$actual" ]; then cond5=1; else cond5=0; fi
