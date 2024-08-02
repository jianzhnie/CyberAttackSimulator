import os
import sys

import wandb
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import (
    EvalCallback, StopTrainingOnNoModelImprovement)
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import MlpPolicy as PPOMlp
from wandb.integration.sb3 import WandbCallback

sys.path.append(os.getcwd())
from cyberattacksim.envs.generic.core.action_loops import ActionLoop
from cyberattacksim.envs.generic.core.blue_interface import BlueInterface
from cyberattacksim.envs.generic.core.network_interface import NetworkInterface
from cyberattacksim.envs.generic.core.red_interface import RedInterface
from cyberattacksim.envs.generic.generic_env import GenericNetworkEnv
from cyberattacksim.game_modes.game_mode_db import default_game_mode
from cyberattacksim.networks.network_db import default_18_node_network


def main() -> None:
    # get the current directory
    current_dir = os.getcwd()
    # setup the monitor to check the training
    algo_name = 'ppo'
    # directories
    log_dir = os.path.join(current_dir, 'work_dir', 'default_18_nodes')
    model_dir = os.path.join(log_dir, algo_name)
    tf_log_dir = os.path.join(model_dir, 'tf_logs')
    model_name = os.path.join(model_dir, algo_name + '_model')
    media_dir = os.path.join(log_dir, algo_name, 'media')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    run = wandb.init(
        dir=log_dir,
        project='CyberAttackSimulator',
        name='default_18_nodes',
        sync_tensorboard=True,
        tags=['CyberAttackSimulator'],
    )
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
    # reset the environment
    env.reset()

    timesteps = 1000000
    env.reset()
    # setup the monitor to check the training
    env = Monitor(env, model_name)
    # define callback to stop the training
    stop_train_callback = StopTrainingOnNoModelImprovement(
        max_no_improvement_evals=5, min_evals=10, verbose=1)
    print(stop_train_callback)
    eval_callback = EvalCallback(
        env,
        n_eval_episodes=10,
        eval_freq=1000,  # eval_freq
        log_path=model_dir,  # save the logs
        best_model_save_path=model_dir,  # save the model
        deterministic=True,
        render=False,
        verbose=1,
    )
    wandb_callback = WandbCallback(
        model_save_path=f'model_dir/{run.id}',
        model_save_freq=1000,
        verbose=2,
    )

    # instantiate the agent - here we can set the various hyper parameters as the
    # Learning rate - tested to  learning_rate = 0.01 and the gamma = 0.75
    agent = PPO(
        PPOMlp,
        env,
        verbose=1,
        normalize_advantage=True,
        tensorboard_log=tf_log_dir,
    )
    # Train the agent
    agent.learn(
        total_timesteps=timesteps,
        callback=[eval_callback, wandb_callback],
        log_interval=10,
        eval_freq=100,
        progress_bar=True,
    )
    evaluate_policy(agent, env, n_eval_episodes=10)
    # save the trained-converged model
    agent.save(model_name)
    run.finish()
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
