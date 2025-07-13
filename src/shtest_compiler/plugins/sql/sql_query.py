from shtest_compiler.compiler.sql_drivers import get_sql_command
import os
import tempfile

class SQLQueryCommand:
    def __init__(self, query, output_file=None, driver="oracle"):
        self.query = query
        self.output_file = output_file
        self.driver = driver
        
    def to_shell(self):
        # Create a temporary SQL file with the query
        sql_conn = os.environ.get("SQL_CONN", "")
        
        # Generate the SQL command based on driver
        if self.driver == "oracle":
            # For Oracle, we need to handle the output differently
            if self.output_file:
                return self._oracle_query_with_output(sql_conn)
            else:
                return self._oracle_query_stdout(sql_conn)
        elif self.driver == "postgres":
            return self._postgres_query(sql_conn)
        elif self.driver == "mysql":
            return self._mysql_query(sql_conn)
        else:
            # Default to Oracle behavior
            return self._oracle_query_stdout(sql_conn)
    
    def _oracle_query_stdout(self, sql_conn):
        """Execute Oracle query and output to stdout"""
        # Create temporary SQL file
        temp_sql = f"temp_query_{hash(self.query) % 10000}.sql"
        return f'''cat > {temp_sql} << 'EOF'
{self.query}
EOF
{get_sql_command(temp_sql, sql_conn, self.driver)}
rm -f {temp_sql}'''
    
    def _oracle_query_with_output(self, sql_conn):
        """Execute Oracle query and save output to file"""
        temp_sql = f"temp_query_{hash(self.query) % 10000}.sql"
        return f'''cat > {temp_sql} << 'EOF'
{self.query}
EOF
{get_sql_command(temp_sql, sql_conn, self.driver)} > {self.output_file}
rm -f {temp_sql}'''
    
    def _postgres_query(self, sql_conn):
        """Execute PostgreSQL query"""
        if self.output_file:
            return f'''echo "{self.query}" | psql "{sql_conn}" -A -t > {self.output_file}'''
        else:
            return f'''echo "{self.query}" | psql "{sql_conn}" -A -t'''
    
    def _mysql_query(self, sql_conn):
        """Execute MySQL query"""
        if self.output_file:
            return f'''echo "{self.query}" | mysql "{sql_conn}" > {self.output_file}'''
        else:
            return f'''echo "{self.query}" | mysql "{sql_conn}"'''

def handle(*groups, scope=None, driver="oracle", output_file=None):
    query, = groups
    return SQLQueryCommand(query=query, output_file=output_file, driver=driver) 