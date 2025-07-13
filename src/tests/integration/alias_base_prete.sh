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
# Execute: Exécuter script.sh ; Résultat: base prête.
echo "Executing: Exécuter script.sh ; Résultat: base prête."
stdout=$(Exécuter script.sh ; Résultat: base prête. 2>&1)
last_ret=$?


# Execute: Exécuter script.sh ; Résultat: La base de test est prête.
echo "Executing: Exécuter script.sh ; Résultat: La base de test est prête."
stdout=$(Exécuter script.sh ; Résultat: La base de test est prête. 2>&1)
last_ret=$?


# Execute: Exécuter script.sh ; Résultat: La base est prête pour le test.
echo "Executing: Exécuter script.sh ; Résultat: La base est prête pour le test."
stdout=$(Exécuter script.sh ; Résultat: La base est prête pour le test. 2>&1)
last_ret=$?



# Final result
if [ "$test_passed" = true ]; then
    echo "✅ Test passed"
    exit 0
else
    echo "❌ Test failed"
    exit 1
fi