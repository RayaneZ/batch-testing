from .mkdir import handle as handle_mkdir
from .touch_ts import handle as handle_touch_ts
from .touch import handle as handle_touch
from .move_file import handle as handle_move_file
from .delete_file import handle as handle_delete_file
from .copy_file import handle as handle_copy_file
from .compare_files import handle as handle_compare_files
from .cat_file import handle as handle_cat_file
from .exists import handle as handle_exists

# Tous les handlers correspondent à ceux du YAML
PLUGIN_HANDLERS = {
    "create_file": handle_touch,  # création simple
    "update_file": handle_touch,  # mise à jour (même logique que création simple)
    "delete_file": handle_delete_file,
    "copy_file": handle_copy_file,
    "move_file": handle_move_file,
    "cat_file": handle_cat_file,
    "exists": handle_exists,
    "touch_ts": handle_touch_ts,
    "compare_files": handle_compare_files,
}

# Exemple de signature de handler (dans copy_file.py) :
# def handle(groups, **kwargs):
#     src, dest = groups
#     # ou src = kwargs.get('src'), dest = kwargs.get('dest')
#     ... 