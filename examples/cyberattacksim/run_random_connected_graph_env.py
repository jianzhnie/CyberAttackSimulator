"""A custom config runner module.

This module is used simple as a playground/testbed for custom configurations of
CyberAttack.

.. warning::

    This module is being deprecated in a future release to make way for
    CyberAttack runner module in the main package.
"""

import os
import sys
import time

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import MlpPolicy as PPOMlp

sys.path.append(os.getcwd())
from cyberattacksim.agents.sinewave_red import SineWaveRedAgent
from cyberattacksim.envs.generic.core.action_loops import ActionLoop
from cyberattacksim.envs.generic.core.blue_interface import BlueInterface
from cyberattacksim.envs.generic.core.network_interface import NetworkInterface
from cyberattacksim.envs.generic.generic_env import GenericNetworkEnv
from cyberattacksim.game_modes.game_mode_db import default_game_mode
from cyberattacksim.networks import network_creator


def main():
    """Run the custom config."""
    game_mode = default_game_mode()

    network = network_creator.gnp_random_connected_graph(
        n_nodes=30, probability_of_edge=0.02)
    network.set_random_entry_nodes = True
    network.num_of_random_entry_nodes = 3
    network.reset_random_entry_nodes()
    network.set_random_high_value_nodes = True
    network.num_of_random_high_value_nodes = 3
    network.reset_random_high_value_nodes()
    network.set_random_vulnerabilities = True
    network.reset_random_vulnerabilities()

    network_interface = NetworkInterface(game_mode=game_mode, network=network)

    red = SineWaveRedAgent(network_interface)
    blue = BlueInterface(network_interface)

    env = GenericNetworkEnv(
        red,
        blue,
        network_interface,
        print_metrics=True,
        show_metrics_every=10,
        collect_additional_per_ts_data=True,
        print_per_ts_data=False,
    )

    # get the current directory
    current_dir = os.getcwd()
    # directories
    log_dir = os.path.join(current_dir, 'work_dir', 'random_connected_graph')
    tensorboard_log_dir = os.path.join(log_dir, 'tf_logs/')
    filename = f'random_connected_graph_{round(time.time())}'
    media_dir = os.path.join(log_dir, 'media')
    model_name = os.path.join(log_dir, filename)

    check_env(env, warn=True)
    # setup the monitor to check the training
    env = Monitor(env, model_name)
    env.reset()

    agent = PPO(PPOMlp, env, verbose=1, tensorboard_log=tensorboard_log_dir)

    eval_callback = EvalCallback(Monitor(env),
                                 eval_freq=100,
                                 deterministic=False,
                                 render=True)

    agent.learn(total_timesteps=100000, callback=eval_callback)

    loop = ActionLoop(env, agent, filename, episode_count=10)
    loop.gif_action_loop(
        render_network=True,
        save_gif=True,
        save_webm=True,
        gif_output_directory=media_dir,
        webm_output_directory=media_dir,
    )


if __name__ == '__main__':
    main()
