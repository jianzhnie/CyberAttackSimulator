"""This code is an example for setting up the training of the various agents
using the algorithms present and using the current version of YAWNING TITAN."""

import glob
import os

import generate_test_networks as gtn
import numpy as np
# load the agents
from stable_baselines3 import A2C, DQN, PPO
# load the policies
from stable_baselines3.a2c import MlpPolicy as A2C_policy
from stable_baselines3.common.callbacks import (
    EvalCallback, StopTrainingOnNoModelImprovement)
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.dqn import MlpPolicy as DQN_policy
from stable_baselines3.ppo import MlpPolicy as PPO_policy
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.game_modes.game_mode_db import default_game_mode

from nasimulator.agents.action_loop import ActionLoop
from nasimulator.networks import network_creator
from nasimulator.networks.network_creator import get_network_from_dict


def main() -> None:
    # get the current directory
    current_dir = os.getcwd()
    # directories
    log_dir = os.path.join(current_dir, 'work_dir', 'new_logs_dir')
    network_dir = os.path.join(current_dir, 'work_dir', 'networks')

    # Specify algorithms, policies and saving directories
    algorithms = ['PPO', 'A2C', 'DQN']
    agents = [PPO, A2C, DQN]
    policies = [PPO_policy, A2C_policy, DQN_policy]
    dir_agent = [os.path.join(log_dir, imodel) for imodel in algorithms]
    # check with lower timesteps
    timesteps = 5e5
    # for this example we can show only the stand setup,
    model_names = [
        'PPO_std',
        'A2C_std',
        'DQN_std',
    ]
    # get the network network nodes
    # if you want to test the "unseen" networks use 22/55/60
    standard_example = [
        18,
        50,
        100,
    ]
    # entry nodes
    network_entry = [
        ['3', '5', '10'],  # 18
        ['3', '10', '15', '25', '34', '45', '7'],  # 50
        ['4', '10', '20', '30', '40', '55', '76', '78', '12', '88', '90'],
    ]  # 100
    game_mode = default_game_mode()
    # loop over the network size
    for index, isize in enumerate(standard_example):
        network_load = glob.glob(
            os.path.join(network_dir, f'synthetic_{isize}*.npz'))

        if len(network_load) == 1:
            network_files = np.load(network_load[0], allow_pickle=True)
            matrix = network_files['matrix']
            positions = dict(np.ndenumerate(network_files['connections']))[(
            )]  # convert the positions nd array to dict
        else:
            if isize == 18:
                matrix, positions = network_creator.get_18_node_network_mesh()
            else:
                matrix, positions = gtn.create_network(
                    n_nodes=isize,
                    connectivity=0.6,  # standard connectivity
                    output_dir=network_dir,
                    filename=f'synthetic_{isize}',
                    save_matrix=True,
                    save_graph=False,
                )

        # need to load the various networks
        network = get_network_from_dict(matrix, positions,
                                        network_entry[index])
        network.show(verbose=True)
        # Loop over the algorithms
        for idx, algorithm in enumerate(algorithms):
            agent = agents[idx]
            policy = policies[idx]
            model_dir = os.path.join(dir_agent[idx], algorithm)
            model_name = os.path.join(model_dir,
                                      model_names[idx] + f'_{isize}')
            meida_path = model_name
            print(f'Starting the agent using {algorithm} algorithm')
            # here enters the random seed! - I must use them in the testing phase.
            network_interface = NetworkInterface(game_mode=game_mode,
                                                 network=network)

            # generate the red and blue agents
            red = RedInterface(network_interface)
            blue = BlueInterface(network_interface)

            # generate the network environment
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
            if algorithm == 'DQN':  # adapt in case of buffer size
                chosen_agent = agent(policy, env, verbose=1, buffer_size=10000)
            else:
                chosen_agent = agent(policy,
                                     env,
                                     verbose=1,
                                     normalize_advantage=True)

            # Train the agent
            _ = chosen_agent.learn(total_timesteps=timesteps,
                                   callback=eval_callback)
            # save the trained-converged model
            chosen_agent.save(model_name)
            # visualize the trained-converged model
            loop = ActionLoop(env, chosen_agent, episode_count=3)
            loop.gif_action_loop(
                save_gif=True,
                render_network=True,
                save_webm=True,
                gif_output_directory=meida_path,
                webm_output_directory=meida_path,
            )


if __name__ == '__main__':
    main()
