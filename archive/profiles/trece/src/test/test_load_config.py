"""
Test module for load_config.py
"""
import pytest
from pathlib import Path
from trece.src.core.load_config import load_config, CONFIG_PATH

def test_config_file_exists():
    """Test that the config file exists."""
    assert CONFIG_PATH.exists(), f"Config file not found at {CONFIG_PATH}"

def test_load_config_structure():
    """Test that the loaded config has the expected structure."""
    config = load_config()
    
    # Test top-level sections
    assert 'paths' in config
    assert 'settings' in config
    
    # Test paths structure
    paths = config['paths']
    assert isinstance(paths['database'], str)
    assert 'archive' in paths
    assert 'meta' in paths
    
    # Test settings
    settings = config['settings']
    assert 'default_template' in settings
    assert 'db_connection' in settings
    assert str(Path(paths['database'])) in settings['db_connection']

def test_paths_resolve_correctly():
    """Test that paths are properly resolved relative to project root."""
    config = load_config()
    project_root = Path(__file__).parent.parent.parent.parent
    
    # Verify database path
    db_path = project_root / config['paths']['database']
    assert db_path.parent.exists(), f"Database directory doesn't exist: {db_path.parent}"
    
    # Verify template path
    templates_path = project_root / config['paths']['templates']
    assert templates_path.exists(), f"Templates directory doesn't exist: {templates_path}"