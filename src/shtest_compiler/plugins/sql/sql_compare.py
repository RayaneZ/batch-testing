import os

class SQLCompareCommand:
    def __init__(self, query1, query2, driver="oracle", tolerance=0.0, ignore_order=False):
        self.query1 = query1
        self.query2 = query2
        self.driver = driver
        self.tolerance = tolerance
        self.ignore_order = ignore_order
        
    def to_shell(self):
        # Generate temporary files for both queries
        temp_file1 = f"temp_compare_1_{hash(self.query1) % 10000}.xlsx"
        temp_file2 = f"temp_compare_2_{hash(self.query2) % 10000}.xlsx"
        
        # Export both queries to Excel
        export_cmd1 = self._export_query(self.query1, temp_file1)
        export_cmd2 = self._export_query(self.query2, temp_file2)
        
        # Compare the Excel files
        compare_cmd = self._compare_excel_files(temp_file1, temp_file2)
        
        # Cleanup
        cleanup_cmd = f"rm -f {temp_file1} {temp_file2}"
        
        return f"{export_cmd1} && {export_cmd2} && {compare_cmd} && {cleanup_cmd}"
    
    def _export_query(self, query, output_file):
        """Export a single query to Excel"""
        sql_conn = os.environ.get("SQL_CONN", "")
        
        if self.driver == "oracle":
            return self._oracle_export(query, sql_conn, output_file)
        elif self.driver == "postgres":
            return self._postgres_export(query, sql_conn, output_file)
        elif self.driver == "mysql":
            return self._mysql_export(query, sql_conn, output_file)
        else:
            return self._oracle_export(query, sql_conn, output_file)
    
    def _oracle_export(self, query, sql_conn, output_file):
        """Export Oracle query to Excel"""
        temp_sql = f"temp_query_{hash(query) % 10000}.sql"
        temp_csv = f"temp_csv_{hash(query) % 10000}.csv"
        
        return f'''cat > {temp_sql} << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
{query}
EOF
sqlplus -s {sql_conn} @{temp_sql} > {temp_csv}
python3 -c "
import pandas as pd
import sys
try:
    df = pd.read_csv('{temp_csv}', header=None)
    df.to_excel('{output_file}', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {{e}}', file=sys.stderr)
    sys.exit(1)
"
rm -f {temp_sql} {temp_csv}'''
    
    def _postgres_export(self, query, sql_conn, output_file):
        """Export PostgreSQL query to Excel"""
        temp_csv = f"temp_csv_{hash(query) % 10000}.csv"
        
        return f'''echo "{query}" | psql "{sql_conn}" -A -t --csv > {temp_csv}
python3 -c "
import pandas as pd
import sys
try:
    df = pd.read_csv('{temp_csv}', header=None)
    df.to_excel('{output_file}', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {{e}}', file=sys.stderr)
    sys.exit(1)
"
rm -f {temp_csv}'''
    
    def _mysql_export(self, query, sql_conn, output_file):
        """Export MySQL query to Excel"""
        temp_csv = f"temp_csv_{hash(query) % 10000}.csv"
        
        return f'''echo "{query}" | mysql "{sql_conn}" --batch --raw > {temp_csv}
python3 -c "
import pandas as pd
import sys
try:
    df = pd.read_csv('{temp_csv}', header=None)
    df.to_excel('{output_file}', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {{e}}', file=sys.stderr)
    sys.exit(1)
"
rm -f {temp_csv}'''
    
    def _compare_excel_files(self, file1, file2):
        """Compare two Excel files and return comparison result"""
        ignore_order_flag = "True" if self.ignore_order else "False"
        
        return f'''python3 -c "
import pandas as pd
import numpy as np
import sys

def compare_excel_files(file1, file2, tolerance={self.tolerance}, ignore_order={ignore_order_flag}):
    try:
        # Read Excel files
        df1 = pd.read_excel(file1, header=None)
        df2 = pd.read_excel(file2, header=None)
        
        # Convert to numeric where possible for tolerance comparison
        for col in df1.columns:
            try:
                df1[col] = pd.to_numeric(df1[col], errors='ignore')
                df2[col] = pd.to_numeric(df2[col], errors='ignore')
            except:
                pass
        
        if ignore_order:
            # Sort both dataframes by all columns
            df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
            df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)
        else:
            df1_sorted = df1.reset_index(drop=True)
            df2_sorted = df2.reset_index(drop=True)
        
        # Check if shapes match
        if df1_sorted.shape != df2_sorted.shape:
            print(f'SHAPE_MISMATCH: {{df1_sorted.shape}} vs {{df2_sorted.shape}}')
            return False
        
        # Compare values with tolerance
        if tolerance > 0:
            # For numeric comparison with tolerance
            numeric_cols = df1_sorted.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                diff = np.abs(df1_sorted[numeric_cols] - df2_sorted[numeric_cols])
                if (diff > tolerance).any().any():
                    print(f'TOLERANCE_EXCEEDED: Max difference {{diff.max().max()}} > {{tolerance}}')
                    return False
        
        # Exact comparison for non-numeric and remaining columns
        if not df1_sorted.equals(df2_sorted):
            print('EXACT_MISMATCH: Values differ')
            return False
        
        print('COMPARISON_SUCCESS: Files are identical')
        return True
        
    except Exception as e:
        print(f'COMPARISON_ERROR: {{e}}')
        return False

# Execute comparison
success = compare_excel_files('{file1}', '{file2}')
if not success:
    sys.exit(1)
"'''

def handle(*groups, scope=None, driver="oracle", tolerance=0.0, ignore_order=False):
    # Always take the first two as queries
    query1, query2 = groups[:2]
    # If any group contains the ignore order flag, set ignore_order True
    if any("ignorer l'ordre lors de la comparaison" in str(g) for g in groups):
        ignore_order = True
    return SQLCompareCommand(query1=query1, query2=query2, driver=driver, tolerance=tolerance, ignore_order=ignore_order) 