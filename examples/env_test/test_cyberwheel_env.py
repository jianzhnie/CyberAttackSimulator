import os
import sys
from copy import deepcopy
from importlib.resources import files

import gymnasium as gym

sys.path.append(os.getcwd())
from cyberwheel.cyberwheel_envs.cyberwheel_dynamic import DynamicCyberwheel
from cyberwheel.network.network_base import Network
from cyberwheel.red_agents import ARTAgent
from cyberwheel.red_agents.strategies import DFSImpact, ServerDowntime


def create_cyberwheel_env(
    network_config: str = '15-host-network.yaml',
    decoy_config: str = 'decoy_hosts.yaml',
    host_config: str = 'host_definitions.yaml',
    detector_config: str = 'example_detector_handler.yaml',
    min_decoys: int = 0,
    max_decoys: int = 1,
    reward_scaling: float = 10.0,
    reward_function: str = 'default',
    red_agent: str = 'art_agent',
    blue_config: str = 'dynamic_blue_agent.yaml',
    num_steps: int = 100,
    red_strategy: str = 'server_downtime',
) -> DynamicCyberwheel:
    """Creates a DynamicCyberwheel environment."""

    # Load network from yaml here
    network_config = files('cyberwheel.resources.configs.network').joinpath(
        network_config)
    print(f'Building network: {network_config} ...')
    network = Network.create_network_from_yaml(network_config)

    print('Mapping attack validity to hosts...', end=' ')
    service_mapping = {}
    if red_agent == 'art_agent':
        service_mapping = ARTAgent.get_service_map(network)

    if red_strategy == 'dfs_impact':
        red_strategy = DFSImpact
    else:
        red_strategy = ServerDowntime

    env: gym.Env = DynamicCyberwheel(
        network_config=network_config,
        decoy_host_file=decoy_config,
        host_def_file=host_config,
        detector_config=detector_config,
        min_decoys=min_decoys,
        max_decoys=max_decoys,
        blue_reward_scaling=reward_scaling,
        reward_function=reward_function,
        red_agent=red_agent,
        blue_config=blue_config,
        num_steps=num_steps,
        network=deepcopy(network),
        service_mapping=service_mapping,
        red_strategy=red_strategy,
    )

    return env


def create_massive_node_env(network_size: int = 10):
    if network_size == 10:
        network_config = '10-host-network.yaml'
    if network_size == 50:
        network_config = '50-host-network.yaml'
    if network_size == 200:
        network_config = '200-host-network.yaml'

    if network_size == 1000:
        network_config = '1000-host-network.yaml'
    if network_size == 5000:
        network_config = '5000-host-network.yaml'
    if network_size == 10000:
        network_config = '10000-host-network.yaml'

    if network_size == 100000:
        network_config = '100000-host-network.yaml'
    if network_size == 150000:
        network_config = '150000-host-network.yaml'

    env = create_cyberwheel_env(network_config)

    return env


if __name__ == '__main__':
    # Load network from yaml here
    env = create_massive_node_env(network_size=100000)

    done = False
    steps = 0
    obs, _ = env.reset()
    while not done:
        action = env.action_space.sample()
        obs, reward, done, truncated, info = env.step(action)
        print(reward, done, truncated, info)
        steps += 1
    print(f'Env finished after {steps} steps')
