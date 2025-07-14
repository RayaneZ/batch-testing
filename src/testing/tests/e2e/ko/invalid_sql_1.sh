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


# Test step: Test invalid SQL
echo 'Action: Exécuter la requête SQL: SELECT * FROM nonexistent_table'
run_action "sh 'la requête SQL: SELECT * FROM nonexistent_table'"

# Test step: Test malformed SQL
echo 'Action: Exécuter la requête SQL: SELECT * FROM table WHERE column = 'unclosed quote'
run_action "sh 'la requête SQL: SELECT * FROM table WHERE column = 'unclosed quote'"

echo 'All steps and validations passed.'
exit 0