from .mkdir import handle as handle_mkdir
from .compare_files import handle as handle_compare_files
from .exists import handle as handle_exists

# Tous les handlers correspondent à ceux du YAML
PLUGIN_HANDLERS = {
    "exists": handle_exists,
    "compare_files": handle_compare_files,
}

# Exemple de signature de handler (dans copy_file.py) :
# def handle(groups, **kwargs):
#     src, dest = groups
#     # ou src = kwargs.get('src'), dest = kwargs.get('dest')
#     ... 