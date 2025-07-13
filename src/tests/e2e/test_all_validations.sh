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
# stdout contient bonjour
if echo "$stdout" | grep -q "bonjour"; then echo 'stdout contient bonjour'; else echo 'stdout ne contient pas bonjour'; fi

# Test step: stderr
# stderr contient erreur
if echo "$stderr" | grep -q "erreur"; then echo 'stderr contient erreur'; else echo 'stderr ne contient pas erreur'; fi

# Test step: fichier contient
# ^fichier ([^ ]+) contient (.+)$
if grep -q "{text}" "{file}"; then echo '{expected}'; else echo '{opposite}'; fi

# Test step: fichier existe
# ^fichier ([^ ]+) existe$
if [ -f 'fichier.txt' ]; then echo '^fichier ([^ ]+) existe$'; else echo 'le fichier fichier.txt n'\''existe pas'; fi

# Test step: fichier vide
# ^fichier ([^ ]+) est vide$
if [ ! -s 'vide.txt' ]; then echo '^fichier ([^ ]+) est vide$'; else echo 'le fichier vide.txt n'\''est pas vide'; fi

echo 'All steps and validations passed.'
exit 0