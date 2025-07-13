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
# ^retour ([0-9]+)$
if [ ${?} -eq {code} ]; then echo '{expected}'; else echo '{opposite}'; fi
# Aucun message d'erreur
if [ ! -s 'stderr.log' ]; then echo '{expected}'; else echo '{opposite}'; fi
# les logs sont accessibles
if [ -f '{file_path}' ]; then echo '{expected}'; else echo '{opposite}'; fi

echo 'All steps and validations passed.'
exit 0