from .purge_dir import handle as handle_purge_dir
from .move_dir import handle as handle_move_dir
from .mkdir import handle as handle_mkdir
from .delete_dir import handle as handle_delete_dir
from .copy_dir import handle as handle_copy_dir

# Tous les handlers correspondent à ceux du YAML
dir_PLUGIN_HANDLERS = {
    "create_dir": handle_mkdir,
    "delete_dir": handle_delete_dir,
    "copy_dir": handle_copy_dir,
    "move_dir": handle_move_dir,
    "purge_dir": handle_purge_dir,
}

# Exemple de signature de handler (dans copy_dir.py) :
# def handle(groups, **kwargs):
#     src, dest = groups
#     # ou src = kwargs.get('src'), dest = kwargs.get('dest')
#     ... 