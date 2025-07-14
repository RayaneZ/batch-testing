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


# Test step: Sortie standard
echo 'Action: echo "OK"'
run_action "echo \"OK\""
# stdout contient ok
if echo "$stdout" | grep -q "ok"; then
    echo 'OK: stdout contient ok'
else
    echo 'FAIL: stdout ne contient pas ok'
    exit 1
fi

# Test step: Sortie erreur
echo 'Action: echo "KO" 1>&2'
run_action "echo \"KO\" 1>&2"
# stderr contient ko
if echo "$stderr" | grep -q "ko"; then
    echo 'OK: stderr contient ko'
else
    echo 'FAIL: stderr ne contient pas ko'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0