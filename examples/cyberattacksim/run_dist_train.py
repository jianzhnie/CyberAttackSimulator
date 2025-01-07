import argparse
import os
import sys
from typing import Tuple, Union

import gymnasium as gym
import tyro
from accelerate import Accelerator

sys.path.append(os.getcwd())
sys.path.append('/home/robin/work_dir/ScaleRL')
from scalerl.algorithms.dqn.dqn_agent import DQNAgent
from scalerl.trainer.off_policy import OffPolicyTrainer
from scalerl.utils import get_device

from cyberattacksim.utils.env_utils import create_env
from cyberattacksim.utils.file_utils import (load_yaml_config,
                                             update_dataclass_from_dict)
from examples.configs.rl_args import (A2CArguments, DistDQNArguments,
                                      DQNArguments, PPOArguments)


def make_vect_envs(env_name: str,
                   num_envs: int = 1) -> gym.vector.AsyncVectorEnv:
    """Creates multiple vectorized environments that run asynchronously.

    Args:
        env_name: Name of the gymnasium environment to create
        num_envs: Number of environments to run in parallel

    Returns:
        AsyncVectorEnv: Vectorized environment instance
    """
    return gym.vector.AsyncVectorEnv(
        [lambda: create_env(env_id=env_name) for _ in range(num_envs)])


def get_algo_args(
    algo_name: str,
) -> Union[DQNArguments, A2CArguments, PPOArguments, DistDQNArguments]:
    """Get algorithm-specific arguments based on algorithm name.

    Args:
        algo_name: Name of the RL algorithm

    Returns:
        Algorithm-specific arguments dataclass

    Raises:
        NotImplementedError: If algorithm is not supported
    """
    algo_map = {
        'dqn': DQNArguments,
        'a2c': A2CArguments,
        'ppo': PPOArguments,
        'dist_dqn': DistDQNArguments,
    }

    if algo_name not in algo_map:
        raise NotImplementedError(f'Algorithm {algo_name} not supported')

    return tyro.cli(algo_map[algo_name])


def get_env_shapes(
        env: gym.vector.VectorEnv) -> Tuple[Tuple, Union[int, Tuple]]:
    """Extract state and action shapes from environment.

    Args:
        env: Vectorized gym environment

    Returns:
        Tuple containing state shape and action shape
    """
    state_shape = env.single_observation_space.shape or env.single_observation_space.n
    action_shape = env.single_action_space.shape or env.single_action_space.n
    return state_shape, action_shape


def main() -> None:
    """Main training function."""
    # Initialize parser with algorithm choices
    parser = argparse.ArgumentParser(
        description='Cyber Attack Simulator Training')
    parser.add_argument(
        '--algo_name',
        type=str,
        choices=['dqn', 'a2c', 'ppo', 'dist_dqn'],
        default='dist_dqn',
        help='RL algorithm to use',
    )
    parser.add_argument(
        '--env_id',
        type=str,
        default='default_18_node_network',
        help='Environment ID to train on',
    )

    # Load configuration
    curr_path = os.getcwd()
    config_file = os.path.join(curr_path, 'examples/configs/config.yaml')
    config = load_yaml_config(config_file)

    # Setup accelerator and parse arguments
    accelerator = Accelerator()
    run_args = parser.parse_args()

    # Get algorithm-specific arguments
    algo_args = get_algo_args(run_args.algo_name)

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
    train_env: gym.Env = make_vect_envs(args.env_id, num_envs=args.num_envs)
    test_env: gym.Env = make_vect_envs(args.env_id, num_envs=args.num_envs)

    # train_env: gym.Env = create_env(env_id=args.env_id)
    # test_env: gym.Env = create_env(env_id=args.env_id)

    # state_shape = train_env.observation_space.shape or train_env.observation_space.n
    # action_shape = train_env.action_space.shape or train_env.action_space.n
    state_shape = (train_env.single_observation_space.shape
                   or train_env.single_observation_space.n)
    action_shape = (train_env.single_action_space.shape
                    or train_env.single_action_space.n)

    args.action_bound = (train_env.action_space.high[0] if isinstance(
        train_env.action_space, gym.spaces.Box) else None)

    if accelerator is None:
        device = get_device(args.device)
        args.num_processes = 1
    else:
        device = accelerator.device
        args.num_processes = accelerator.num_processes

    if accelerator is None or accelerator.is_main_process:
        print('---------------------------------------')
        print('Environment:', args.env_id)
        print('Algorithm:', args.algo_name)
        print('State Shape:', state_shape)
        print('Action Shape:', action_shape)
        print('Action Bound:', args.action_bound)
        print('Num Process:', args.num_processes)
        print('Device:', device)
        print('---------------------------------------')
        print(args)

    # agent
    agent = DQNAgent(
        args=args,
        state_shape=state_shape,
        action_shape=action_shape,
        accelerator=accelerator,
        device=device,
    )
    runner = OffPolicyTrainer(
        args,
        train_env=train_env,
        test_env=test_env,
        agent=agent,
        accelerator=accelerator,
        device=device,
    )
    runner.run()


if __name__ == '__main__':
    main()
