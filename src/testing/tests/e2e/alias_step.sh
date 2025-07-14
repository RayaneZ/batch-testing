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


# Test step: Exécution de script
echo 'Action: exécuter dummy.sh'
run_action "sh 'dummy.sh'"
# le code de retour est 0
if test $last_ret -eq 0; then
    echo 'OK: le code de retour est 0'
else
    echo 'FAIL: le code de retour n'\''est pas 0'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0