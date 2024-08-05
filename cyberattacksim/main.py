"""Provides a CLI using Typer as an entry point."""

import os
import sys

import typer

app = typer.Typer()


@app.command()
def gui():
    """Start the CyberAttackSim GUI."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'cyberattacksim_server.settings.dev')
    """Method that is fired on execution of the command in the terminal."""
    from cyberattacksim_gui.management.commands.run_gui import Command

    command = Command()
    command.run()


@app.command()
def build_dirs():
    """Build the CyberAttackSim app directories."""
    from cyberattacksim.utils import setup_app_dirs

    setup_app_dirs.run()


@app.command()
def reset_db(rebuild: bool = False):
    """Force a reset of the default entries in the NetworkDB and GameModeDB.

    :param rebuild: If True, completely rebuild the DB, removing all custom
        Networks and GameModes. Default value is False.
    """
    from cyberattacksim.utils import reset_network_and_game_mode_db_defaults

    reset_network_and_game_mode_db_defaults.run(rebuild)


@app.command()
def logs(last_n: int = 10):
    """Print the CyberAttackSim log file.

    :param last_n: The number of lines to print. Default value is 10.
    """
    import re

    from platformdirs import PlatformDirs

    cas_platform_dirs = PlatformDirs(appname='cyberattacksim')

    if sys.platform == 'win32':
        log_dir = cas_platform_dirs.user_data_path / 'logs'
    else:
        log_dir = cas_platform_dirs.user_log_path
    log_path = os.path.join(log_dir, 'cyberattacksim.log')

    if os.path.isfile(log_path):
        with open(log_path) as file:
            lines = file.readlines()
        for line in lines[-last_n:]:
            print(re.sub(r'\n*', '', line))


@app.command()
def docs():
    """View the CyberAttackSim docs."""
    import webbrowser

    webbrowser.open('https://jianzhnie.github.io/CyberAttackSim/', new=2)


@app.command()
def version():
    """Get the installed CyberAttackSim version number."""
    import cyberattacksim

    print(cyberattacksim.__version__)


@app.command()
def release_notes():
    """View the GitHub release notes of the installed CyberAttackSim
    version."""
    import webbrowser

    import cyberattacksim

    v = cyberattacksim.__version__
    url = f'https://github.com/jianzhnie/CyberAttackSim/releases/tag/v{v}'

    webbrowser.open(url, new=2)


@app.command()
def setup():
    """Perform the CyberAttackSim first-time setup.

    WARNING: All user-data will be lost.
    """
    from logging import getLogger

    import cyberattacksim  # noqa - Gets the CyberAttackSim logger config
    from cyberattacksim.utils import (reset_network_and_game_mode_db_defaults,
                                      setup_app_dirs)

    _LOGGER = getLogger(__name__)

    _LOGGER.info('Performing the CyberAttackSim first-time setup...')

    _LOGGER.info('Building the CyberAttackSim app directories...')
    setup_app_dirs.run()

    _LOGGER.info('Rebuilding the NetworkDB and GameModeDB...')
    reset_network_and_game_mode_db_defaults.run(rebuild=True)

    _LOGGER.info('CyberAttackSim setup complete!')


@app.command()
def keyboard_agent():
    """Play CyberAttackSim using the Keyboard Agent."""
    from stable_baselines3.common.env_checker import check_env

    from cyberattacksim.agents.keyboard import KeyboardAgent
    from cyberattacksim.envs.generic.core.blue_interface import BlueInterface
    from cyberattacksim.envs.generic.core.network_interface import \
        NetworkInterface
    from cyberattacksim.envs.generic.core.red_interface import RedInterface
    from cyberattacksim.envs.generic.generic_env import GenericNetworkEnv
    from cyberattacksim.game_modes.game_mode_db import default_game_mode
    from cyberattacksim.networks.network_db import default_18_node_network

    network = default_18_node_network()
    game_mode = default_game_mode()

    network_interface = NetworkInterface(game_mode=game_mode, network=network)

    red = RedInterface(network_interface)
    blue = BlueInterface(network_interface)

    env = GenericNetworkEnv(red, blue, network_interface)
    check_env(env, warn=True)
    _ = env.reset()

    kb = KeyboardAgent(env)
    kb.play(render_graphically=False)


if __name__ == '__main__':
    app()
