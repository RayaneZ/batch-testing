
# sql_drivers.py

# Dictionnaire associant chaque driver à sa commande SQL
SQL_DRIVERS = {
    "oracle": lambda script, conn: f"sqlplus -s {conn} @{script}",
    "postgres": lambda script, conn: f'psql "$SQL_URL" -f {script}',
    "mysql": lambda script, conn: f'mysql "$SQL_URL" < {script}',
    "redis": lambda script, conn: f'redis-cli < {script}',
}

def get_sql_command(script: str, conn: str, driver: str) -> str:
    """
    Retourne la commande shell à exécuter pour lancer un script SQL,
    en fonction du type de base de données (driver).
    """
    driver = driver.lower()
    if driver in SQL_DRIVERS:
        return SQL_DRIVERS[driver](script, conn)
    raise ValueError(f"Unsupported SQL driver: {driver}")
