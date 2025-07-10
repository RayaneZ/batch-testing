
def get_sql_command(script: str, conn: str, driver: str) -> str:
    driver = driver.lower()
    if driver == "oracle":
        return f"sqlplus -s {conn} @{script}"
    if driver == "postgres":
        return f'psql "$SQL_URL" -f {script}'
    if driver == "mysql":
        return f'mysql "$SQL_URL" < {script}'
    if driver == "redis":
        return f'redis-cli < {script}'
    raise ValueError(f"Unsupported SQL driver: {driver}")
