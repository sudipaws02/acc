import yaml
import os


def load_yaml_file(filepath: str) -> dict:
    """Load a YAML file and return its contents as a dictionary."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Config file not found: {filepath}")
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)


def load_configs(config_dir: str = "config") -> dict:
    """
    Load and return all configuration files used in the tool.

    Returns:
        dict: {
            'column_map': {...},
            'ea_filters': {...}
        }
    """
    column_map = load_yaml_file(os.path.join(config_dir, "column_map.yaml"))
    ea_filters = load_yaml_file(os.path.join(config_dir, "ea-filters.yaml"))

    return {
        "column_map": column_map,
        "ea_filters": ea_filters
    }