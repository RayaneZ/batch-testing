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

# Test step: Main Step
# Execute: echo "This is an orphan action"
echo "Executing: echo "This is an orphan action""
stdout=$(echo "This is an orphan action" 2>&1)
last_ret=$?


# Execute: echo "Another orphan"
echo "Executing: echo "Another orphan""
stdout=$(echo "Another orphan" 2>&1)
last_ret=$?


# Execute: echo "This is a normal action"
echo "Executing: echo "This is a normal action""
stdout=$(echo "This is a normal action" 2>&1)
last_ret=$?


echo "$stdout" | grep -q "None"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient orphan'
    exit 1
else
    echo '✅ Validation passed: stdout contient orphan'
fi


echo "$stdout" | grep -q "None"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient another'
    exit 1
else
    echo '✅ Validation passed: stdout contient another'
fi


echo "$stdout" | grep -q "None"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient normal'
    exit 1
else
    echo '✅ Validation passed: stdout contient normal'
fi



# Final result
if [ "$test_passed" = true ]; then
    echo "Test passed"
    exit 0
else
    echo "Test failed"
    exit 1
fi