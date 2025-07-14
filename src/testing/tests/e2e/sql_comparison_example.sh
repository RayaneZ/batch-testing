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
    # stdout contient excel file created successfully
    echo "$stdout" | grep -q "excel file created successfully"
}

helper_2() {
    # stdout contient comparison_success
    echo "$stdout" | grep -q "comparison_success"
}

# Test step: Configuration de la base de données
echo 'Action: définir la variable SQL_CONN = user/password@testdb'
run_action "export SQL_CONN='user/password@testdb'"
# variable sql_conn vaut user/password@testdb
if test "$sql_conn" = "user/password@testdb"; then
    echo 'OK: variable sql_conn vaut user/password@testdb'
else
    echo 'FAIL: variable sql_conn ne vaut pas user/password@testdb'
    exit 1
fi

# Test step: Test d'export de requête simple
echo 'Action: exporter les résultats de la requête SELECT COUNT(*) FROM employees vers employees_count.xlsx'
run_action "exporter les résultats de la requête SELECT COUNT(*) FROM employees vers employees_count.xlsx"
helper_1 

# Test step: Test de comparaison de requêtes identiques
echo 'Action: comparer les résultats de la requête SELECT * FROM employees WHERE department = 'IT' avec SELECT * FROM employees WHERE department = 'IT''
run_action "cat > temp_query_3374.sql << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
SELECT * FROM employees WHERE department = 'IT'
EOF
sqlplus -s  @temp_query_3374.sql > temp_csv_3374.csv
python3 -c \"
import pandas as pd
import sys
try:
    df = pd.read_csv('temp_csv_3374.csv', header=None)
    df.to_excel('temp_compare_1_3374.xlsx', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {e}', file=sys.stderr)
    sys.exit(1)
\"
rm -f temp_query_3374.sql temp_csv_3374.csv && cat > temp_query_3374.sql << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
SELECT * FROM employees WHERE department = 'IT'
EOF
sqlplus -s  @temp_query_3374.sql > temp_csv_3374.csv
python3 -c \"
import pandas as pd
import sys
try:
    df = pd.read_csv('temp_csv_3374.csv', header=None)
    df.to_excel('temp_compare_2_3374.xlsx', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {e}', file=sys.stderr)
    sys.exit(1)
\"
rm -f temp_query_3374.sql temp_csv_3374.csv && python3 -c \"
import pandas as pd
import numpy as np
import sys

def compare_excel_files(file1, file2, tolerance=0.0, ignore_order=False):
    try:
        df1 = pd.read_excel(file1, header=None)
        df2 = pd.read_excel(file2, header=None)
        for col in df1.columns:
            try:
                df1[col] = pd.to_numeric(df1[col], errors='ignore')
                df2[col] = pd.to_numeric(df2[col], errors='ignore')
            except:
                pass
        if ignore_order:
            df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
            df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)
        else:
            df1_sorted = df1.reset_index(drop=True)
            df2_sorted = df2.reset_index(drop=True)
        if df1_sorted.shape != df2_sorted.shape:
            print(f'SHAPE_MISMATCH: {df1_sorted.shape} vs {df2_sorted.shape}')
            return False
        if tolerance > 0:
            numeric_cols = df1_sorted.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                diff = np.abs(df1_sorted[numeric_cols] - df2_sorted[numeric_cols])
                if (diff > tolerance).any().any():
                    print(f'TOLERANCE_EXCEEDED: Max difference {diff.max().max()} > {tolerance}')
                    return False
        if not df1_sorted.equals(df2_sorted):
            print('EXACT_MISMATCH: Values differ')
            return False
        print('COMPARISON_SUCCESS: Files are identical')
        return True
    except Exception as e:
        print(f'COMPARISON_ERROR: {e}')
        return False
success = compare_excel_files('temp_compare_1_3374.xlsx', 'temp_compare_2_3374.xlsx')
if not success:
    sys.exit(1)
\" && rm -f temp_compare_1_3374.xlsx temp_compare_2_3374.xlsx"
helper_2 

# Test step: Test de comparaison avec tolérance numérique
echo 'Action: comparer les résultats de la requête SELECT AVG(salary) FROM employees avec SELECT AVG(salary) FROM employees'
run_action "cat > temp_query_9408.sql << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
SELECT AVG(salary) FROM employees
EOF
sqlplus -s  @temp_query_9408.sql > temp_csv_9408.csv
python3 -c \"
import pandas as pd
import sys
try:
    df = pd.read_csv('temp_csv_9408.csv', header=None)
    df.to_excel('temp_compare_1_9408.xlsx', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {e}', file=sys.stderr)
    sys.exit(1)
\"
rm -f temp_query_9408.sql temp_csv_9408.csv && cat > temp_query_9408.sql << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
SELECT AVG(salary) FROM employees
EOF
sqlplus -s  @temp_query_9408.sql > temp_csv_9408.csv
python3 -c \"
import pandas as pd
import sys
try:
    df = pd.read_csv('temp_csv_9408.csv', header=None)
    df.to_excel('temp_compare_2_9408.xlsx', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {e}', file=sys.stderr)
    sys.exit(1)
\"
rm -f temp_query_9408.sql temp_csv_9408.csv && python3 -c \"
import pandas as pd
import numpy as np
import sys

def compare_excel_files(file1, file2, tolerance=0.0, ignore_order=False):
    try:
        df1 = pd.read_excel(file1, header=None)
        df2 = pd.read_excel(file2, header=None)
        for col in df1.columns:
            try:
                df1[col] = pd.to_numeric(df1[col], errors='ignore')
                df2[col] = pd.to_numeric(df2[col], errors='ignore')
            except:
                pass
        if ignore_order:
            df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
            df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)
        else:
            df1_sorted = df1.reset_index(drop=True)
            df2_sorted = df2.reset_index(drop=True)
        if df1_sorted.shape != df2_sorted.shape:
            print(f'SHAPE_MISMATCH: {df1_sorted.shape} vs {df2_sorted.shape}')
            return False
        if tolerance > 0:
            numeric_cols = df1_sorted.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                diff = np.abs(df1_sorted[numeric_cols] - df2_sorted[numeric_cols])
                if (diff > tolerance).any().any():
                    print(f'TOLERANCE_EXCEEDED: Max difference {diff.max().max()} > {tolerance}')
                    return False
        if not df1_sorted.equals(df2_sorted):
            print('EXACT_MISMATCH: Values differ')
            return False
        print('COMPARISON_SUCCESS: Files are identical')
        return True
    except Exception as e:
        print(f'COMPARISON_ERROR: {e}')
        return False
success = compare_excel_files('temp_compare_1_9408.xlsx', 'temp_compare_2_9408.xlsx')
if not success:
    sys.exit(1)
\" && rm -f temp_compare_1_9408.xlsx temp_compare_2_9408.xlsx"
helper_2 

# Test step: Test d'exécution de requête simple
echo 'Action: exécuter la requête SELECT COUNT(*) FROM employees'
run_action "sh 'la requête SELECT COUNT(*) FROM employees'"
# stdout contient un nombre
if echo "$stdout" | grep -q "un nombre"; then
    echo 'OK: stdout contient un nombre'
else
    echo 'FAIL: stdout ne contient pas un nombre'
    exit 1
fi

# Test step: Test d'export avec format personnalisé
echo 'Action: exporter les résultats de la requête SELECT name, salary FROM employees ORDER BY salary DESC vers top_salaries.xlsx'
run_action "exporter les résultats de la requête SELECT name, salary FROM employees ORDER BY salary DESC vers top_salaries.xlsx"
helper_1 

# Test step: Test de comparaison avec ordre ignoré
echo 'Action: comparer les résultats de la requête SELECT name, department FROM employees ORDER BY name avec SELECT name, department FROM employees ORDER BY department (ignorer l'ordre lors de la comparaison)'
run_action "cat > temp_query_1260.sql << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
SELECT name, department FROM employees ORDER BY name
EOF
sqlplus -s  @temp_query_1260.sql > temp_csv_1260.csv
python3 -c \"
import pandas as pd
import sys
try:
    df = pd.read_csv('temp_csv_1260.csv', header=None)
    df.to_excel('temp_compare_1_1260.xlsx', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {e}', file=sys.stderr)
    sys.exit(1)
\"
rm -f temp_query_1260.sql temp_csv_1260.csv && cat > temp_query_3336.sql << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
SELECT name, department FROM employees ORDER BY department (ignorer l'ordre lors de la comparaison)
EOF
sqlplus -s  @temp_query_3336.sql > temp_csv_3336.csv
python3 -c \"
import pandas as pd
import sys
try:
    df = pd.read_csv('temp_csv_3336.csv', header=None)
    df.to_excel('temp_compare_2_3336.xlsx', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {e}', file=sys.stderr)
    sys.exit(1)
\"
rm -f temp_query_3336.sql temp_csv_3336.csv && python3 -c \"
import pandas as pd
import numpy as np
import sys

def compare_excel_files(file1, file2, tolerance=0.0, ignore_order=False):
    try:
        df1 = pd.read_excel(file1, header=None)
        df2 = pd.read_excel(file2, header=None)
        for col in df1.columns:
            try:
                df1[col] = pd.to_numeric(df1[col], errors='ignore')
                df2[col] = pd.to_numeric(df2[col], errors='ignore')
            except:
                pass
        if ignore_order:
            df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
            df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)
        else:
            df1_sorted = df1.reset_index(drop=True)
            df2_sorted = df2.reset_index(drop=True)
        if df1_sorted.shape != df2_sorted.shape:
            print(f'SHAPE_MISMATCH: {df1_sorted.shape} vs {df2_sorted.shape}')
            return False
        if tolerance > 0:
            numeric_cols = df1_sorted.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                diff = np.abs(df1_sorted[numeric_cols] - df2_sorted[numeric_cols])
                if (diff > tolerance).any().any():
                    print(f'TOLERANCE_EXCEEDED: Max difference {diff.max().max()} > {tolerance}')
                    return False
        if not df1_sorted.equals(df2_sorted):
            print('EXACT_MISMATCH: Values differ')
            return False
        print('COMPARISON_SUCCESS: Files are identical')
        return True
    except Exception as e:
        print(f'COMPARISON_ERROR: {e}')
        return False
success = compare_excel_files('temp_compare_1_1260.xlsx', 'temp_compare_2_3336.xlsx')
if not success:
    sys.exit(1)
\" && rm -f temp_compare_1_1260.xlsx temp_compare_2_3336.xlsx"
helper_2 

# Test step: Test de comparaison sans ordre - données identiques
echo 'Action: comparer les résultats de la requête SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY salary avec SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY name (ignorer l'ordre lors de la comparaison)'
run_action "cat > temp_query_9015.sql << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY salary
EOF
sqlplus -s  @temp_query_9015.sql > temp_csv_9015.csv
python3 -c \"
import pandas as pd
import sys
try:
    df = pd.read_csv('temp_csv_9015.csv', header=None)
    df.to_excel('temp_compare_1_9015.xlsx', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {e}', file=sys.stderr)
    sys.exit(1)
\"
rm -f temp_query_9015.sql temp_csv_9015.csv && cat > temp_query_3790.sql << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
SELECT id, name, salary FROM employees WHERE department = 'HR' ORDER BY name (ignorer l'ordre lors de la comparaison)
EOF
sqlplus -s  @temp_query_3790.sql > temp_csv_3790.csv
python3 -c \"
import pandas as pd
import sys
try:
    df = pd.read_csv('temp_csv_3790.csv', header=None)
    df.to_excel('temp_compare_2_3790.xlsx', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {e}', file=sys.stderr)
    sys.exit(1)
\"
rm -f temp_query_3790.sql temp_csv_3790.csv && python3 -c \"
import pandas as pd
import numpy as np
import sys

def compare_excel_files(file1, file2, tolerance=0.0, ignore_order=False):
    try:
        df1 = pd.read_excel(file1, header=None)
        df2 = pd.read_excel(file2, header=None)
        for col in df1.columns:
            try:
                df1[col] = pd.to_numeric(df1[col], errors='ignore')
                df2[col] = pd.to_numeric(df2[col], errors='ignore')
            except:
                pass
        if ignore_order:
            df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
            df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)
        else:
            df1_sorted = df1.reset_index(drop=True)
            df2_sorted = df2.reset_index(drop=True)
        if df1_sorted.shape != df2_sorted.shape:
            print(f'SHAPE_MISMATCH: {df1_sorted.shape} vs {df2_sorted.shape}')
            return False
        if tolerance > 0:
            numeric_cols = df1_sorted.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                diff = np.abs(df1_sorted[numeric_cols] - df2_sorted[numeric_cols])
                if (diff > tolerance).any().any():
                    print(f'TOLERANCE_EXCEEDED: Max difference {diff.max().max()} > {tolerance}')
                    return False
        if not df1_sorted.equals(df2_sorted):
            print('EXACT_MISMATCH: Values differ')
            return False
        print('COMPARISON_SUCCESS: Files are identical')
        return True
    except Exception as e:
        print(f'COMPARISON_ERROR: {e}')
        return False
success = compare_excel_files('temp_compare_1_9015.xlsx', 'temp_compare_2_3790.xlsx')
if not success:
    sys.exit(1)
\" && rm -f temp_compare_1_9015.xlsx temp_compare_2_3790.xlsx"
helper_2 

# Test step: Test de comparaison sans ordre - données différentes
echo 'Action: comparer les résultats de la requête SELECT name FROM employees WHERE department = 'IT' avec SELECT name FROM employees WHERE department = 'HR' (ignorer l'ordre lors de la comparaison)'
run_action "cat > temp_query_1337.sql << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
SELECT name FROM employees WHERE department = 'IT'
EOF
sqlplus -s  @temp_query_1337.sql > temp_csv_1337.csv
python3 -c \"
import pandas as pd
import sys
try:
    df = pd.read_csv('temp_csv_1337.csv', header=None)
    df.to_excel('temp_compare_1_1337.xlsx', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {e}', file=sys.stderr)
    sys.exit(1)
\"
rm -f temp_query_1337.sql temp_csv_1337.csv && cat > temp_query_4095.sql << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
SELECT name FROM employees WHERE department = 'HR' (ignorer l'ordre lors de la comparaison)
EOF
sqlplus -s  @temp_query_4095.sql > temp_csv_4095.csv
python3 -c \"
import pandas as pd
import sys
try:
    df = pd.read_csv('temp_csv_4095.csv', header=None)
    df.to_excel('temp_compare_2_4095.xlsx', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {e}', file=sys.stderr)
    sys.exit(1)
\"
rm -f temp_query_4095.sql temp_csv_4095.csv && python3 -c \"
import pandas as pd
import numpy as np
import sys

def compare_excel_files(file1, file2, tolerance=0.0, ignore_order=False):
    try:
        df1 = pd.read_excel(file1, header=None)
        df2 = pd.read_excel(file2, header=None)
        for col in df1.columns:
            try:
                df1[col] = pd.to_numeric(df1[col], errors='ignore')
                df2[col] = pd.to_numeric(df2[col], errors='ignore')
            except:
                pass
        if ignore_order:
            df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
            df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)
        else:
            df1_sorted = df1.reset_index(drop=True)
            df2_sorted = df2.reset_index(drop=True)
        if df1_sorted.shape != df2_sorted.shape:
            print(f'SHAPE_MISMATCH: {df1_sorted.shape} vs {df2_sorted.shape}')
            return False
        if tolerance > 0:
            numeric_cols = df1_sorted.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                diff = np.abs(df1_sorted[numeric_cols] - df2_sorted[numeric_cols])
                if (diff > tolerance).any().any():
                    print(f'TOLERANCE_EXCEEDED: Max difference {diff.max().max()} > {tolerance}')
                    return False
        if not df1_sorted.equals(df2_sorted):
            print('EXACT_MISMATCH: Values differ')
            return False
        print('COMPARISON_SUCCESS: Files are identical')
        return True
    except Exception as e:
        print(f'COMPARISON_ERROR: {e}')
        return False
success = compare_excel_files('temp_compare_1_1337.xlsx', 'temp_compare_2_4095.xlsx')
if not success:
    sys.exit(1)
\" && rm -f temp_compare_1_1337.xlsx temp_compare_2_4095.xlsx"
# stdout contient comparison_error
if echo "$stdout" | grep -q "comparison_error"; then
    echo 'OK: stdout contient comparison_error'
else
    echo 'FAIL: stdout ne contient pas comparison_error'
    exit 1
fi

echo 'All steps and validations passed.'
exit 0