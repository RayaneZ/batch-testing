from shtest_compiler.ast.shell_framework_ast import ActionNode
from shtest_compiler.compiler.sql_drivers import get_sql_command
import os

class RunSQLScriptAction(ActionNode):
    def __init__(self, script, driver="oracle"):
        self.script = script
        self.driver = driver
    def to_shell(self):
        sql_conn = os.environ.get("SQL_CONN", "")
        cmd = get_sql_command(script=self.script, conn=sql_conn, driver=self.driver)
        return f'run_cmd "{cmd}"'

def handle(params):
    script = params['script']
    driver = params.get('driver', 'oracle')
    return RunSQLScriptAction(script, driver) 