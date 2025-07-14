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


# Test step: Connexion
echo 'Action: echo "Connexion réussie"'
run_action "echo \"Connexion réussie\""
# stdout contient "connexion"
if echo "$stdout" | grep -q ""connexion""; then
    echo 'OK: stdout contient "connexion"'
else
    echo 'FAIL: stdout ne contient pas "connexion"'
    exit 1
fi

# Test step: Vérification
echo 'Action: echo "OK"'
run_action "echo \"OK\""
# stdout contient "ok"
if echo "$stdout" | grep -q ""ok""; then
    echo 'OK: stdout contient "ok"'
else
    echo 'FAIL: stdout ne contient pas "ok"'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0