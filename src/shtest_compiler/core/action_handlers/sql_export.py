import os

from shtest_compiler.ast.shell_framework_ast import ActionNode


class SQLExportAction(ActionNode):
    def __init__(self, query, sql_conn, output_file, driver="oracle", format="excel"):
        self.query = query
        self.sql_conn = sql_conn
        self.output_file = output_file
        self.driver = driver
        self.format = format

    def to_shell(self):
        temp_output = f"temp_sql_output_{hash(self.query) % 10000}.csv"
        try:
            if self.driver == "oracle":
                sql_cmd = self._oracle_export(temp_output)
            elif self.driver == "postgres":
                sql_cmd = self._postgres_export(temp_output)
            elif self.driver == "mysql":
                sql_cmd = self._mysql_export(temp_output)
            else:
                sql_cmd = self._oracle_export(temp_output)
            if self.format.lower() == "excel":
                excel_cmd = self._convert_to_excel(temp_output)
                return f"{sql_cmd} && {excel_cmd}"
            else:
                return f"{sql_cmd} && cp {temp_output} {self.output_file} && rm -f {temp_output}"
        except Exception as e:
            from shtest_compiler.utils.logger import log_pipeline_error
            import traceback
            log_pipeline_error(f"[ERROR] {type(e).__name__}: {e}\n{traceback.format_exc()}")
            raise

    def _oracle_export(self, temp_output):
        temp_sql = f"temp_query_{hash(self.query) % 10000}.sql"
        return f"""cat > {temp_sql} << 'EOF'
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON
SET TRIMOUT ON
{self.query}
EOF
{self._get_oracle_command(temp_sql, self.sql_conn)} > {temp_output}
rm -f {temp_sql}"""

    def _postgres_export(self, temp_output):
        return (
            f"""echo "{self.query}" | psql "{self.sql_conn}" -A -t --csv > {temp_output}"""
        )

    def _mysql_export(self, temp_output):
        return f"""echo "{self.query}" | mysql "{self.sql_conn}" --batch --raw > {temp_output}"""

    def _get_oracle_command(self, script, conn):
        return f"sqlplus -s {conn} @{script}"

    def _convert_to_excel(self, csv_file):
        return f"""python3 -c "
import pandas as pd
import sys
try:
    df = pd.read_csv('{csv_file}', header=None)
    df.to_excel('{self.output_file}', index=False, header=False)
    print('Excel file created successfully')
except Exception as e:
    print(f'Error converting to Excel: {{e}}', file=sys.stderr)
    sys.exit(1)
" && rm -f {csv_file}"""


def handle(params):
    query = params["query"]
    sql_conn = params["SQL_CONN"]
    output_file = params["output_file"]
    driver = params.get("SQL_DRIVER", params.get("driver", "oracle"))
    format = params.get("format", "excel")
    return SQLExportAction(query, sql_conn, output_file, driver, format)
