#!/bin/bash

# Generated shell script from .shtest file

# Function to log differences
log_diff() {
    local expected="$1"
    local actual="$2"
    if [ "$expected" != "$actual" ]; then
        echo "Expected: $expected"
        echo "Actual: $actual"
    fi
}

# Initialize variables
last_ret=0
test_passed=true

# Test step: Configuration de la base de données

# Test step: Test d'export de requête simple

# Test step: Test de comparaison de requêtes identiques

# Test step: Test de comparaison avec tolérance numérique

# Test step: Test d'exécution de requête simple

# Test step: Test d'export avec format personnalisé

# Test step: Test de comparaison avec ordre ignoré

# Test step: Test de comparaison sans ordre - données identiques

# Test step: Test de comparaison sans ordre - données différentes
# Execute: définir la variable SQL_CONN = user/password@testdb
echo "Executing: définir la variable SQL_CONN = user/password@testdb"
stdout=$(définir la variable SQL_CONN = user/password@testdb 2>&1)
last_ret=$?


# Execute: exporter les résultats de la requête SELECT COUNT(*) FROM employees vers employees_count.xlsx
echo "Executing: exporter les résultats de la requête SELECT COUNT(*) FROM employees vers employees_count.xlsx"
stdout=$(exporter les résultats de la requête SELECT COUNT(*) FROM employees vers employees_count.xlsx 2>&1)
last_ret=$?


# Execute: comparer les résultats de la requête SELECT * FROM employees WHERE department = 'IT' avec SELECT * FROM employees WHERE department = 'IT'
echo "Executing: comparer les résultats de la requête SELECT * FROM employees WHERE department = 'IT' avec SELECT * FROM employees WHERE department = 'IT'"
stdout=$(comparer les résultats de la requête SELECT * FROM employees WHERE department = 'IT' avec SELECT * FROM employees WHERE department = 'IT' 2>&1)
last_ret=$?


# Execute: comparer les résultats de la requête SELECT AVG(salary) FROM employees avec SELECT AVG(salary) FROM employees
echo "Executing: comparer les résultats de la requête SELECT AVG(salary) FROM employees avec SELECT AVG(salary) FROM employees"
stdout=$(comparer les résultats de la requête SELECT AVG(salary) FROM employees avec SELECT AVG(salary) FROM employees 2>&1)
last_ret=$?


# Execute: exécuter la requête SELECT COUNT(*) FROM employees
echo "Executing: exécuter la requête SELECT COUNT(*) FROM employees"
stdout=$(exécuter la requête SELECT COUNT(*) FROM employees 2>&1)
last_ret=$?


# Execute: exporter les résultats de la requête SELECT name, salary FROM employees ORDER BY salary DESC vers top_salaries.xlsx
echo "Executing: exporter les résultats de la requête SELECT name, salary FROM employees ORDER BY salary DESC vers top_salaries.xlsx"
stdout=$(exporter les résultats de la requête SELECT name, salary FROM employees ORDER BY salary DESC vers top_salaries.xlsx 2>&1)
last_ret=$?


# Execute: comparer les résultats de la requête SELECT name, department FROM employees ORDER BY name avec SELECT name, department FROM employees ORDER BY department (ignorer l'ordre lors de la comparaison)
echo "Executing: comparer les résultats de la requête SELECT name, department FROM employees ORDER BY name avec SELECT name, department FROM employees ORDER BY department (ignorer l'ordre lors de la comparaison)"
stdout=$(comparer les résultats de la requête SELECT name, department FROM employees ORDER BY name avec SELECT name, department FROM employees ORDER BY department (ignorer l'ordre lors de la comparaison) 2>&1)
last_ret=$?


# Execute: comparer les résultats de la requête SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY salary avec SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY name (ignorer l'ordre lors de la comparaison)
echo "Executing: comparer les résultats de la requête SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY salary avec SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY name (ignorer l'ordre lors de la comparaison)"
stdout=$(comparer les résultats de la requête SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY salary avec SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY name (ignorer l'ordre lors de la comparaison) 2>&1)
last_ret=$?


# Execute: comparer les résultats de la requête SELECT name FROM employees WHERE department = 'IT' avec SELECT name FROM employees WHERE department = 'HR' (ignorer l'ordre lors de la comparaison)
echo "Executing: comparer les résultats de la requête SELECT name FROM employees WHERE department = 'IT' avec SELECT name FROM employees WHERE department = 'HR' (ignorer l'ordre lors de la comparaison)"
stdout=$(comparer les résultats de la requête SELECT name FROM employees WHERE department = 'IT' avec SELECT name FROM employees WHERE department = 'HR' (ignorer l'ordre lors de la comparaison) 2>&1)
last_ret=$?


echo 'ERROR: No matcher found for validation: variable SQL_CONN vaut user/password@testdb'
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: variable SQL_CONN vaut user/password@testdb'
    exit 1
else
    echo '✅ Validation passed: variable SQL_CONN vaut user/password@testdb'
fi


echo "$stdout" | grep -q "None"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient Excel file created successfully'
    exit 1
else
    echo '✅ Validation passed: stdout contient Excel file created successfully'
fi


echo "$stdout" | grep -q "None"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient COMPARISON_SUCCESS'
    exit 1
else
    echo '✅ Validation passed: stdout contient COMPARISON_SUCCESS'
fi


echo "$stdout" | grep -q "None"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient COMPARISON_SUCCESS'
    exit 1
else
    echo '✅ Validation passed: stdout contient COMPARISON_SUCCESS'
fi


echo "$stdout" | grep -q "None"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient un nombre'
    exit 1
else
    echo '✅ Validation passed: stdout contient un nombre'
fi


echo "$stdout" | grep -q "None"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient Excel file created successfully'
    exit 1
else
    echo '✅ Validation passed: stdout contient Excel file created successfully'
fi


echo "$stdout" | grep -q "None"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient COMPARISON_SUCCESS'
    exit 1
else
    echo '✅ Validation passed: stdout contient COMPARISON_SUCCESS'
fi


echo "$stdout" | grep -q "None"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient COMPARISON_SUCCESS'
    exit 1
else
    echo '✅ Validation passed: stdout contient COMPARISON_SUCCESS'
fi


echo "$stdout" | grep -q "None"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient COMPARISON_ERROR'
    exit 1
else
    echo '✅ Validation passed: stdout contient COMPARISON_ERROR'
fi



# Final result
if [ "$test_passed" = true ]; then
    echo "Test passed"
    exit 0
else
    echo "Test failed"
    exit 1
fi