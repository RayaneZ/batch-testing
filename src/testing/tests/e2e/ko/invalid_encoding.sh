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


# Test step: Test invalid chars
echo 'Action: echo "test with invalid chars: \x00\x01\x02"'
run_action "echo \"test with invalid chars: \\x00\\x01\\x02\""

# Test step: Test unicode issues
echo 'Action: echo "test with unicode: 🚀🌟✨"'
run_action "echo \"test with unicode: 🚀🌟✨\""

echo 'All steps and validations passed.'
exit 0