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


# Test step: variable vaut
echo 'Action: export MON_VAR=42'
run_action "export MON_VAR=42"
# variable mon_var vaut 42
if test "$mon_var" = "42"; then
    echo 'OK: variable mon_var vaut 42'
else
    echo 'FAIL: variable mon_var ne vaut pas 42'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0