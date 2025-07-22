#!/usr/bin/env python3
"""
Docker Compose Configuration Validator
Validates the syntax and structure of Docker Compose files
"""

import yaml
import os
import sys

def validate_yaml_file(file_path):
    """Validate a YAML file and return any errors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            yaml.safe_load(file)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)
    except FileNotFoundError:
        return False, "File not found"
    except Exception as e:
        return False, str(e)

def validate_docker_compose_structure(file_path):
    """Validate Docker Compose specific structure"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        errors = []
        
        # Check for required top-level keys
        if 'services' not in config:
            errors.append("Missing required 'services' section")
        
        # Check services structure
        if 'services' in config:
            services = config['services']
            if not isinstance(services, dict):
                errors.append("'services' must be a dictionary")
            else:
                for service_name, service_config in services.items():
                    if not isinstance(service_config, dict):
                        errors.append(f"Service '{service_name}' must be a dictionary")
                    
                    # Check for either image or build
                    if 'image' not in service_config and 'build' not in service_config:
                        errors.append(f"Service '{service_name}' must have either 'image' or 'build' specified")
        
        return len(errors) == 0, errors
    
    except Exception as e:
        return False, [str(e)]

def main():
    """Main validation function"""
    config_files = [
        'docker-compose.yml',
        'docker-compose.official.yml',
        'docker-compose.fixed.yml'
    ]
    
    print("Docker Compose Configuration Validator")
    print("=" * 50)
    
    all_valid = True
    
    for config_file in config_files:
        print(f"\nValidating {config_file}...")
        
        if not os.path.exists(config_file):
            print(f"  ❌ File not found: {config_file}")
            all_valid = False
            continue
        
        # Validate YAML syntax
        yaml_valid, yaml_error = validate_yaml_file(config_file)
        if not yaml_valid:
            print(f"  ❌ YAML Syntax Error: {yaml_error}")
            all_valid = False
            continue
        else:
            print(f"  ✅ YAML syntax is valid")
        
        # Validate Docker Compose structure
        structure_valid, structure_errors = validate_docker_compose_structure(config_file)
        if not structure_valid:
            print(f"  ❌ Structure Errors:")
            for error in structure_errors:
                print(f"     - {error}")
            all_valid = False
        else:
            print(f"  ✅ Docker Compose structure is valid")
    
    print("\n" + "=" * 50)
    if all_valid:
        print("✅ All configuration files are valid!")
        return 0
    else:
        print("❌ Some configuration files have errors!")
        return 1

if __name__ == "__main__":
    sys.exit(main())

