"""The `cyberattacksim` top-level __init__.

`gym.envs` registered:
    `five-node-def-v0`
        entry_point: `cyberattacksim.envs.specific:FiveNodeDef`
    `four-node-def-v0`
        entry_point: `cyberattacksim.envs.specific:FourNodeDef`
    `networks-graph-explore-v0`
        entry_point: `cyberattacksim.envs.specific:GraphExplore`
    `18-node-env-v0`
        entry_point: `cyberattacksim.envs.specific:NodeEnv`

App directories initialised:
    `LOG_DIR`:
        The path to the app log directory as an instance of `Path` or `PosixPath`, depending on the OS.

Logging configured from the root:
    Logging is configured using the `cyberattacksim.config._package_data.logging_config.yaml` config file.
"""

import logging.config
import os
from pathlib import Path, PosixPath, WindowsPath
from typing import Final, Union

import yaml
from gym.envs.registration import register

register(id='five-node-def-v0',
         entry_point='cyberattacksim.envs.specific:FiveNodeDef')

register(id='four-node-def-v0',
         entry_point='cyberattacksim.envs.specific:FourNodeDef')

register(
    id='networks-graph-explore-v0',
    entry_point='cyberattacksim.envs.specific:GraphExplore',
)

register(id='18-node-env-v0',
         entry_point='cyberattacksim.envs.specific:NodeEnv')

# Below handles application directories and user directories.
# Uses `platformdirs.PlatformDirs` and `pathlib.Path` to create the required
# app directories in the correct locations based on the users OS.

_CAS_ROOT_DIR: Final[Union[Path, WindowsPath,
                           PosixPath]] = Path(__file__).parent.resolve()


def _version() -> str:
    version_path = _CAS_ROOT_DIR / 'VERSION'
    with open(version_path, 'r') as file:
        return file.readline().strip()


__version__ = _version()

_CAS_USER_DIRS: Final[Union[Path, WindowsPath,
                            PosixPath]] = (Path.home() / 'cyberattacksim')
"""The users home space for YT which is located at: ~/cyberattacksim."""

LOG_DIR: Final[Union[Path, WindowsPath,
                     PosixPath]] = _CAS_USER_DIRS / 'log_dir'
"""The path to the app log directory as an instance of `Path` or `PosixPath`, depending on the OS."""

DB_DIR: Final[Union[Path, WindowsPath, PosixPath]] = _CAS_USER_DIRS / 'db'
"""The path to the app db directory as an instance of `Path` or `PosixPath`, depending on the OS."""

APP_IMAGES_DIR: Final[Union[Path, WindowsPath,
                            PosixPath]] = (_CAS_USER_DIRS / 'app_images')
"""The path to the app images directory as an instance of `Path` or `PosixPath`, depending on the OS."""

NOTEBOOKS_DIR: Final[Union[Path, WindowsPath,
                           PosixPath]] = _CAS_USER_DIRS / 'notebooks'
"""
The path to the users notebooks directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users notebooks are stored at: ~/cyberattacksim/notebooks.
"""

GAME_MODES_DIR: Final[Union[Path, WindowsPath,
                            PosixPath]] = (_CAS_USER_DIRS / 'game_modes')
"""
The path to the users game modes directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users game modes are stored at: ~/cyberattacksim/game_modes.
"""

IMAGES_DIR: Final[Union[Path, WindowsPath,
                        PosixPath]] = _CAS_USER_DIRS / 'images'
"""
The path to the users images directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users images are stored at: ~/cyberattacksim/images.
"""

VIDEOS_DIR: Final[Union[Path, WindowsPath,
                        PosixPath]] = _CAS_USER_DIRS / 'videos'
"""
The path to the users videos directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users videos are stored at: ~/cyberattacksim/videos.
"""

AGENTS_DIR: Final[Union[Path, WindowsPath,
                        PosixPath]] = _CAS_USER_DIRS / 'agents'
"""
The path to the users agents directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users agents are stored at: ~/cyberattacksim/agents.
"""

AGENTS_LOGS_DIR: Final[Union[Path, WindowsPath,
                             PosixPath]] = (_CAS_USER_DIRS / 'agents' / 'logs')
"""
The path to the users agents logs directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users agent logs are stored at: ~/cyberattacksim/agents/logs.
"""

PPO_TENSORBOARD_LOGS_DIR: Final[Union[Path, WindowsPath,
                                      PosixPath]] = (_CAS_USER_DIRS /
                                                     'agents' / 'logs' /
                                                     'tensorboard')
"""
The path to the PPO algorithm tensorboard logs directory as an instance of `Path` or `PosixPath`, depending on the OS.

Users agent PPO algorithm tensorboard logs are stored at: ~/cyberattacksim/agents/logs/ppo_tensorboard.
"""

# Setup root logger format
with open(_CAS_ROOT_DIR / 'config' / '_package_data' / 'logging_config.yaml',
          'r') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)

LOG_FILE_PATH: Final[str] = os.path.join(
    LOG_DIR, config['handlers']['info_rotating_file_handler']['filename'])
config['handlers']['info_rotating_file_handler']['filename'] = LOG_FILE_PATH

try:
    logging.config.dictConfig(config)
except Exception:  # noqa
    pass
