# sql_drivers.py

"""
Utilisation de SQL_CONN pour l'exécution de scripts SQL dans les tests batch
==========================================================================

Pour tous les SGBD, la variable d'environnement SQL_CONN doit être définie dans le .shtest
avant toute action SQL. Le format attendu dépend du SGBD sélectionné via SQL_DRIVER.

Exemples d'utilisation dans un .shtest :

--- Oracle ---
Action: Définir la variable SQL_DRIVER = oracle ;
Action: Définir la variable SQL_CONN = user/password@db ;
Action: Exécuter le script SQL mon_script.sql ;
# Commande générée :
#   sqlplus -s user/password@db @mon_script.sql

--- PostgreSQL ---
Action: Définir la variable SQL_DRIVER = postgres ;
Action: Définir la variable SQL_CONN = postgres://user:password@host:5432/dbname ;
Action: Exécuter le script SQL mon_script.sql ;
# Commande générée :
#   psql "postgres://user:password@host:5432/dbname" -f mon_script.sql

--- MySQL ---
Action: Définir la variable SQL_DRIVER = mysql ;
Action: Définir la variable SQL_CONN = mysql://user:password@host:3306/dbname ;
Action: Exécuter le script SQL mon_script.sql ;
# Commande générée :
#   mysql "mysql://user:password@host:3306/dbname" < mon_script.sql

--- Redis ---
Action: Définir la variable SQL_DRIVER = redis ;
Action: Définir la variable SQL_CONN = -h myhost -p 6380 -a mypass ;
Action: Exécuter le script SQL mon_script.redis ;
# Commande générée :
#   redis-cli -h myhost -p 6380 -a mypass < mon_script.redis

Note :
- Il n'est pas nécessaire de générer ou d'exporter SQL_DRIVER dans le shell, il sert uniquement à la génération du script.
- Adaptez la valeur de SQL_CONN selon le SGBD utilisé.
"""

# Dictionnaire associant chaque driver à sa commande SQL
# Tous les drivers utilisent la variable SQL_CONN
# Format attendu :
#   - Oracle : user/password@db
#   - Postgres : postgres://user:password@host:port/dbname
#   - MySQL : mysql://user:password@host:port/dbname (ou syntaxe CLI compatible)
#   - Redis : options à passer à redis-cli (ex: -h host -p port -a password)
#     Exemple .shtest :
#         Action: Définir la variable SQL_DRIVER = redis ;
#         Action: Définir la variable SQL_CONN = -h myhost -p 6380 -a mypass ;
#         Action: Exécuter le script SQL mon_script.redis ;
#     Commande générée :
#         redis-cli -h myhost -p 6380 -a mypass < mon_script.redis
SQL_DRIVERS = {
    "oracle": lambda script, conn: f"sqlplus -s {conn} @{script}",
    "postgres": lambda script, conn: f'psql "{conn}" -f {script}',
    "mysql": lambda script, conn: f'mysql "{conn}" < {script}',
    "redis": lambda script, conn: f"redis-cli {conn} < {script}",
}


def get_sql_command(script: str, conn: str, driver: str = None) -> str:
    """
    Retourne la commande shell à exécuter pour lancer un script SQL,
    en fonction du type de base de données (driver).
    Utilise toujours la variable SQL_CONN, dont le format dépend du SGBD.
    """
    driver = (driver or "oracle").lower()
    if driver in SQL_DRIVERS:
        return SQL_DRIVERS[driver](script, conn)
    raise ValueError(f"Unsupported SQL driver: {driver}")
