from .sql_script import handle as handle_sql_script
from .sql_query import handle as handle_sql_query
from .sql_export import handle as handle_sql_export
from .sql_compare import handle as handle_sql_compare

# Tous les handlers correspondent à ceux du YAML
PLUGIN_HANDLERS = {
    "sql_script": handle_sql_script,
    "sql_query": handle_sql_query,
    "sql_export": handle_sql_export,
    "sql_compare": handle_sql_compare,
}

# Exemple de signature de handler (dans sql_script.py) :
# def handle(groups, **kwargs):
#     script, = groups
#     # ou script = kwargs.get('script')
#     ... 