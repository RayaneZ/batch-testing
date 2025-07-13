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


# Test step: Test invalid variable name
echo 'Action: Définir la variable: 123invalid_name = "value"'
run_action "Définir la variable: 123invalid_name = "value""

# Test step: Test invalid variable assignment
echo 'Action: Définir la variable: test_var = # Missing value'
run_action "Définir la variable: test_var = # Missing value"

# Test step: Test invalid variable reference
echo 'Action: echo "Testing variable: ${undefined_variable}"'
run_action "echo "Testing variable: ${undefined_variable}""

echo 'All steps and validations passed.'
exit 0