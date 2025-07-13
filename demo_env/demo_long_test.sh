#!/bin/bash

# Generated shell script from .shtest file

# Function to log differences
log_diff() {
    local expected="$1"
    local actual="$2"
    if [ "$expected" != "$actual" ]; then
        echo "Expected: $expected"
        echo "Actual: $actual"
    fi
}

# Initialize variables
last_ret=0
test_passed=true

# Test step: Step 1 - Preparation

# Test step: Step 2 - Ancien fichier

# Test step: Step 3 - Nouveau fichier

# Test step: Step 4 - Execution du batch

# Test step: Step 5 - Vérifier la table en base
# Execute: Creer le dossier ./qualification/demo_env
echo "Executing: Creer le dossier ./qualification/demo_env"
stdout=$(Creer le dossier ./qualification/demo_env 2>&1)
last_ret=$?

echo 'ERROR: No directory specified for dir_ready validation'
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: le dossier est cree'
    exit 1
else
    echo '✅ Validation passed: le dossier est cree'
fi


# Execute: Creer le fichier ./qualification/demo_env/initial.txt
echo "Executing: Creer le fichier ./qualification/demo_env/initial.txt"
stdout=$(Creer le fichier ./qualification/demo_env/initial.txt 2>&1)
last_ret=$?

echo 'ERROR: No file specified for file_present validation'
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: le fichier est cree'
    exit 1
else
    echo '✅ Validation passed: le fichier est cree'
fi


# Execute: Définir la variable SQL_CONN = rootme/ffDDD584R@base_name
echo "Executing: Définir la variable SQL_CONN = rootme/ffDDD584R@base_name"
stdout=$(Définir la variable SQL_CONN = rootme/ffDDD584R@base_name 2>&1)
last_ret=$?

result_0=0
if [ -n "$SQL_CONN" ]; then
    result_0=1
    actual="identifiants configurés"
else
    actual="non configuré"
fi
expected="identifiants configurés"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: Les identifiants sont configurés'
    exit 1
else
    echo '✅ Validation passed: Les identifiants sont configurés'
fi


# Execute: toucher le fichier ./qualification/demo_env/old.txt -t 202201010000
echo "Executing: toucher le fichier ./qualification/demo_env/old.txt -t 202201010000"
stdout=$(toucher le fichier ./qualification/demo_env/old.txt -t 202201010000 2>&1)
last_ret=$?

result_0=0
if [ -f "." ]; then
    result_0=1
    actual="date modifiée"
else
    actual="date inchangée"
fi
expected="date modifiée"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: date modifiee'
    exit 1
else
    echo '✅ Validation passed: date modifiee'
fi


# Execute: Creer le fichier ./qualification/demo_env/newfile.txt
echo "Executing: Creer le fichier ./qualification/demo_env/newfile.txt"
stdout=$(Creer le fichier ./qualification/demo_env/newfile.txt 2>&1)
last_ret=$?

echo 'ERROR: No matcher found for validation: fichier crée'
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: fichier crée'
    exit 1
else
    echo '✅ Validation passed: fichier crée'
fi


# Execute: Mettre a jour la date du fichier ./qualification/demo_env/newfile.txt 202401010101
echo "Executing: Mettre a jour la date du fichier ./qualification/demo_env/newfile.txt 202401010101"
stdout=$(Mettre a jour la date du fichier ./qualification/demo_env/newfile.txt 202401010101 2>&1)
last_ret=$?

result_0=0
if [ -f "." ]; then
    result_0=1
    actual="date modifiée"
else
    actual="date inchangée"
fi
expected="date modifiée"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: date modifiee'
    exit 1
else
    echo '✅ Validation passed: date modifiee'
fi


# Execute: Exécuter ./qualification/purge.sh
echo "Executing: Exécuter ./qualification/purge.sh"
stdout=$(Exécuter ./qualification/purge.sh 2>&1)
last_ret=$?

result_0=0
if [ $last_ret -eq 0 ]; then
    result_0=1
    actual="Le script retourne un code 0"
else
    actual="échec"
fi
expected="Le script retourne un code 0"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: Le script retourne un code 0'
    exit 1
else
    echo '✅ Validation passed: Le script retourne un code 0'
fi

echo 'ERROR: No matcher found for validation: (la sortie standard contient "Succès complet"'
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_1 -eq 0 ]; then
    echo '❌ Validation failed: (la sortie standard contient "Succès complet"'
    exit 1
else
    echo '✅ Validation passed: (la sortie standard contient "Succès complet"'
fi

echo 'ERROR: Exception in plugin stderr_contains: StderrContainsValidation.to_shell() missing 1 required positional argument: 'var''
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_2 -eq 0 ]; then
    echo '❌ Validation failed: la sortie d'erreur contient WARNING)'
    exit 1
else
    echo '✅ Validation passed: la sortie d'erreur contient WARNING)'
fi


# Execute: Exécuter /opt/batch/migration.sh
echo "Executing: Exécuter /opt/batch/migration.sh"
stdout=$(Exécuter /opt/batch/migration.sh 2>&1)
last_ret=$?

result_0=0
if [ $last_ret -eq 0 ]; then
    result_0=1
    actual="Le script retourne un code 0"
else
    actual="échec"
fi
expected="Le script retourne un code 0"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: Le script retourne un code 0'
    exit 1
else
    echo '✅ Validation passed: Le script retourne un code 0'
fi


