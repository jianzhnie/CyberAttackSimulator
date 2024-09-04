import os
import sys
import time

import gymnasium as gym
import networkx as nx

sys.path.append(os.getcwd())

from cyberattacksim.envs.generic.core.blue_interface import BlueInterface
from cyberattacksim.envs.generic.core.network_interface import NetworkInterface
from cyberattacksim.envs.generic.core.red_interface import RedInterface
from cyberattacksim.envs.generic.generic_env import GenericNetworkEnv
from cyberattacksim.game_modes.game_mode_db import default_game_mode
from cyberattacksim.networks.network import Network
from cyberattacksim.utils.env_utils import (get_network_from_nodes_edges,
                                            read_nodes_edges_from_file)


def creat_genetic_network(
    graph_name: str,
    num_nodes: int = 10,
    data_dir: str = './data',
    seed: int = 42,
) -> None:
    if graph_name == 'wheel_graph':
        base_graph = nx.wheel_graph(10000)
    elif graph_name == 'path_graph':
        base_graph = nx.path_graph()
    elif graph_name == 'complete_graph':
        base_graph = nx.complete_graph(num_nodes)
    elif graph_name == 'random_internet':
        base_graph = nx.random_internet_as_graph(num_nodes, seed=seed)
    else:
        raise ValueError('Invalid graph name')

    file_path = os.path.join(data_dir, 'graph.edgelist')
    nx.write_edgelist(base_graph, file_path)
    nodes, edges = read_nodes_edges_from_file(file_path)
    network = get_network_from_nodes_edges(nodes, edges)
    return network


def creat_generic_env(network: Network) -> gym.Env:
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


def creat_massive_network(
    graph_name: str = 'path_graph',
    num_nodes: int = 10000,
    data_dir: str = './data',
    set_random_entry_nodes: bool = True,
    num_of_random_entry_nodes: int = 10,
    set_random_high_value_nodes: bool = True,
    num_of_random_high_value_nodes: int = 10,
    seed: int = 42,
) -> None:
    if graph_name == 'wheel_graph':
        base_graph = nx.wheel_graph(num_nodes)
    elif graph_name == 'path_graph':
        base_graph = nx.path_graph(num_nodes)
    elif graph_name == 'complete_graph':
        base_graph = nx.complete_graph(num_nodes)
    elif graph_name == 'random_internet':
        base_graph = nx.random_internet_as_graph(num_nodes, seed=seed)
    else:
        raise ValueError('Invalid graph name')

    file_path = os.path.join(data_dir, 'graph.edgelist')
    nx.write_edgelist(base_graph, file_path)
    nodes, edges = read_nodes_edges_from_file(file_path)
    network = get_network_from_nodes_edges(
        nodes,
        edges,
        set_random_entry_nodes=set_random_entry_nodes,
        num_of_random_entry_nodes=num_of_random_entry_nodes,
        set_random_high_value_nodes=set_random_high_value_nodes,
        num_of_random_high_value_nodes=num_of_random_high_value_nodes,
    )
    return network


def creat_massive_env(network: Network) -> gym.Env:
    game_mode = default_game_mode()
    start_time = time.time()
    network_interface = NetworkInterface(game_mode=game_mode, network=network)
    end_time = time.time()
    print(f'NetworkInterface Time Cost: {end_time - start_time}')
    start_time = time.time()
    red_attacker = RedInterface(network_interface)
    blue_offender = BlueInterface(network_interface)
    end_time = time.time()
    print(f'Red and Blue Interface Create Time Cost: {end_time - start_time}')
    env = GenericNetworkEnv(
        red_agent=red_attacker,
        blue_agent=blue_offender,
        network_interface=network_interface,
        print_metrics=True,
    )
    return env


if __name__ == '__main__':
    start_time = time.time()
    network = creat_massive_network(graph_name='path_graph',
                                    data_dir='work_dir/networks',
                                    num_nodes=100)
    end_time = time.time()
    print(f'Time to create network: {end_time - start_time}')
    start_time = time.time()
    env = creat_massive_env(network)
    end_time = time.time()
    print(f'Time to create env: {end_time - start_time}')
    done = False
    steps = 0
    obs, _ = env.reset()
    start_time = time.time()
    while not done:
        action = env.action_space.sample()
        obs, reward, done, truncated, info = env.step(action)
        print(reward, done, truncated)
        steps += 1
    end_time = time.time()
    print(f'Env finished after {steps} steps, time: {end_time - start_time}')
