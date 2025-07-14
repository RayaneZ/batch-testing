import os

# Validation handlers implement checks triggered by patterns in patterns_validations.yml.
# The function name should match the 'handler' field in the YAML.
# The function receives a context and params dict, and should return a result dict.

def example_file_exists(context, params):
    """
    Validation handler: Checks if the example file exists in the target directory.
    """
    target_dir = params.get('target_dir', '.')
    file_path = os.path.join(target_dir, 'example.txt')
    exists = os.path.isfile(file_path)
    return {'exists': exists, 'file': file_path} 