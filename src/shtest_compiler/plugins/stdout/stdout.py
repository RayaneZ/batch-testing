from .contains import handle as handle_contains

# Tous les handlers correspondent à ceux du YAML
PLUGIN_HANDLERS = {
    "stdout_contains": handle_contains,
}

# Exemple de signature de handler (dans contains.py) :
# def handle(groups, **kwargs):
#     substring, = groups
#     # ou substring = kwargs.get('text')
#     ...
