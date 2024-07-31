import os
import sys

from stable_baselines3 import A2C, DQN, PPO
from stable_baselines3.a2c import MlpPolicy as A2C_policy
from stable_baselines3.common.callbacks import (
    EvalCallback, StopTrainingOnNoModelImprovement)
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.dqn import MlpPolicy as DQN_policy
from stable_baselines3.ppo import MlpPolicy as PPO_policy

from cyberattacksim.envs.generic.core.blue_interface import BlueInterface
from cyberattacksim.envs.generic.core.network_interface import NetworkInterface
from cyberattacksim.envs.generic.core.red_interface import RedInterface
from cyberattacksim.envs.generic.generic_env import GenericNetworkEnv
from cyberattacksim.game_modes.game_mode_db import default_game_mode
from cyberattacksim.networks.network_db import default_18_node_network

sys.path.append(os.getcwd())
from cyberattacksim.envs.generic.core.action_loops import ActionLoop


def main():
    # get the current directory
    current_dir = os.getcwd()
    # directories
    log_dir = os.path.join(current_dir, 'work_dir', 'default_18_nodes')
    # setup the monitor to check the training
    # Specify algorithms, policies and saving directories
    algorithms = ['PPO', 'A2C', 'DQN']
    agents = [PPO, A2C, DQN]
    policies = [PPO_policy, A2C_policy, DQN_policy]
    # for this example we can show only the stand setup,
    model_names = [
        'PPO_std',
        'A2C_std',
        'DQN_std',
    ]
    # check with lower timesteps
    timesteps = 1000000
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    network = default_18_node_network()
    # check the network
    network.show(verbose=True)
    game_mode = default_game_mode()
    # Loop over the algorithms
    for idx, algorithm in enumerate(algorithms):
        agent = agents[idx]
        policy = policies[idx]
        model_dir = os.path.join(log_dir, algorithm)
        tf_log_dir = os.path.join(model_dir, 'tf_logs')
        model_name = os.path.join(model_dir, model_names[idx])
        media_dir = os.path.join(log_dir, algorithm, 'media')

        print(f'Starting the agent using {algorithm} algorithm')
        # init the network
        network_interface = NetworkInterface(game_mode=game_mode,
                                             network=network)
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
        # check the env
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
        print(eval_callback)
        # instantiate the agent - here we can set the various hyper parameters as the
        # Learning rate - tested to  learning_rate = 0.01 and the gamma = 0.75
        if algorithm == 'DQN':  # adapt in case of buffer size
            chosen_agent = DQN(
                policy,
                env,
                verbose=1,
                buffer_size=100000,
                target_update_interval=1000,
                tensorboard_log=tf_log_dir,
            )
        else:
            chosen_agent = agent(
                policy,
                env,
                verbose=1,
                normalize_advantage=True,
                tensorboard_log=tf_log_dir,
            )

        # Train the agent
        _ = chosen_agent.learn(
            total_timesteps=timesteps,
            log_interval=10,
            eval_freq=100,
            progress_bar=True,
        )
        # save the trained-converged model
        chosen_agent.save(model_name)
        # visualize the trained-converged model
        loop = ActionLoop(env, chosen_agent, episode_count=3)
        loop.gif_action_loop(
            save_gif=True,
            render_network=True,
            save_webm=True,
            gif_output_directory=media_dir,
            webm_output_directory=media_dir,
        )


if __name__ == '__main__':
    main()
