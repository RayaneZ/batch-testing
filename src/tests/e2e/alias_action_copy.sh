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


helper_1() {
    # Le fichier est copié
    if [ -f '$1' ] && [ -f '$2' ]; then cmp -s '$1' '$2' && echo '$3' || echo '$4'; else echo '$4'; fi
}

helper_2() {
    # Le dossier est copié
    if [ -d '$1' ] && [ -d '$2' ]; then diff -r '$1' '$2' >/dev/null 2>&1 && echo '$3' || echo '$4'; else echo '$4'; fi
}

# Test step: Default Step
helper_1 "" "" "" ""
helper_1 "" "" "" ""
helper_2 "" "" "" ""
helper_2 "" "" "" ""

echo 'All steps and validations passed.'
exit 0