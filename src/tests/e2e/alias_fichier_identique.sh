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


# Test step: Default Step
# ^fichier_identique ([^ ]+) ([^ ]+)$
if [ -f '{file1}' ] && [ -f '{file2}' ]; then cmp -s '{file1}' '{file2}' && echo '{expected}' || echo '{opposite}'; else echo '{opposite}'; fi
# ^le fichier ([^ ]+) est identique à ([^ ]+)$
if [ -f '{file1}' ] && [ -f '{file2}' ]; then cmp -s '{file1}' '{file2}' && echo '{expected}' || echo '{opposite}'; else echo '{opposite}'; fi
# ^le fichier ([^ ]+) est identique a ([^ ]+)$
if [ -f '{file1}' ] && [ -f '{file2}' ]; then cmp -s '{file1}' '{file2}' && echo '{expected}' || echo '{opposite}'; else echo '{opposite}'; fi

echo 'All steps and validations passed.'
exit 0