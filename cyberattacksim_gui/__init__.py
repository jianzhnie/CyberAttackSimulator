from pathlib import Path, PosixPath, WindowsPath
from typing import Final, Union

from cyberattacksim import _CAS_ROOT_DIR, LOG_DIR

_CAS_GUI_PLATFORM_DIRS: Final[Union[Path, WindowsPath,
                                    PosixPath]] = (_CAS_ROOT_DIR / 'cache' /
                                                   'gui')


def _static_dir() -> Union[Path, PosixPath]:
    dir_path = _CAS_GUI_PLATFORM_DIRS / 'static'
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _yt_run_temp_dir() -> Union[Path, PosixPath]:
    dir_path = _CAS_GUI_PLATFORM_DIRS / 'static' / 'yt_run'
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _yt_gui_run_log() -> Union[Path, PosixPath]:
    dir_path = LOG_DIR / 'yt_gui_run.log'
    # Create if it doesn't already exist and bypass if it does already exist
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


DEFAULT_GAME_MODE: Final[str] = 'everything_off_config.yaml'
"""The filename of the game mode file to act as the base for all game modes """

STATIC_DIR: Final[Union[Path, PosixPath]] = _static_dir()
"""The path to the app static directory as an instance of `Path` or `PosixPath`, depending on the OS."""

# YT_RUN_TEMP_DIR: Final[Union[Path, PosixPath]] = _yt_run_temp_dir()
# """The path to the app temp directory for :class: `~cyberattacksim.cyberattacksim_run.CyberAttackRun` as an instance of `Path` or `PosixPath`, depending on the OS."""

CAS_RUN_TEMP_DIR = _CAS_GUI_PLATFORM_DIRS / 'static' / 'gifs'

CAS_GUI_RUN_LOG = LOG_DIR / 'yt_gui_run.log'

CAS_GUI_STDOUT = LOG_DIR / 'stdout.txt'
