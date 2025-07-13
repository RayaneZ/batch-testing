from .mkdir import handle as handle_mkdir
from .compare_files import handle as handle_compare_files
from .exists import handle as handle_exists
from .file_contains import handle as handle_file_contains
from .file_empty import handle as handle_file_empty

# Tous les handlers correspondent à ceux du YAML
PLUGIN_HANDLERS = {
    "exists": handle_exists,
    "file_contains": handle_file_contains,
    "file_empty": handle_file_empty,
    "compare_files": handle_compare_files,
} 