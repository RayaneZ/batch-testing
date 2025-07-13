from shtest_compiler.ast.shell_framework_ast import ActionNode
from shtest_compiler.compiler.sql_drivers import get_sql_command
import os

class SQLQueryAction(ActionNode):
    def __init__(self, query, output_file=None, driver="oracle"):
        self.query = query
        self.output_file = output_file
        self.driver = driver
    def to_shell(self):
        sql_conn = os.environ.get("SQL_CONN", "")
        if self.driver == "oracle":
            if self.output_file:
                return self._oracle_query_with_output(sql_conn)
            else:
                return self._oracle_query_stdout(sql_conn)
        elif self.driver == "postgres":
            return self._postgres_query(sql_conn)
        elif self.driver == "mysql":
            return self._mysql_query(sql_conn)
        else:
            return self._oracle_query_stdout(sql_conn)
    def _oracle_query_stdout(self, sql_conn):
        temp_sql = f"temp_query_{hash(self.query) % 10000}.sql"
        return f'''cat > {temp_sql} << 'EOF'
{self.query}
EOF
{get_sql_command(temp_sql, sql_conn, self.driver)}
rm -f {temp_sql}'''
    def _oracle_query_with_output(self, sql_conn):
        temp_sql = f"temp_query_{hash(self.query) % 10000}.sql"
        return f'''cat > {temp_sql} << 'EOF'
{self.query}
EOF
{get_sql_command(temp_sql, sql_conn, self.driver)} > {self.output_file}
rm -f {temp_sql}'''
    def _postgres_query(self, sql_conn):
        if self.output_file:
            return f'''echo "{self.query}" | psql "{sql_conn}" -A -t > {self.output_file}'''
        else:
            return f'''echo "{self.query}" | psql "{sql_conn}" -A -t'''
    def _mysql_query(self, sql_conn):
        if self.output_file:
            return f'''echo "{self.query}" | mysql "{sql_conn}" > {self.output_file}'''
        else:
            return f'''echo "{self.query}" | mysql "{sql_conn}"'''

def handle(params):
    query = params['query']
    driver = params.get('driver', 'oracle')
    output_file = params.get('output_file', None)
    return SQLQueryAction(query, output_file, driver) 