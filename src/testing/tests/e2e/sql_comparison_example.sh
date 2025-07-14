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


helper_1() {
    # stdout contient excel file created successfully
    echo "$stdout" | grep -q "excel file created successfully"
}

helper_2() {
    # stdout contient comparison_success
    echo "$stdout" | grep -q "comparison_success"
}

# Test step: Configuration de la base de données
echo 'Action: définir la variable SQL_CONN = user/password@testdb'
run_action "export SQL_CONN='user/password@testdb'"
# variable sql_conn vaut user/password@testdb
if test "$sql_conn" = "user/password@testdb"; then
    echo 'OK: variable sql_conn vaut user/password@testdb'
else
    echo 'FAIL: variable sql_conn ne vaut pas user/password@testdb'
    exit 1
fi

# Test step: Test d'export de requête simple
echo 'Action: exporter les résultats de la requête SELECT COUNT(*) FROM employees vers employees_count.xlsx'
run_action "exporter les résultats de la requête SELECT COUNT(*) FROM employees vers employees_count.xlsx"
helper_1 

# Test step: Test de comparaison de requêtes identiques
echo 'Action: comparer les résultats de la requête SELECT * FROM employees WHERE department = 'IT' avec SELECT * FROM employees WHERE department = 'IT''
run_action "comparer les résultats de la requête SELECT * FROM employees WHERE department = 'IT' avec SELECT * FROM employees WHERE department = 'IT'"
helper_2 

# Test step: Test de comparaison avec tolérance numérique
echo 'Action: comparer les résultats de la requête SELECT AVG(salary) FROM employees avec SELECT AVG(salary) FROM employees'
run_action "comparer les résultats de la requête SELECT AVG(salary) FROM employees avec SELECT AVG(salary) FROM employees"
helper_2 

# Test step: Test d'exécution de requête simple
echo 'Action: exécuter la requête SELECT COUNT(*) FROM employees'
run_action "sh 'la requête SELECT COUNT(*) FROM employees'"
# stdout contient un nombre
if echo "$stdout" | grep -q "un nombre"; then
    echo 'OK: stdout contient un nombre'
else
    echo 'FAIL: stdout ne contient pas un nombre'
    exit 1
fi

# Test step: Test d'export avec format personnalisé
echo 'Action: exporter les résultats de la requête SELECT name, salary FROM employees ORDER BY salary DESC vers top_salaries.xlsx'
run_action "exporter les résultats de la requête SELECT name, salary FROM employees ORDER BY salary DESC vers top_salaries.xlsx"
helper_1 

# Test step: Test de comparaison avec ordre ignoré
echo 'Action: comparer les résultats de la requête SELECT name, department FROM employees ORDER BY name avec SELECT name, department FROM employees ORDER BY department (ignorer l'ordre lors de la comparaison)'
run_action "comparer les résultats de la requête SELECT name, department FROM employees ORDER BY name avec SELECT name, department FROM employees ORDER BY department (ignorer l'ordre lors de la comparaison)"
helper_2 

# Test step: Test de comparaison sans ordre - données identiques
echo 'Action: comparer les résultats de la requête SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY salary avec SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY name (ignorer l'ordre lors de la comparaison)'
run_action "comparer les résultats de la requête SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY salary avec SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY name (ignorer l'ordre lors de la comparaison)"
helper_2 

# Test step: Test de comparaison sans ordre - données différentes
echo 'Action: comparer les résultats de la requête SELECT name FROM employees WHERE department = 'IT' avec SELECT name FROM employees WHERE department = 'HR' (ignorer l'ordre lors de la comparaison)'
run_action "comparer les résultats de la requête SELECT name FROM employees WHERE department = 'IT' avec SELECT name FROM employees WHERE department = 'HR' (ignorer l'ordre lors de la comparaison)"
# stdout contient comparison_error
if echo "$stdout" | grep -q "comparison_error"; then
    echo 'OK: stdout contient comparison_error'
else
    echo 'FAIL: stdout ne contient pas comparison_error'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0