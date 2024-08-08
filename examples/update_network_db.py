import os
import sys

import networkx as nx

sys.path.append(os.getcwd())
from cyberattacksim.networks import network_creator
from cyberattacksim.networks.network_db import NetworkDB
from cyberattacksim.utils.env_utils import (
    get_network_from_edges_and_positions, read_nodes_edges_from_file)

if __name__ == '__main__':
    db = NetworkDB()
    db.rebuild_db()

    # creat randomly connected graph
    description = 'A randomly connected graph. With the guarantee that each node will have at least one connection.'
    author = 'Robion/CyberAttack'
    base_name = 'Randomly Connected Network'
    node_list = [30, 50, 100]
    for n_nodes in node_list:
        network = network_creator.gnp_random_connected_graph(
            n_nodes=n_nodes, probability_of_edge=0.02)
        network.set_random_entry_nodes = True
        network.num_of_random_entry_nodes = 3
        network.reset_random_entry_nodes()
        network.set_random_high_value_nodes = True
        network.num_of_random_high_value_nodes = 3
        network.reset_random_high_value_nodes()
        network.set_random_vulnerabilities = True
        network.reset_random_vulnerabilities()
        name = base_name + ':' + str(n_nodes) + '-nodes'
        db.upsert(network,
                  name=name,
                  description=description,
                  author=author,
                  locked=True)

    # creat star graph
    description = 'This is one node in the middle with groups of nodes around it. \
        There is only one connection between a group and the center node.\
        Groups cannot connect to each other.'

    author = 'Robion/CyberAttack'
    base_name = 'Star Node Network'
    network = network_creator.create_star(first_layer_size=8,
                                          group_size=5,
                                          group_connectivity=0.5)
    network.set_random_entry_nodes = True
    network.num_of_random_entry_nodes = 1
    network.reset_random_entry_nodes()
    network.set_random_high_value_nodes = True
    network.num_of_random_high_value_nodes = 1
    network.reset_random_high_value_nodes()
    network.set_random_vulnerabilities = True
    network.reset_random_vulnerabilities()
    name = base_name
    db.upsert(network,
              name=name,
              description=description,
              author=author,
              locked=True)

    # creat star graph
    description = 'Corporate Network'
    author = 'Robion/CyberAttack'
    base_name = 'Corporate Network'
    network = network_creator.create_corporate_network()
    name = base_name
    db.upsert(network,
              name=name,
              description=description,
              author=author,
              locked=True)

    # Craete Real Network
    current_dir = os.getcwd()
    # directories
    log_dir = os.path.join(current_dir, 'work_dir', 'random_nodes_logs_dir')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    edges_file = os.path.join(log_dir, 'random_nodes.edgelist')
    G = nx.karate_club_graph()
    pos = nx.spring_layout(G, iterations=100, seed=42)

    nx.write_edgelist(G, edges_file)
    nodes, edges = read_nodes_edges_from_file(edges_file)
    network = get_network_from_edges_and_positions(edges, pos)

    network.set_random_entry_nodes = True
    network.num_of_random_entry_nodes = 3
    network.reset_random_entry_nodes()
    network.set_random_high_value_nodes = True
    network.num_of_random_high_value_nodes = 3
    network.reset_random_high_value_nodes()
    network.set_random_vulnerabilities = True
    network.reset_random_vulnerabilities()

    description = 'Zachary’s Karate Club graph.'
    author = 'Robion/CyberAttack'
    base_name = 'Karate Club Network'
    name = base_name
    db.upsert(network,
              name=name,
              description=description,
              author=author,
              locked=True)
