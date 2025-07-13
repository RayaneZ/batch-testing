from shtest_compiler.compiler.sql_drivers import get_sql_command
import os

class SQLScriptCommand:
    def __init__(self, script, driver="oracle"):
        self.script = script
        self.driver = driver
    def to_shell(self):
        # Utiliser le système sql_drivers pour générer la commande appropriée
        sql_conn = os.environ.get("SQL_CONN", "")
        cmd = get_sql_command(script=self.script, conn=sql_conn, driver=self.driver)
        return f'run_cmd "{cmd}"'
 
def handle(groups, scope=None, driver="oracle"):
    script, = groups
    return SQLScriptCommand(script=script, driver=driver) 