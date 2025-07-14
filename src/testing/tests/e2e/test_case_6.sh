echo "[ERROR] ImportError: Handler 'dir_ready' (is_action=False) not found in core or plugins.
To implement this handler, create a Python file named 'dir_ready.py' 
in the appropriate directory: 
'shtest_compiler/core/handlers' for core, 
or 'shtest_compiler/plugins/<your_plugin>/handlers' for plugins. 
The handler should define a 'handle(params)' function.
Pattern entry for reference: {'phrase': 'Le dossier est prêt', 'handler': 'dir_ready', 'scope': 'last_action', 'opposite': {'phrase': 'Le dossier est absent'}, 'aliases': ['le dossier est prêt', 'dossier prêt', 'le dossier est cree', 'dossier cree', 'le dossier est créé', 'dossier créé', 'le dossier est cree', 'dossier cree', 'le dossier est créé', 'dossier créé', 'le dossier est present', 'dossier present', 'le dossier est vide', 'dossier vide', '^le dossier est prêt$', '^dossier prêt$', '^le dossier est cree$', '^dossier cree$', '^le dossier est créé$', '^dossier créé$', '^le dossier est present$', '^dossier present$', '^le dossier est vide$', '^dossier vide$']}"
exit 1