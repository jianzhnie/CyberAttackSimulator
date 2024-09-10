import argparse
import os
import sys

import tyro
import wandb

import torch_npu
from torch_npu.contrib import transfer_to_npu

from stable_baselines3 import A2C, DQN, PPO, HerReplayBuffer
from stable_baselines3.a2c import MlpPolicy as A2CMlp
from stable_baselines3.common.callbacks import (
    EvalCallback, StopTrainingOnNoModelImprovement)
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.dqn import MlpPolicy as DQNMlp
from stable_baselines3.ppo import MlpPolicy as PPOMlp
from wandb.integration.sb3 import WandbCallback

sys.path.append(os.getcwd())

from algorithms.MC.MCAgent import MC
from algorithms.MC.MCMlp import MCPolicy as MCMlp
from algorithms.BR.BRAgent import BR
from algorithms.BR.BRMlp import BRPolicy as BRMlp
from algorithms.policies.policy import ACRNNPolicy
from algorithms.policies.policy import ACCNNPolicy
from algorithms.policies.policy import ACSNNPolicy
from cyberattacksim.envs.generic.core.action_loops import ActionLoop
from cyberattacksim.utils.env_utils import create_env
from cyberattacksim.utils.file_utils import (load_yaml_config,
                                             update_dataclass_from_dict)
from cyberattacksim.utils.setup_app_dirs import setup_app_dirs
from examples.configs.rl_args import (A2CArguments, DQNArguments, 
                                        MCArguments, BRArguments, PPOArguments)

from algorithms.TD3.TD3Agent import TD3
from algorithms.TD3.TD3Mlp import TD3Policy as TD3Mlp

from algorithms.SAC.SACAgent import SAC
from algorithms.SAC.SACMlp import SACPolicy as SACMlp

from algorithms.DQfD.DQfDAgent import DQfD
from algorithms.DQfD.DQfDMlp import DQfDPolicy as DQfDMlp

from algorithms.CFR.CFRAgent import CFR
from algorithms.CFR.CFRMlp import CFRPolicy as CFRMlp
from examples.configs.rl_args import DQfDArguments, CFRArguments, SACArguments, TD3Arguments


