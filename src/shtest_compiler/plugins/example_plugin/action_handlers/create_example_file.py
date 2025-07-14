import os

# Action handlers implement actions triggered by patterns in patterns_actions.yml.
# The function name should match the 'handler' field in the YAML.
# The function receives a context and params dict, and should return a result dict.

def create_example_file(context, params):
    """
    Action handler: Creates an example file in the target directory.
    """
    target_dir = params.get('target_dir', '.')
    file_path = os.path.join(target_dir, 'example.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('This is an example file created by the plugin.')
    return {'status': 'success', 'file': file_path} 