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

# Test step: Contenu du fichier
# Execute: echo "ERREUR" > logs.txt
echo "Executing: echo "ERREUR" > logs.txt"
stdout=$(echo "ERREUR" > logs.txt 2>&1)
last_ret=$?


echo 'ERROR: No file specified for file_contains validation'
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: fichier logs.txt contient ERREUR'
    exit 1
else
    echo '✅ Validation passed: fichier logs.txt contient ERREUR'
fi



# Final result
if [ "$test_passed" = true ]; then
    echo "✅ Test passed"
    exit 0
else
    echo "❌ Test failed"
    exit 1
fi