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


helper_1() {
    # stdout contient excel file created successfully
    if echo "$stdout" | grep -q "excel file created successfully"; then echo 'stdout contient excel file created successfully'; else echo 'stdout ne contient pas excel file created successfully'; fi
}

helper_2() {
    # stdout contient comparison_success
    if echo "$stdout" | grep -q "comparison_success"; then echo 'stdout contient comparison_success'; else echo 'stdout ne contient pas comparison_success'; fi
}

# Test step: Configuration de la base de données
# variable sql_conn vaut user/password@testdb
if [ "$sql_conn" = "user/password@testdb" ]; then echo 'variable sql_conn vaut user/password@testdb'; else echo 'variable sql_conn ne vaut pas user/password@testdb'; fi

# Test step: Test d'export de requête simple
helper_1 

# Test step: Test de comparaison de requêtes identiques
helper_2 

# Test step: Test de comparaison avec tolérance numérique
helper_2 

# Test step: Test d'exécution de requête simple
# stdout contient un nombre
if echo "$stdout" | grep -q "un nombre"; then echo 'stdout contient un nombre'; else echo 'stdout ne contient pas un nombre'; fi

# Test step: Test d'export avec format personnalisé
helper_1 

# Test step: Test de comparaison avec ordre ignoré
helper_2 

# Test step: Test de comparaison sans ordre - données identiques
helper_2 

# Test step: Test de comparaison sans ordre - données différentes
# stdout contient comparison_error
if echo "$stdout" | grep -q "comparison_error"; then echo 'stdout contient comparison_error'; else echo 'stdout ne contient pas comparison_error'; fi

echo 'All steps and validations passed.'
exit 0