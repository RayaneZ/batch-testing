import os
import tempfile

class SQLExportCommand:
    def __init__(self, query, output_file, driver="oracle", format="excel"):
        self.query = query
        self.output_file = output_file
        self.driver = driver
        self.format = format
        
    def to_shell(self):
        # First execute the query and save to temporary file
        temp_output = f"temp_sql_output_{hash(self.query) % 10000}.csv"
        
        # Generate the SQL execution command
        sql_conn = os.environ.get("SQL_CONN", "")
        
        if self.driver == "oracle":
            sql_cmd = self._oracle_export(sql_conn, temp_output)
        elif self.driver == "postgres":
            sql_cmd = self._postgres_export(sql_conn, temp_output)
        elif self.driver == "mysql":
            sql_cmd = self._mysql_export(sql_conn, temp_output)
        else:
            sql_cmd = self._oracle_export(sql_conn, temp_output)
        
        # Convert to Excel if needed
        if self.format.lower() == "excel":
            excel_cmd = self._convert_to_excel(temp_output)
            return f"{sql_cmd} && {excel_cmd}"
        else:
            # Just copy the CSV output
            return f"{sql_cmd} && cp {temp_output} {self.output_file} && rm -f {temp_output}"
    
    def _oracle_export(self, sql_conn, temp_output):
        """Export Oracle query results to CSV"""
        temp_sql = f"temp_query_{hash(self.query) % 10000}.sql"
        return f'''cat > {temp_sql} << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
{self.query}
EOF
{self._get_oracle_command(temp_sql, sql_conn)} > {temp_output}
rm -f {temp_sql}'''
    
    def _postgres_export(self, sql_conn, temp_output):
        """Export PostgreSQL query results to CSV"""
        return f'''echo "{self.query}" | psql "{sql_conn}" -A -t --csv > {temp_output}'''
    
    def _mysql_export(self, sql_conn, temp_output):
        """Export MySQL query results to CSV"""
        return f'''echo "{self.query}" | mysql "{sql_conn}" --batch --raw > {temp_output}'''
    
    def _get_oracle_command(self, script, conn):
        """Get Oracle command with proper formatting"""
        return f"sqlplus -s {conn} @{script}"
    
    def _convert_to_excel(self, csv_file):
        """Convert CSV to Excel using Python"""
        return f'''python3 -c "
import pandas as pd
import sys
try:
    df = pd.read_csv('{csv_file}', header=None)
    df.to_excel('{self.output_file}', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {{e}}', file=sys.stderr)
    sys.exit(1)
" && rm -f {csv_file}'''

def handle(*groups, scope=None, driver="oracle", format="excel"):
    query, output_file = groups[:2]
    return SQLExportCommand(query=query, output_file=output_file, driver=driver, format=format) 