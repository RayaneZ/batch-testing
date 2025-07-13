from .run import handle as handle_run
from .run_with_args import handle as handle_run_with_args

# Tous les handlers correspondent à ceux du YAML
PLUGIN_HANDLERS = {
    "run_script": handle_run,
    "run_with_args": handle_run_with_args,
}

# Exemple de signature de handler (dans run.py) :
# def handle(groups, **kwargs):
#     script, = groups
#     # ou script = kwargs.get('script')
#     ... 