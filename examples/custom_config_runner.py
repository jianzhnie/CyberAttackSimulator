"""A custom config runner module.

This module is used simple as a playground/testbed for custom configurations of
Yawning-Titan.

.. warning::

    This module is being deprecated in a future release to make way for
    Yawning-Titan runner module in the main package.
"""

import os
import sys
import time

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import MlpPolicy as PPOMlp

from cyberattacksim.agents.sinewave_red import SineWaveRedAgent
from cyberattacksim.envs.generic.core.blue_interface import BlueInterface
from cyberattacksim.envs.generic.core.network_interface import NetworkInterface
from cyberattacksim.envs.generic.generic_env import GenericNetworkEnv
from cyberattacksim.game_modes.game_mode_db import default_game_mode
from cyberattacksim.networks import network_creator

sys.path.append(os.getcwd())
from cyberattacksim.envs.generic.core.action_loops import ActionLoop


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

    check_env(env, warn=True)

    env.reset()

    ENABLE_PROFILER = False
    CREATE_TENSORBOARD = True
    RENDER_FINAL_AGENT = True
    DURING_TRAIN_EVAL = True
    out_dir = '/home/robin/work_dir/rlcode/cyber/YAWNING-TITAN/examples/gnp_graph'
    tensorboard_log_dir = os.path.join(out_dir, 'logs/ppo-tensorboard/')
    if CREATE_TENSORBOARD:
        agent = PPO(PPOMlp,
                    env,
                    verbose=1,
                    tensorboard_log=tensorboard_log_dir)
    else:
        agent = PPO(PPOMlp, env, verbose=1)

    eval_callback = EvalCallback(Monitor(env),
                                 eval_freq=1000,
                                 deterministic=False,
                                 render=True)

    if ENABLE_PROFILER:
        import cProfile
        import pstats

        profiler = cProfile.Profile()

        profiler.enable()
        if DURING_TRAIN_EVAL:
            agent.learn(total_timesteps=5000,
                        n_eval_episodes=1,
                        callback=eval_callback)
        else:
            agent.learn(total_timesteps=5000)

        profiler.disable()

        stats = pstats.Stats(profiler)

        stats.sort_stats('tottime')

        stats.print_stats()
    else:
        if DURING_TRAIN_EVAL:
            agent.learn(total_timesteps=5000,
                        n_eval_episodes=1,
                        callback=eval_callback)
        else:
            agent.learn(total_timesteps=5000)

    if RENDER_FINAL_AGENT:
        filename = f'ppo_18-node-env-v0_{round(time.time())}'

        loop = ActionLoop(env, agent, filename, episode_count=100)
        out_dir = os.path.join(out_dir, 'images')
        loop.gif_action_loop(
            save_gif=True,
            render_network=True,
            save_webm=True,
            gif_output_directory=out_dir,
            webm_output_directory=out_dir,
        )


if __name__ == '__main__':
    main()
