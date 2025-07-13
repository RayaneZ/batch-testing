#!/bin/bash

# Generated shell script from .shtest file

# Function to log differences
log_diff() {
    local expected="$1"
    local actual="$2"
    if [ "$expected" != "$actual" ]; then
        echo "Expected: $expected"
        echo "Actual: $actual"
    fi
}

# Initialize variables
last_ret=0
test_passed=true

# Test step: Sortie standard

# Test step: Sortie erreur
# Execute: echo "OK"
echo "Executing: echo "OK""
stdout=$(echo "OK" 2>&1)
last_ret=$?


# Execute: echo "KO" 1>&2
echo "Executing: echo "KO" 1>&2"
stdout=$(echo "KO" 1>&2 2>&1)
last_ret=$?


result_0=0
if echo "$stdout" | grep -q ''; then
    result_0=1
fi
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient OK'
    exit 1
else
    echo '✅ Validation passed: stdout contient OK'
fi


echo 'ERROR: Exception in plugin stderr_contains: StderrContainsValidation.to_shell() missing 1 required positional argument: 'var''
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stderr contient KO'
    exit 1
else
    echo '✅ Validation passed: stderr contient KO'
fi



# Final result
if [ "$test_passed" = true ]; then
    echo "✅ Test passed"
    exit 0
else
    echo "❌ Test failed"
    exit 1
fi