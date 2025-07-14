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


# Test step: stdout
echo 'Action: echo "Bonjour"'
run_action "echo \"Bonjour\""
# stdout contient bonjour
if echo "$stdout" | grep -q "bonjour"; then
    echo 'OK: stdout contient bonjour'
else
    echo 'FAIL: stdout ne contient pas bonjour'
    exit 1
fi

# Test step: stderr
echo 'Action: echo "Erreur grave" 1>&2'
run_action "echo \"Erreur grave\" 1>&2"
# stderr contient erreur
if echo "$stderr" | grep -q "erreur"; then
    echo 'OK: stderr contient erreur'
else
    echo 'FAIL: stderr ne contient pas erreur'
    exit 1
fi

# Test step: fichier contient
echo 'Action: echo "KO" > logs.txt'
run_action "echo \"KO\" > logs.txt"
echo 'ERROR: Exception in handler file_contains: 'canonical_phrase''

# Test step: fichier existe
echo 'Action: touch fichier.txt'
run_action "touch fichier.txt"
# le fichier fichier.txt existe
if test -f 'fichier.txt'; then
    echo 'OK: le fichier fichier.txt existe'
else
    echo 'FAIL: le fichier fichier.txt n'\''existe pas'
    exit 1
fi

# Test step: fichier vide
echo 'Action: > vide.txt'
run_action "> vide.txt"
# le fichier vide.txt est vide
if test ! -s 'vide.txt'; then
    echo 'OK: le fichier vide.txt est vide'
else
    echo 'FAIL: le fichier vide.txt n'\''est pas vide'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0