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

# Test step: variable vaut
# Execute: export MON_VAR=42
echo "Executing: export MON_VAR=42"
stdout=$(export MON_VAR=42 2>&1)
last_ret=$?


echo 'ERROR: No matcher found for validation: variable MON_VAR vaut 42'
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: variable MON_VAR vaut 42'
    exit 1
else
    echo '✅ Validation passed: variable MON_VAR vaut 42'
fi



# Final result
if [ "$test_passed" = true ]; then
    echo "✅ Test passed"
    exit 0
else
    echo "❌ Test failed"
    exit 1
fi