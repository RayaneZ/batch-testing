from .mkdir import handle as handle_mkdir
from .touch_ts import handle as handle_touch_ts
from .touch import handle as handle_touch
from .move_file import handle as handle_move_file
from .delete_file import handle as handle_delete_file
from .copy_file import handle as handle_copy_file
from .compare_files import handle as handle_compare_files
from .cat_file import handle as handle_cat_file
from .exists import handle as handle_exists
from .file_contains import handle as handle_file_contains
from .file_empty import handle as handle_file_empty

# Tous les handlers correspondent à ceux du YAML
PLUGIN_HANDLERS = {
    "create_file": handle_touch,  # création simple
    "update_file": handle_touch,  # mise à jour (même logique que création simple)
    "delete_file": handle_delete_file,
    "copy_file": handle_copy_file,
    "move_file": handle_move_file,
    "cat_file": handle_cat_file,
    "exists": handle_exists,
    "file_contains": handle_file_contains,
    "file_empty": handle_file_empty,
    "touch_ts": handle_touch_ts,
    "compare_files": handle_compare_files,
} 