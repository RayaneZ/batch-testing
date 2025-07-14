#!/bin/bash

# Generated shell script from .shtest file

run_action() {
    local cmd="$1"
    stdout=""
    stderr=""
    last_ret=0
    stdout=$(eval "$cmd" 2>stderr.log)
    last_ret=$?
    if [ -s stderr.log ]; then
        stderr=$(cat stderr.log)
    else
        stderr=""
    fi
    return $last_ret
}

validate_expect_actual() {
    local expected="$1"
    local actual="$2"
    if [ "$expected" != "$actual" ]; then
        echo "Expected: $expected"
        echo "Actual:   $actual"
        return 1
    fi
    return 0
}


# Test step: Exécution et vérification des logs
echo 'Action: exécuter /opt/batch/traitement.sh produit=123 quantité=10'
run_action "sh '/opt/batch/traitement.sh produit=123 quantité=10'"
# le code de retour est 0
if test $last_ret -eq 0; then
    echo 'OK: le code de retour est 0'
else
    echo 'FAIL: le code de retour n'\''est pas 0'
    exit 1
fi
echo 'Action: vérifier qu'il n'y a pas d'erreurs dans les logs'
run_action "vérifier qu'il n'y a pas d'erreurs dans les logs"
# aucun message d'erreur
if test ! -s 'stderr.log'; then
    echo 'OK: aucun message d'\''erreur'
else
    echo 'FAIL: un message d'\''erreur est présent'
    exit 1
fi
echo 'Action: indiquer le chemin des logs /var/log/system.log'
run_action "indiquer le chemin des logs /var/log/system.log"
# le fichier None est accessible
if test -f 'None'; then
    echo 'OK: le fichier None est accessible'
else
    echo 'FAIL: le fichier None n'\''est pas accessible'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0