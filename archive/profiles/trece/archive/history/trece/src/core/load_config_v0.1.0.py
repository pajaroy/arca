# ---
# type: "script"
# fecha: "2025-08-20"
# version: "0.1.0"
# descripcion: "Modulo para cargar configuracion desde un archivo YAML"
# ---
"""
Module to load and expose the application configuration from YAML file.
"""
from pathlib import Path
import yaml
from typing import Dict, Any

# Get project root by going up 3 levels from this file's location
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"

def load_config() -> Dict[str, Any]:
    """
    Load the YAML configuration file and return its contents as a dictionary.
    
    Returns:
        dict: The loaded configuration
        
    Raises:
        FileNotFoundError: If the config file doesn't exist
        yaml.YAMLError: If there's an error parsing the YAML
    """
    with open(CONFIG_PATH, 'r', encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)
    
    # Generate db_connection path from the config
    if 'paths' in config and 'database' in config['paths']:
        db_path = PROJECT_ROOT / config['paths']['database']
        config['settings']['db_connection'] = f"sqlite:///{db_path.absolute()}"
    
    return config

# Export the configuration
config = load_config()