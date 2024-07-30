import os


def make_dirs(path: str) -> None:
    """Ensure that a directory exists. If it does not exist, create it.

    Args:
        path (str): The directory path to check and create if not exists.

    Returns:
        None
    """
    if not os.path.exists(path):
        os.makedirs(path)
