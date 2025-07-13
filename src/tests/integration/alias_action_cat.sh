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

# Test step: Default Step
# Execute: afficher le contenu du fichier = /tmp/test.txt ; Résultat: contenu affiché.
echo "Executing: afficher le contenu du fichier = /tmp/test.txt ; Résultat: contenu affiché."
afficher le contenu du fichier = /tmp/test.txt ; Résultat: contenu affiché.
last_ret=$?


# Execute: cat le fichier = /tmp/test.txt ; Résultat: contenu affiché.
echo "Executing: cat le fichier = /tmp/test.txt ; Résultat: contenu affiché."
cat le fichier = /tmp/test.txt ; Résultat: contenu affiché.
last_ret=$?


# Execute: lire le fichier = /tmp/test.txt ; Résultat: contenu affiché.
echo "Executing: lire le fichier = /tmp/test.txt ; Résultat: contenu affiché."
lire le fichier = /tmp/test.txt ; Résultat: contenu affiché.
last_ret=$?



# Final result
if [ "$test_passed" = true ]; then
    echo "✅ Test passed"
    exit 0
else
    echo "❌ Test failed"
    exit 1
fi