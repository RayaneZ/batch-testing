import os
from string import Template

from .mysql import MYSQL_TEMPLATE
from .oracle import ORACLE_TEMPLATE
from .postgres import POSTGRES_TEMPLATE
from .redis import REDIS_TEMPLATE

COMMANDS = {
    "mysql": MYSQL_TEMPLATE,
    "oracle": ORACLE_TEMPLATE,
    "postgres": POSTGRES_TEMPLATE,
    "redis": REDIS_TEMPLATE,
}


def get_sql_command(script: str, conn: str) -> str:
    driver = os.environ.get("SQL_DRIVER", "oracle").lower()
    template = COMMANDS.get(driver, ORACLE_TEMPLATE)
    return template.substitute(script=script, conn=conn)
