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


# Test step: Connexion personnalisée
echo 'Action: SQL_CONN=my_user/my_pass@base'
run_action "SQL_CONN=my_user/my_pass@base"
# variable sql_conn vaut my_user/my_pass@base
if test "$sql_conn" = "my_user/my_pass@base"; then
    echo 'OK: variable sql_conn vaut my_user/my_pass@base'
else
    echo 'FAIL: variable sql_conn ne vaut pas my_user/my_pass@base'
    exit 1
fi
echo 'Action: init_custom.sql'
run_action "init_custom.sql"
# stdout contient ok
if echo "$stdout" | grep -q "ok"; then
    echo 'OK: stdout contient ok'
else
    echo 'FAIL: stdout ne contient pas ok'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0