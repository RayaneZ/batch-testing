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


helper_1() {
    # le fichier None a été copié vers None
    [ -f None ] && [ -f None ] && cmp -s None None
}

# Test step: Default Step
echo 'Action: copier le fichier /tmp/a.txt vers /tmp/b.txt'
run_action "cp '/tmp/a.txt' '/tmp/b.txt'"
helper_1 
echo 'Action: déplacer le fichier /tmp/a.txt vers /tmp/b.txt'
run_action "mv '/tmp/a.txt' '/tmp/b.txt'"
helper_1 
echo 'Action: copier le dossier /tmp/dir vers /tmp/dir2'
run_action "cp -r '/tmp/dir' '/tmp/dir2'"
# le dossier None a été copié vers None
if test -d 'None' && test -d 'None' && diff -r 'None' 'None' >/dev/null 2>&1; then
    echo 'OK: le dossier None a été copié vers None'
else
    echo 'FAIL: le dossier None n'\''a pas été copié vers None'
    exit 1
fi
echo 'Action: déplacer le dossier /tmp/dir vers /tmp/dir2'
run_action "mv '/tmp/dir' '/tmp/dir2'"
# le dossier None a été copié vers None
if test -d 'None' && test -d 'None' && diff -r 'None' 'None' >/dev/null 2>&1; then
    echo 'OK: le dossier None a été copié vers None'
else
    echo 'FAIL: le dossier None n'\''a pas été copié vers None'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0