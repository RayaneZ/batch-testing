#!/usr/bin/env python3
"""
Test script to verify YAML file loading from executable directory.
This script can be run to test if the YAML files are being found and loaded correctly.
"""

import os
import sys
import yaml

def test_yaml_loading():
    """Test YAML file loading from the executable directory."""
    
    print("=== YAML Loading Test ===")
    
    # Get the base path (same logic as resource_path)
    if getattr(sys, 'frozen', False):  # Running as compiled exe
        base_path = os.path.dirname(sys.executable)
        print(f"Running as compiled exe, base_path: {base_path}")
    else:
        base_path = os.path.dirname(os.path.dirname(__file__))
        print(f"Running in development, base_path: {base_path}")
    
    # List all files in the base directory
    print(f"\nContents of {base_path}:")
    try:
        for item in os.listdir(base_path):
            print(f"  - {item}")
    except Exception as e:
        print(f"Error listing directory: {e}")
    
    # Test loading specific YAML files
    yaml_files = [
        "config/patterns_actions.yml",
        "config/patterns_validations.yml", 
        "config/handler_requirements.yml",
        "regex_config.yml"
    ]
    
    print(f"\n=== Testing YAML File Loading ===")
    for yaml_file in yaml_files:
        full_path = os.path.join(base_path, yaml_file)
        print(f"\nTesting: {yaml_file}")
        print(f"Full path: {full_path}")
        
        if os.path.exists(full_path):
            print(f"✓ File exists")
            try:
                with open(full_path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    print(f"✓ Successfully loaded YAML")
                    if isinstance(data, dict):
                        print(f"  Keys: {list(data.keys())}")
                    elif isinstance(data, list):
                        print(f"  List length: {len(data)}")
                    else:
                        print(f"  Data type: {type(data)}")
            except Exception as e:
                print(f"✗ Error loading YAML: {e}")
        else:
            print(f"✗ File not found")
    
    # Test plugin discovery
    print(f"\n=== Testing Plugin Discovery ===")
    plugins_dir = os.path.join(base_path, "plugins")
    if os.path.exists(plugins_dir):
        print(f"Plugins directory exists: {plugins_dir}")
        try:
            plugins = [d for d in os.listdir(plugins_dir) 
                      if os.path.isdir(os.path.join(plugins_dir, d)) 
                      and not d.startswith('.')]
            print(f"Found plugins: {plugins}")
            
            for plugin in plugins:
                plugin_dir = os.path.join(plugins_dir, plugin)
                config_dir = os.path.join(plugin_dir, "config")
                if os.path.exists(config_dir):
                    print(f"  Plugin {plugin} has config directory")
                    config_files = os.listdir(config_dir)
                    print(f"    Config files: {config_files}")
                else:
                    print(f"  Plugin {plugin} has no config directory")
        except Exception as e:
            print(f"Error listing plugins: {e}")
    else:
        print(f"Plugins directory not found: {plugins_dir}")

if __name__ == "__main__":
    test_yaml_loading() 