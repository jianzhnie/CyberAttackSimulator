import os
import time

import gymnasium as gym
import networkx as nx
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.game_modes.game_mode_db import default_game_mode
from yawning_titan.networks.network import Network

from simulator.utils import get_network_from_nodes_edges, read_edges_from_file


def creat_env(network: Network) -> gym.Env:
    network.set_random_entry_nodes = True
    network.num_of_random_entry_nodes = 1
    network.reset_random_entry_nodes()
    network.set_random_high_value_nodes = True
    network.num_of_random_high_value_nodes = 3
    network.reset_random_high_value_nodes()
    network.set_random_vulnerabilities = True
    network.reset_random_vulnerabilities()
    game_mode = default_game_mode()
    network_interface = NetworkInterface(game_mode=game_mode, network=network)
    red_attacker = RedInterface(network_interface)
    blue_offender = BlueInterface(network_interface)
    env = GenericNetworkEnv(
        red_agent=red_attacker,
        blue_agent=blue_offender,
        network_interface=network_interface,
        print_metrics=True,
    )
    return env


if __name__ == '__main__':
    start_time = time.time()
    G = nx.wheel_graph(100)
    data_dir = './data'
    file_path = os.path.join(data_dir, 'wheel_graph.edgelist')
    nx.write_edgelist(G, file_path)
    nodes, edges = read_edges_from_file(file_path)
    network = get_network_from_nodes_edges(nodes, edges)
    end_time = time.time()
    print(f'Time to create network: {end_time - start_time}')

    start_time = time.time()
    env = creat_env(network)
    end_time = time.time()
    print(f'Time to create env: {end_time - start_time}')
    done = False
    steps = 0
    obs = env.reset()
    start_time = time.time()
    while not done:
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        steps += 1
    end_time = time.time()
    print(f'Env finished after {steps} steps, time: {end_time - start_time}')
