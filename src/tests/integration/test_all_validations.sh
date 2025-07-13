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

# Test step: stdout

# Test step: stderr

# Test step: fichier contient

# Test step: fichier existe

# Test step: fichier vide
# Execute: echo "Bonjour"
echo "Executing: echo "Bonjour""
stdout=$(echo "Bonjour" 2>&1)
last_ret=$?


# Execute: echo "Erreur grave" 1>&2
echo "Executing: echo "Erreur grave" 1>&2"
stdout=$(echo "Erreur grave" 1>&2 2>&1)
last_ret=$?


# Execute: echo "KO" > logs.txt
echo "Executing: echo "KO" > logs.txt"
stdout=$(echo "KO" > logs.txt 2>&1)
last_ret=$?


# Execute: touch fichier.txt
echo "Executing: touch fichier.txt"
stdout=$(touch fichier.txt 2>&1)
last_ret=$?


# Execute: > vide.txt
echo "Executing: > vide.txt"
stdout=$(> vide.txt 2>&1)
last_ret=$?


result_0=0
if echo "$stdout" | grep -q ''; then
    result_0=1
fi
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stdout contient Bonjour'
    exit 1
else
    echo '✅ Validation passed: stdout contient Bonjour'
fi


echo 'ERROR: Exception in plugin stderr_contains: StderrContainsValidation.to_shell() missing 1 required positional argument: 'var''
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: stderr contient Erreur'
    exit 1
else
    echo '✅ Validation passed: stderr contient Erreur'
fi


echo 'ERROR: No file specified for file_contains validation'
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: fichier logs.txt contient KO'
    exit 1
else
    echo '✅ Validation passed: fichier logs.txt contient KO'
fi


echo 'ERROR: No file specified for file_exists validation'
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: fichier fichier.txt existe'
    exit 1
else
    echo '✅ Validation passed: fichier fichier.txt existe'
fi


echo 'ERROR: No file specified for file_empty validation'
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: fichier vide.txt est vide'
    exit 1
else
    echo '✅ Validation passed: fichier vide.txt est vide'
fi



# Final result
if [ "$test_passed" = true ]; then
    echo "✅ Test passed"
    exit 0
else
    echo "❌ Test failed"
    exit 1
fi