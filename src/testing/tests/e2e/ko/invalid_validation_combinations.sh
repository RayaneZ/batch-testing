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
    echo 'Action: echo "test"'
    run_action "echo \"test\""
}

helper_1() {
    helper_1|
}

# Test step: Test conflicting validations
helper_1 

# Test step: Test invalid validation parameters
helper_1 

# Test step: Test missing validation parameters
helper_1 

echo 'All steps and validations passed.'
exit 0