# Execute: Exécuter le script SQL verification.sql
echo "Executing: Exécuter le script SQL verification.sql"
stdout=$(Exécuter le script SQL verification.sql 2>&1)
last_ret=$?

result_0=0
if [ $last_ret -eq 0 ]; then
    result_0=1
    actual="Le script retourne un code 0"
else
    actual="échec"
fi
expected="Le script retourne un code 0"
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: Le script s'execute avec succès'
    exit 1
else
    echo '✅ Validation passed: Le script s'execute avec succès'
fi


# Execute: Comparer le fichier ./output.txt avec ./output_attendu.txt
echo "Executing: Comparer le fichier ./output.txt avec ./output_attendu.txt"
stdout=$(Comparer le fichier ./output.txt avec ./output_attendu.txt 2>&1)
last_ret=$?

echo 'ERROR: Need two files to compare for files_identical validation'
echo "Expected: $expected"
echo "Actual:   $actual"
if [ $result_0 -eq 0 ]; then
    echo '❌ Validation failed: Les fichiers sont identiques'
    exit 1
else
    echo '✅ Validation passed: Les fichiers sont identiques'
fi


# Execute: Creer le dossier ./qualification/demo_env ; Resultat: le dossier est cree.
echo "Executing: Creer le dossier ./qualification/demo_env ; Resultat: le dossier est cree."
stdout=$(Creer le dossier ./qualification/demo_env ; Resultat: le dossier est cree. 2>&1)
last_ret=$?


# Execute: Creer le fichier ./qualification/demo_env/initial.txt ; Resultat: le fichier est cree.
echo "Executing: Creer le fichier ./qualification/demo_env/initial.txt ; Resultat: le fichier est cree."
stdout=$(Creer le fichier ./qualification/demo_env/initial.txt ; Resultat: le fichier est cree. 2>&1)
last_ret=$?


# Execute: Définir la variable SQL_CONN = rootme/ffDDD584R@base_name ; Résultat: Les identifiants sont configurés.
echo "Executing: Définir la variable SQL_CONN = rootme/ffDDD584R@base_name ; Résultat: Les identifiants sont configurés."
stdout=$(Définir la variable SQL_CONN = rootme/ffDDD584R@base_name ; Résultat: Les identifiants sont configurés. 2>&1)
last_ret=$?


# Execute: toucher le fichier ./qualification/demo_env/old.txt -t 202201010000 ; Resultat: date modifiee.
echo "Executing: toucher le fichier ./qualification/demo_env/old.txt -t 202201010000 ; Resultat: date modifiee."
stdout=$(toucher le fichier ./qualification/demo_env/old.txt -t 202201010000 ; Resultat: date modifiee. 2>&1)
last_ret=$?


# Execute: Creer le fichier ./qualification/demo_env/newfile.txt ; Resultat: fichier crée.
echo "Executing: Creer le fichier ./qualification/demo_env/newfile.txt ; Resultat: fichier crée."
stdout=$(Creer le fichier ./qualification/demo_env/newfile.txt ; Resultat: fichier crée. 2>&1)
last_ret=$?


# Execute: Mettre a jour la date du fichier ./qualification/demo_env/newfile.txt 202401010101 ; Resultat: date modifiee.
echo "Executing: Mettre a jour la date du fichier ./qualification/demo_env/newfile.txt 202401010101 ; Resultat: date modifiee."
stdout=$(Mettre a jour la date du fichier ./qualification/demo_env/newfile.txt 202401010101 ; Resultat: date modifiee. 2>&1)
last_ret=$?


# Execute: Exécuter ./qualification/purge.sh ; Résultat: Le script retourne un code 0 et (la sortie standard contient "Succès complet" ou la sortie d'erreur contient WARNING).
echo "Executing: Exécuter ./qualification/purge.sh ; Résultat: Le script retourne un code 0 et (la sortie standard contient "Succès complet" ou la sortie d'erreur contient WARNING)."
stdout=$(Exécuter ./qualification/purge.sh ; Résultat: Le script retourne un code 0 et (la sortie standard contient "Succès complet" ou la sortie d'erreur contient WARNING). 2>&1)
last_ret=$?


# Execute: Exécuter /opt/batch/migration.sh ; Résultat: Le script retourne un code 0.
echo "Executing: Exécuter /opt/batch/migration.sh ; Résultat: Le script retourne un code 0."
stdout=$(Exécuter /opt/batch/migration.sh ; Résultat: Le script retourne un code 0. 2>&1)
last_ret=$?


# Execute: Exécuter le script SQL verification.sql ; Résultat: Le script s'execute avec succès.
echo "Executing: Exécuter le script SQL verification.sql ; Résultat: Le script s'execute avec succès."
stdout=$(Exécuter le script SQL verification.sql ; Résultat: Le script s'execute avec succès. 2>&1)
last_ret=$?


# Execute: Comparer le fichier ./output.txt avec ./output_attendu.txt; Résultat: Les fichiers sont identiques
echo "Executing: Comparer le fichier ./output.txt avec ./output_attendu.txt; Résultat: Les fichiers sont identiques"
stdout=$(Comparer le fichier ./output.txt avec ./output_attendu.txt; Résultat: Les fichiers sont identiques 2>&1)
last_ret=$?



# Final result
if [ "$test_passed" = true ]; then
    echo "✅ Test passed"
    exit 0
else
    echo "❌ Test failed"
    exit 1
fi