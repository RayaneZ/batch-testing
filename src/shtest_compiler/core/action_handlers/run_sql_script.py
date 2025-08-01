import os

from shtest_compiler.ast.shell_framework_ast import ActionNode
from shtest_compiler.compiler.sql_drivers import get_sql_command


class RunSQLScriptAction(ActionNode):
    def __init__(self, script, sql_conn, driver="oracle"):
        self.script = script
        self.sql_conn = sql_conn
        self.driver = driver

    def to_shell(self):
        cmd = get_sql_command(script=self.script, conn=self.sql_conn, driver=self.driver)
        return f'run_cmd "{cmd}"'


def handle(params):
    script = params["script"]
    sql_conn = params["SQL_CONN"]
    driver = params.get("SQL_DRIVER", params.get("driver", "oracle"))
    return RunSQLScriptAction(script, sql_conn, driver)
