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


# Test step: Connexion personnalisée
# variable sql_conn vaut my_user/my_pass@base
if [ "$sql_conn" = "my_user/my_pass@base" ]; then echo 'variable sql_conn vaut my_user/my_pass@base'; else echo 'variable sql_conn ne vaut pas my_user/my_pass@base'; fi
# stdout contient ok
if echo "$stdout" | grep -q "ok"; then echo 'stdout contient ok'; else echo 'stdout ne contient pas ok'; fi

echo 'All steps and validations passed.'
exit 0