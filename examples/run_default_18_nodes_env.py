import os
import sys

from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.ppo import MlpPolicy as PPOMlp
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.game_modes.game_mode_db import default_game_mode
from yawning_titan.networks.network_db import default_18_node_network

sys.path.append(os.getcwd())
import os

from stable_baselines3.common.callbacks import (
    EvalCallback, StopTrainingOnNoModelImprovement)
from stable_baselines3.common.monitor import Monitor

from nasimulator.envs.generic.core.action_loops import ActionLoop


def main():
    # get the current directory
    current_dir = os.getcwd()
    # directories
    log_dir = os.path.join(current_dir, 'work_dir', 'default_18_nodes')
    # setup the monitor to check the training
    algo_name = 'ppo'
    model_dir = os.path.join(log_dir, algo_name)
    model_name = os.path.join(model_dir, 'ppo_18')
    media_dir = os.path.join(log_dir, 'media')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    network = default_18_node_network()
    game_mode = default_game_mode()
    network_interface = NetworkInterface(game_mode=game_mode, network=network)
    red = RedInterface(network_interface)
    blue = BlueInterface(network_interface)
    env = GenericNetworkEnv(
        red,
        blue,
        network_interface,
        print_metrics=True,
        show_metrics_every=50,
        collect_additional_per_ts_data=True,
        print_per_ts_data=False,
    )
    # check the network
    check_env(env, warn=True)

    # reset the environment
    env.reset()

    timesteps = 1000
    env.reset()
    # setup the monitor to check the training
    env = Monitor(env, model_name)
    # define callback to stop the training
    stop_train_callback = StopTrainingOnNoModelImprovement(
        max_no_improvement_evals=3, min_evals=5, verbose=1)
    eval_callback = EvalCallback(
        env,
        callback_after_eval=stop_train_callback,
        n_eval_episodes=5,
        eval_freq=1000,  # eval_freq
        log_path=model_dir,  # save the logs
        best_model_save_path=model_dir,  # save the model
        deterministic=False,
        verbose=1,
    )
    # instantiate the agent - here we can set the various hyper parameters as the
    # Learning rate - tested to  learning_rate = 0.01 and the gamma = 0.75
    agent = PPO(PPOMlp, env, verbose=1, normalize_advantage=True)
    # Train the agent
    agent.learn(
        total_timesteps=timesteps,
        callback=eval_callback,
        log_interval=10,
    )
    # save the trained-converged model
    agent.save(model_name)
    # visualize the trained-converged model
    loop = ActionLoop(env, agent, episode_count=5)
    loop.gif_action_loop(
        save_gif=True,
        render_network=True,
        save_webm=True,
        gif_output_directory=media_dir,
        webm_output_directory=media_dir,
    )


if __name__ == '__main__':
    main()
