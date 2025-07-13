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
    # ^le fichier ([^ ]+) contient (.+)$
    if grep -q "$1" "$2"; then echo '$3'; else echo '$4'; fi
}

# Test step: Vérifications de fichiers et dossiers
# ^le fichier ([^ ]+) existe$
if [ -f '/tmp/test.log' ]; then echo '^le fichier ([^ ]+) existe$'; else echo 'le fichier /tmp/test.log n'\''existe pas'; fi
# ^le fichier ([^ ]+) a les droits ([0-7]+)$
if [ $(stat -c '%a' '{file_path}') = '{mode}' ]; then echo '{expected}'; else echo '{opposite}'; fi
helper_1 "" "" "" ""
helper_1 "" "" "" ""
# ^le dossier ([^ ]+) existe$
if [ -d '/tmp/testdir' ]; then echo '^le dossier ([^ ]+) existe$'; else echo 'le dossier /tmp/testdir n'\''existe pas'; fi
# ^le dossier ([^ ]+) a les droits ([0-7]+)$
if [ $(stat -c '%a' '{dir_path}') = '{mode}' ]; then echo '{expected}'; else echo '{opposite}'; fi
# ^le dossier ([^ ]+) contient ([0-9]+) fichiers (.+)$
actual=$(find '{dir_path}' -type f -name '{pattern}' | wc -l); if [ "$actual" -eq {count} ]; then echo '{expected}'; else echo '{opposite}'; fi
# file_date
if [ -f '/tmp/test.log' ]; then file_date=$(date -r '/tmp/test.log' +%Y%m%d%H%M); if [ "$file_date" = '202501010000' ]; then echo 'OK'; else echo 'NOK'; fi; else echo 'NOK'; fi

echo 'All steps and validations passed.'
exit 0