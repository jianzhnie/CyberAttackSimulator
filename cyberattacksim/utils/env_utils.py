import random
from typing import Any, Dict, List, Tuple

import numpy as np
from stable_baselines3.common.env_checker import check_env

from cyberattacksim.envs.generic.core.blue_interface import BlueInterface
from cyberattacksim.envs.generic.core.network_interface import NetworkInterface
from cyberattacksim.envs.generic.core.red_interface import RedInterface
from cyberattacksim.envs.generic.generic_env import GenericNetworkEnv
from cyberattacksim.game_modes.game_mode_db import (dcbo_game_mode,
                                                    default_game_mode)
from cyberattacksim.networks import network_creator
from cyberattacksim.networks.network import Network
from cyberattacksim.networks.network_db import (dcbo_base_network,
                                                default_18_node_network)
from cyberattacksim.networks.node import Node


def create_env(
    env_id: str,
    node_size: int = 18,
) -> GenericNetworkEnv:
    """Create a CyberAttackSim environment.

    :param use_same_net: If true uses a saved network, otherwise creates a new
        network.

    :returns: A CyberAttackSim OpenAI Gym environment.
    """
    if env_id == 'default_18_node_network':
        network = default_18_node_network()
        game_mode = default_game_mode()

    elif env_id == 'dcbo_base_network':
        network = dcbo_base_network()
        game_mode = dcbo_game_mode()

    elif env_id == 'random_connected_network':
        network = network_creator.gnp_random_connected_graph(
            n_nodes=node_size, probability_of_edge=0.02)
        network.set_random_entry_nodes = True
        network.num_of_random_entry_nodes = 3
        network.reset_random_entry_nodes()
        network.set_random_high_value_nodes = True
        network.num_of_random_high_value_nodes = 3
        network.reset_random_high_value_nodes()
        network.set_random_vulnerabilities = True
        network.reset_random_vulnerabilities()

        game_mode = default_game_mode()

    else:
        raise NotImplementedError

    network_interface = NetworkInterface(game_mode=game_mode, network=network)
    red = RedInterface(network_interface)
    blue = BlueInterface(network_interface)
    env = GenericNetworkEnv(
        red_agent=red,
        blue_agent=blue,
        network_interface=network_interface,
        print_metrics=True,
        show_metrics_every=50,
        collect_additional_per_ts_data=True,
        print_per_ts_data=False,
    )

    check_env(env, warn=True)
    env.reset()
    return env


def get_network_from_edges_and_positions(
    edges: List[Tuple],
    positions: Dict[str, np.ndarray],
) -> Network:
    """Create a network from a list of edges and a dictionary of node
    positions.

    :param edges: A list of edges, (node_a, node_b, extra_info)
    :param positions: The node positions on a graph.
    :return: An instance of :class:`~cyberattacksim.networks.network.Network`.
    """
    network = Network()
    nodes: Dict[Any, Node] = {}
    for node_name in positions:
        position = positions[node_name].tolist()
        node = Node(name=str(node_name))
        nodes[str(node_name)] = node
        node.x_pos = position[0]
        node.y_pos = position[1]
        network.add_node(node)
    for edge in edges:
        node_a = str(edge[0])
        node_b = str(edge[1])
        network.add_edge(nodes[node_a], nodes[node_b])
    return network


def get_network_from_nodes_edges(
    node_list: List[str],
    edges_list: List[Tuple],
    set_random_entry_nodes: bool = False,
    num_of_random_entry_nodes: int = 0,
    set_random_high_value_nodes: bool = False,
    num_of_random_high_value_nodes: int = 0,
) -> Network:
    """Create a network from a list of node names and a list of edges.

    :param node_names: A list of node names.
    :param edges: A list of edges, (node_a, node_b, extra_info)
    :return: An instance of :class:`~cyberattacksim.networks.network.Network`.
    """
    network = Network()
    nodes: Dict[Any, Node] = {}
    if set_random_entry_nodes:
        possible_entry_nodes = set(node_list)
        entry_nodes = random.sample(
            possible_entry_nodes,
            num_of_random_entry_nodes,
        )

    if set_random_high_value_nodes:
        possible_high_value_nodes = set(node_list)
        high_value_nodes = random.sample(
            possible_high_value_nodes,
            num_of_random_high_value_nodes,
        )

    for node_name in node_list:
        entry_node = False
        high_value_node = False
        if node_name in entry_nodes:
            entry_node = True
        if node_name in high_value_nodes:
            high_value_node = True
        node = Node(
            name=str(node_name),
            entry_node=entry_node,
            high_value_node=high_value_node,
        )
        nodes[str(node_name)] = node
        network.add_node(node)

    for edge in edges_list:
        node_a = str(edge[0])
        node_b = str(edge[1])
        network.add_edge(nodes[node_a], nodes[node_b])
    return network


def read_nodes_edges_from_file(file_path: str) -> tuple[list, list]:
    """Read edges from a file and return a list of nodes and a list of edges.

    Args:
        file_path (str): file path

    Returns:
        tuple[list, list]: list of nodes and list of edges
    """
    nodes = set()
    edges = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            parts = line.strip().split(' ')
            if len(parts) >= 2:
                start_node = str(parts[0])
                end_node = str(parts[1])
                extra_info = parts[2]
                nodes.add(start_node)
                nodes.add(end_node)
                edges.append((start_node, end_node, extra_info))

    return list(nodes), edges