def main() -> None:
    # Initialize ArgumentParser
    parser = argparse.ArgumentParser(description='Cyber Attack Sim')
    parser.add_argument(
        '--algo_name',
        type=str,
        choices=[
            'dqn',
            'a2c',
            'ppo',
            'mc',
            'br',
            'snnppo',
            'rnnppo',
            'cnnppo',
            'mlpppo',
            'sac',
            'td3',
            'dqfd',
            'cfr',
            'her'
        ],
        default='dqn',
        help="Name of the algorithm. Defaults to 'dqn'",
    )
    parser.add_argument(
        '--env_id',
        type=str,
        default='default_18_node_network',
        help="The environment name. Defaults to 'CartPole-v0'",
    )
    parser.add_argument(
        '--use_wandb',
        type=bool,
        default=False,
        help="Will use wandb or not",
    )
    setup_app_dirs()
    # directories
    curr_path = os.getcwd()
    # Load YAML configuration
    config_file = os.path.join(curr_path, 'examples/configs/config.yaml')
    config = load_yaml_config(config_file)
    # Parse arguments
    run_args = parser.parse_args()
    if run_args.algo_name == 'dqn':
        algo_args: DQNArguments = tyro.cli(DQNArguments)
    elif run_args.algo_name == 'a2c':
        algo_args: A2CArguments = tyro.cli(A2CArguments)
    elif run_args.algo_name == 'ppo':
        algo_args: PPOArguments = tyro.cli(PPOArguments)
    elif run_args.algo_name == 'mlpppo':
        algo_args: PPOArguments = tyro.cli(PPOArguments)
    elif run_args.algo_name == 'cnnppo':
        algo_args: PPOArguments = tyro.cli(PPOArguments)
    elif run_args.algo_name == 'snnppo':
        algo_args: PPOArguments = tyro.cli(PPOArguments)   
    elif run_args.algo_name == 'rnnppo':
        algo_args: PPOArguments = tyro.cli(PPOArguments)  
    elif run_args.algo_name == 'mc':
        algo_args: MCArguments = tyro.cli(MCArguments)
    elif run_args.algo_name == 'br':
        algo_args: BRArguments = tyro.cli(BRArguments)
    elif run_args.algo_name == 'sac':
        algo_args: SACArguments = tyro.cli(SACArguments)
    elif run_args.algo_name == 'td3':
        algo_args: TD3Arguments = tyro.cli(TD3Arguments)
    # elif run_args.algo_name == 'dqfd':
    #     algo_args: DQfDArguments = tyro.cli(DQfDArguments)
    elif run_args.algo_name == 'cfr':
        algo_args: CFRArguments = tyro.cli(CFRArguments)
    elif run_args.algo_name == 'her':
        algo_args: DQNArguments = tyro.cli(DQNArguments)
    else:
        raise NotImplementedError

    # Extract Algo-specific settings
    if run_args.algo_name in config:
        algo_config = config.get(run_args.algo_name)
        env_config = algo_config.get(run_args.env_id)
    else:
        env_config = {}
        print(
            'No configuration found for {}, {} in {}. Using default settings.'.
            format(run_args.algo_name, run_args.env_id, config_file))

    # Update parser with YAML configuration
    args: A2CArguments = update_dataclass_from_dict(algo_args, env_config)

    args: MCArguments = update_dataclass_from_dict(algo_args, env_config)
    args: BRArguments = update_dataclass_from_dict(algo_args, env_config)
    
    # set file path
    work_dir = os.path.join(args.work_dir, args.env_id)
    model_dir = os.path.join(work_dir, args.algo_name)
    tf_log_dir = os.path.join(model_dir, 'tf_logs')
    model_name = os.path.join(model_dir, args.algo_name + '_model')
    media_dir = os.path.join(work_dir, args.algo_name, 'media')
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    
    if run_args.use_wandb:
        run = wandb.init(dir=work_dir,
                        project=args.project,
                        name=args.env_id,
                        sync_tensorboard=True)
    env = create_env(env_id=args.env_id)
    # setup the monitor to check the training
    env = Monitor(env, model_name)
    # define callback to stop the trainingX
    stop_train_callback = StopTrainingOnNoModelImprovement(
        max_no_improvement_evals=5, min_evals=10, verbose=1)
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
    if run_args.use_wandb:
        wandb_callback = WandbCallback(
            model_save_path=model_dir,
            model_save_freq=1000,
            verbose=2,
        )
    if args.algo_name == 'dqn':
        agent = DQN(
            policy=DQNMlp,
            env=env,
            learning_rate=args.learning_rate,
            buffer_size=args.buffer_size,
            tau=args.soft_update_tau,
            learning_starts=args.warmup_learn_steps,
            batch_size=args.batch_size,
            train_freq=args.train_frequency,
            gradient_steps=args.gradient_steps,
            target_update_interval=args.target_update_frequency,
            tensorboard_log=tf_log_dir,
            verbose=1,
        )

    elif args.algo_name == 'a2c':
        agent = A2C(
            policy=A2CMlp,
            env=env,
            learning_rate=args.learning_rate,
            n_steps=args.rollout_steps,
            gamma=args.gamma,
            gae_lambda=args.gae_lambda,
            ent_coef=args.ent_coef,
            vf_coef=args.vf_coef,
            max_grad_norm=args.max_grad_norm,
            normalize_advantage=args.normalize_advantage,
            tensorboard_log=tf_log_dir,
            verbose=1,
        )
    elif args.algo_name == 'ppo':
        agent = PPO(
            policy=PPOMlp,
            env=env,
            learning_rate=args.learning_rate,
            n_steps=args.rollout_steps,
            batch_size=args.batch_size,
            n_epochs=args.n_epochs,
            gamma=args.gamma,
            gae_lambda=args.gae_lambda,
            clip_range=args.clip_range,
            normalize_advantage=args.normalize_advantage,
            ent_coef=args.ent_coef,
            vf_coef=args.vf_coef,
            max_grad_norm=args.max_grad_norm,
            tensorboard_log=tf_log_dir,
            verbose=1,
        )
    elif args.algo_name == 'mc':
        agent = MC(
            policy=MCMlp,
            env=env,
            exploration_rate=args.exploration_rate,
            learning_rate=args.learning_rate,
            n_steps=args.rollout_steps,
            gamma=args.gamma,
            gae_lambda=args.gae_lambda,
            ent_coef=args.ent_coef,
            vf_coef=args.vf_coef,
            max_grad_norm=args.max_grad_norm,
            normalize_advantage=args.normalize_advantage,
            tensorboard_log=tf_log_dir,
            verbose=1,
        )
    elif args.algo_name == 'br':
        agent = BR(
            policy=MCMlp,
            env=env,
            exploration_rate=args.exploration_rate,
            learning_rate=args.learning_rate,
            n_steps=args.rollout_steps,
            gamma=args.gamma,
            gae_lambda=args.gae_lambda,
            ent_coef=args.ent_coef,
            vf_coef=args.vf_coef,
            max_grad_norm=args.max_grad_norm,
            normalize_advantage=args.normalize_advantage,
            tensorboard_log=tf_log_dir,
            verbose=1,
        )
    elif args.algo_name == 'mlpppo':
        agent = PPO(
            policy=PPOMlp,
            env=env,
            learning_rate=args.learning_rate,
            n_steps=args.rollout_steps,
            batch_size=args.batch_size,
            n_epochs=args.n_epochs,
            gamma=args.gamma,
            gae_lambda=args.gae_lambda,
            clip_range=args.clip_range,
            normalize_advantage=args.normalize_advantage,
            ent_coef=args.ent_coef,
            vf_coef=args.vf_coef,
            max_grad_norm=args.max_grad_norm,
            tensorboard_log=tf_log_dir,
            verbose=1,
        )
    elif args.algo_name == 'cnnppo':
        agent = PPO(
            policy=ACCNNPolicy,
            env=env,
            learning_rate=args.learning_rate,
            n_steps=args.rollout_steps,
            batch_size=args.batch_size,
            n_epochs=args.n_epochs,
            gamma=args.gamma,
            gae_lambda=args.gae_lambda,
            clip_range=args.clip_range,
            normalize_advantage=args.normalize_advantage,
            ent_coef=args.ent_coef,
            vf_coef=args.vf_coef,
            max_grad_norm=args.max_grad_norm,
            tensorboard_log=tf_log_dir,
            verbose=1,
        )
    elif args.algo_name == 'snnppo':
        agent = PPO(
            policy=ACSNNPolicy,     # ActorCriticPolicy, ACSNNPolicy
            env=env,
            learning_rate=args.learning_rate,
            n_steps=args.rollout_steps,
            batch_size=args.batch_size,
            n_epochs=args.n_epochs,
            gamma=args.gamma,
            gae_lambda=args.gae_lambda,
            clip_range=args.clip_range,
            normalize_advantage=args.normalize_advantage,
            ent_coef=args.ent_coef,
            vf_coef=args.vf_coef,
            max_grad_norm=args.max_grad_norm,
            tensorboard_log=tf_log_dir,
            verbose=1,
            policy_kwargs={'net_arch': [64, 64]}
        )
    elif args.algo_name == 'rnnppo':
            agent = PPO(
                policy=ACRNNPolicy,     # ActorCriticPolicy, ACNNPolicy
                env=env,
                learning_rate=args.learning_rate,
                n_steps=args.rollout_steps,
                batch_size=args.batch_size,
                n_epochs=args.n_epochs,
                gamma=args.gamma,
                gae_lambda=args.gae_lambda,
                clip_range=args.clip_range,
                normalize_advantage=args.normalize_advantage,
                ent_coef=args.ent_coef,
                vf_coef=args.vf_coef,
                max_grad_norm=args.max_grad_norm,
                tensorboard_log=tf_log_dir,
                verbose=1,
                policy_kwargs={'net_arch': [64, 64]}
            )
    elif args.algo_name == 'sac':
        agent = SAC(
            policy=SACMlp,
            env=env,
            learning_rate=args.learning_rate,
            verbose=1,
        )
    elif args.algo_name == 'td3':
        agent = TD3(
            policy=TD3Mlp,
            env=env,
            verbose=1,
        )
    elif args.algo_name == 'dqfd':
        agent = DQfD(
            policy=DQfDMlp,
            env=env,
            learning_rate=args.learning_rate,
            buffer_size=args.buffer_size,
            tau=args.soft_update_tau,
            learning_starts=args.warmup_learn_steps,
            batch_size=args.batch_size,
            train_freq=args.train_frequency,
            gradient_steps=args.gradient_steps,
            target_update_interval=args.target_update_frequency,
            tensorboard_log=tf_log_dir,
            verbose=1,

        )
    elif args.algo_name == 'cfr':
        agent = CFR(
            policy=CFRMlp,
            env=env,
            learning_rate=args.learning_rate,
            n_steps=args.rollout_steps,
            gamma=args.gamma,
            gae_lambda=args.gae_lambda,
            ent_coef=args.ent_coef,
            vf_coef=args.vf_coef,
            max_grad_norm=args.max_grad_norm,
            normalize_advantage=args.normalize_advantage,
            tensorboard_log=tf_log_dir,
            verbose=1,
        )
    elif args.algo_name == 'her':
        agent = DQN(
            policy=DQNMlp,
            env=env,
            learning_rate=args.learning_rate,
            buffer_size=args.buffer_size,
            tau=args.soft_update_tau,
            batch_size=args.batch_size,
            replay_buffer_class=HerReplayBuffer,
            train_freq=args.train_frequency,
            gradient_steps=args.gradient_steps,
            target_update_interval=args.target_update_frequency,
            tensorboard_log=tf_log_dir,
            verbose=1,
        )

    # Train the agent
    print('args.max_timesteps:', args.max_timesteps)
    # import pdb; pdb.set_trace()
    if run_args.use_wandb:
        callbacks = [eval_callback, wandb_callback]
    else:
        callbacks = [eval_callback]
    agent.learn(
        total_timesteps=args.max_timesteps,
        callback=callbacks,
        log_interval=args.train_log_interval,
        progress_bar=True,
    )
    evaluate_policy(agent, env, n_eval_episodes=args.eval_episodes)
    # save the trained-converged model
    agent.save(model_name)
    if run_args.use_wandb:
        run.finish()
    # visualize the trained-converged model
    loop = ActionLoop(env, agent, episode_count=3)
    loop.gif_action_loop(
        save_gif=True,
        render_network=True,
        save_webm=True,
        gif_output_directory=media_dir,
        webm_output_directory=media_dir,
    )


if __name__ == '__main__':
    main()
