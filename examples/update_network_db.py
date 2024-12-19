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
    description = 'A randomly connected graph. With the guarantee that each node will have at least one connection.(一个随机连接的图，保证每个节点至少有一个连接。)'
    author = 'Robin/CyberAttackSim'
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
        Groups cannot connect to each other.(图中有一个中心节点，周围环绕着若干组节点。每组节点与中心节点之间仅有一条连接。各组节点之间无法相互连接。)'

    author = 'Robin/CyberAttackSim'
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
    description = 'Corporate Network(企业网络)'
    author = 'Robin/CyberAttackSim'
    base_name = 'Corporate Network'
    network = network_creator.create_corporate_network()
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

    description = 'Two group Network.(双组网络)'
    author = 'Robin/CyberAttackSim'
    base_name = 'Two group Network'
    network = network_creator.create_p2p()
    name = base_name
    network.set_random_entry_nodes = True
    network.num_of_random_entry_nodes = 1
    network.reset_random_entry_nodes()
    network.set_random_high_value_nodes = True
    network.num_of_random_high_value_nodes = 1
    network.reset_random_high_value_nodes()
    network.set_random_vulnerabilities = True
    network.reset_random_vulnerabilities()
    db.upsert(network,
              name=name,
              description=description,
              author=author,
              locked=True)

    description = 'Ring Network.(环形网络)'
    author = 'Robin/CyberAttackSim'
    base_name = 'Ring Network'
    network = network_creator.create_ring()
    name = base_name
    network.set_random_entry_nodes = True
    network.num_of_random_entry_nodes = 1
    network.reset_random_entry_nodes()
    network.set_random_high_value_nodes = True
    network.num_of_random_high_value_nodes = 1
    network.reset_random_high_value_nodes()
    network.set_random_vulnerabilities = True
    network.reset_random_vulnerabilities()
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

    description = 'Zachary’s Karate Club graph Network.(扎卡里空手道俱乐部关系网络)'
    author = 'Robin/CyberAttackSim'
    base_name = 'Karate Club Network'
    name = base_name
    db.upsert(network,
              name=name,
              description=description,
              author=author,
              locked=True)
