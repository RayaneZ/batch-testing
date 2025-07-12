from .sql_script import handle as handle_sql_script

# Tous les handlers correspondent à ceux du YAML
PLUGIN_HANDLERS = {
    "run_sql_script": handle_sql_script,
}

# Exemple de signature de handler (dans sql_script.py) :
# def handle(groups, **kwargs):
#     script, = groups
#     # ou script = kwargs.get('script')
#     ... 