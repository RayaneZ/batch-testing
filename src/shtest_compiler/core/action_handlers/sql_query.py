import os

from shtest_compiler.ast.shell_framework_ast import ActionNode
from shtest_compiler.compiler.sql_drivers import get_sql_command


class SQLQueryAction(ActionNode):
    def __init__(self, query, sql_conn, output_file=None, driver="oracle"):
        self.query = query
        self.sql_conn = sql_conn
        self.output_file = output_file
        self.driver = driver

    def to_shell(self):
        if self.driver == "oracle":
            if self.output_file:
                return self._oracle_query_with_output()
            else:
                return self._oracle_query_stdout()
        elif self.driver == "postgres":
            return self._postgres_query()
        elif self.driver == "mysql":
            return self._mysql_query()
        else:
            return self._oracle_query_stdout()

    def _oracle_query_stdout(self):
        temp_sql = f"temp_query_{hash(self.query) % 10000}.sql"
        return f"""cat > {temp_sql} << 'EOF'
{self.query}
EOF
{get_sql_command(temp_sql, self.sql_conn, self.driver)}
rm -f {temp_sql}"""

    def _oracle_query_with_output(self):
        temp_sql = f"temp_query_{hash(self.query) % 10000}.sql"
        return f"""cat > {temp_sql} << 'EOF'
{self.query}
EOF
{get_sql_command(temp_sql, self.sql_conn, self.driver)} > {self.output_file}
rm -f {temp_sql}"""

    def _postgres_query(self):
        if self.output_file:
            return f"""echo "{self.query}" | psql "{self.sql_conn}" -A -t > {self.output_file}"""
        else:
            return f"""echo "{self.query}" | psql "{self.sql_conn}" -A -t"""

    def _mysql_query(self):
        if self.output_file:
            return f"""echo "{self.query}" | mysql "{self.sql_conn}" > {self.output_file}"""
        else:
            return f'''echo "{self.query}" | mysql "{self.sql_conn}"'''


def handle(params):
    query = params["query"]
    sql_conn = params["SQL_CONN"]
    driver = params.get("SQL_DRIVER", params.get("driver", "oracle"))
    output_file = params.get("output_file", None)
    return SQLQueryAction(query, sql_conn, output_file, driver)
