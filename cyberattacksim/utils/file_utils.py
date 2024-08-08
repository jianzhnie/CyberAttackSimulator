import os
from typing import Any, Dict

import yaml


def make_dirs(path: str) -> None:
    """Ensure that a directory exists. If it does not exist, create it.

    Args:
        path (str): The directory path to check and create if not exists.

    Returns:
        None
    """
    if not os.path.exists(path):
        os.makedirs(path)


def load_yaml_config(file_path: str) -> Dict[str, Any]:
    """Load configuration from a YAML file.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        Dict[str, Any]: Configuration dictionary.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config


def update_dataclass_from_dict(instance: Any, config: Dict[str, Any]):
    """Update the attributes of a dataclass instance with values from a config
    dictionary.

    Args:
        instance (Any): The dataclass instance to update.
        config (Dict[str, Any]): The configuration dictionary.
    """
    for key, value in config.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
    return instance
