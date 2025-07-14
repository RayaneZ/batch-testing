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


# Test step: Default Step
echo 'Action: afficher le contenu du fichier = /tmp/test.txt'
run_action "cat '= /tmp/test.txt'"
# le contenu de None est affiché
if test -s 'None'; then
    echo 'OK: le contenu de None est affiché'
else
    echo 'FAIL: le contenu de None n'\''est pas affiché'
    exit 1
fi
echo 'Action: cat le fichier = /tmp/test.txt'
run_action "cat '/tmp/test.txt'"
# le contenu de None est affiché
if test -s 'None'; then
    echo 'OK: le contenu de None est affiché'
else
    echo 'FAIL: le contenu de None n'\''est pas affiché'
    exit 1
fi
echo 'Action: lire le fichier = /tmp/test.txt'
run_action "cat '/tmp/test.txt'"
# le contenu de None est affiché
if test -s 'None'; then
    echo 'OK: le contenu de None est affiché'
else
    echo 'FAIL: le contenu de None n'\''est pas affiché'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0