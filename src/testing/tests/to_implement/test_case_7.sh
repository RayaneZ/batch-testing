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


# Test step: Vérifications de fichiers et dossiers
echo 'Action: Vérifier que le fichier /tmp/test.log existe'
run_action "Vérifier que le fichier /tmp/test.log existe"
echo 'ERROR: Could not import handler file_exists: No module named 'shtest_compiler.utils''
echo 'Action: Vérifier que le fichier /tmp/test.log a les droits 0644'
run_action "Vérifier que le fichier /tmp/test.log a les droits 0644"
# le fichier /tmp/test.log a les droits 0644
if [ $(stat -c '%a' /tmp/test.log) = '0644' ]; then
    echo 'OK: le fichier /tmp/test.log a les droits 0644'
else
    echo 'FAIL: le fichier /tmp/test.log n'\''a pas les droits 0644'
    exit 1
fi
echo 'Action: Vérifier que le fichier /tmp/test.log contient OK'
run_action "Vérifier que le fichier /tmp/test.log contient OK"
echo 'ERROR: Exception in core handler file_contains: 'canonical_phrase''
echo 'Action: Vérifier que le fichier /tmp/test.log contient exactement ALLGOOD'
run_action "Vérifier que le fichier /tmp/test.log contient exactement ALLGOOD"
echo 'ERROR: Exception in core handler file_contains: 'canonical_phrase''
echo 'Action: Vérifier que le dossier /tmp/testdir existe'
run_action "Vérifier que le dossier /tmp/testdir existe"
echo 'ERROR: Could not import handler dir_exists: No module named 'shtest_compiler.utils''
echo 'Action: Vérifier que le dossier /tmp/testdir a les droits 0755'
run_action "Vérifier que le dossier /tmp/testdir a les droits 0755"
# le dossier /tmp/testdir a les droits 0755
if test "$(stat -c '%a' '/tmp/testdir')" = '0755'; then
    echo 'OK: le dossier /tmp/testdir a les droits 0755'
else
    echo 'FAIL: le dossier /tmp/testdir n'\''a pas les droits 0755'
    exit 1
fi
echo 'Action: Vérifier que le dossier /tmp/testdir contient 2 fichiers *.txt'
run_action "Vérifier que le dossier /tmp/testdir contient 2 fichiers *.txt"
# le dossier /tmp/testdir contient 2 fichiers correspondant au motif *.txt
if test "$(find '/tmp/testdir' -type f -name '*.txt' | wc -l)" -eq 2; then
    echo 'OK: le dossier /tmp/testdir contient 2 fichiers correspondant au motif *.txt'
else
    echo 'FAIL: le dossier /tmp/testdir ne contient pas 2 fichiers correspondant au motif *.txt'
    exit 1
fi
echo 'Action: Vérifier que la date du fichier /tmp/test.log est 202501010000'
run_action "Vérifier que la date du fichier /tmp/test.log est 202501010000"
# date_modified
if test "$(date -r '/tmp/test.log' +%Y%m%d%H%M)" = '202501010000'; then
    echo 'OK: date_modified'
else
    echo 'FAIL: NOT(date_modified)'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0