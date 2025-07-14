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


# Test step: Résultat combinatoire
echo 'Action: exécuter /opt/batch/traitement.sh'
run_action "sh '/opt/batch/traitement.sh'"
# Compound validation: et
# First validation:
# le code de retour est 0
if test $last_ret -eq 0; then
    echo 'OK: le code de retour est 0'
else
    echo 'FAIL: le code de retour n'\''est pas 0'
    exit 1
fi
cond4=$?
# Second validation:
# Compound validation: ou
# First validation:
# stdout contient ok
if echo "$stdout" | grep -q "ok"; then
    echo 'OK: stdout contient ok'
else
    echo 'FAIL: stdout ne contient pas ok'
    exit 1
fi
cond1=$?
# Second validation:
# stderr contient warning
if echo "$stderr" | grep -q "warning"; then
    echo 'OK: stderr contient warning'
else
    echo 'FAIL: stderr ne contient pas warning'
    exit 1
fi
cond2=$?
if [ $cond1 -eq 0 ] || [ $cond2 -eq 0 ]; then
    echo 'OK: Compound validation (ou)'
else
    echo 'FAIL: Compound validation (ou)'
    exit 1
fi
cond5=$?
if [ $cond4 -eq 0 ] && [ $cond5 -eq 0 ]; then
    echo 'OK: Compound validation (et)'
else
    echo 'FAIL: Compound validation (et)'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0