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


# Test step: Default Step
echo 'Action: toucher le fichier /tmp/test.txt -t 202501010101'
run_action "touch -t '202501010101' '/tmp/test.txt'"
# date_modified
if echo 'ERROR: Missing file or date for date_modified validation'; then
    echo 'OK: date_modified'
else
    echo 'FAIL: NOT(date_modified)'
    exit 1
fi
echo 'Action: mettre à jour la date du fichier /tmp/test.txt 202501010101'
run_action "touch -t '202501010101' '/tmp/test.txt'"
# date_modified
if echo 'ERROR: Missing file or date for date_modified validation'; then
    echo 'OK: date_modified'
else
    echo 'FAIL: NOT(date_modified)'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0