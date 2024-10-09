"""# Network Generator This is a notebook to help creating new networks by
visualizing them."""

import os
import random
import sys

sys.path.append(os.getcwd())
from importlib.resources import files

from cyberwheel.network.network_base import Network
from cyberwheel.network.network_generation.network_generator import \
    NetworkYAMLGenerator


def network_generator(
    num_subnets: int = 10,
    num_hosts_per_subnet: int = 100,
    base_name: str = 'host-network',
) -> None:
    """Generates a network configuration with routers, subnets, and hosts, then
    outputs the configuration as a YAML file and generates a network diagram.

    Args:
        num_subnets (int): The number of subnets to generate. Default is 10.
        num_hosts_per_subnet (int): The number of hosts per subnet. Default is 100.
        base_name (str): The base name for the network and output files. Default is '-host-network'.
    """
    # Calculate the total number of nodes in the network
    total_nodes = num_subnets * num_hosts_per_subnet
    network_name = f'{total_nodes}-{base_name}'
    fig_name = f'{network_name}.png'

    # Initialize the network generator
    network = NetworkYAMLGenerator(network_name=network_name)

    # Add a core router to the network
    core_router_name = 'core_router'
    network.router(core_router_name)

    # Add subnets to the network and connect them to the core router
    for i in range(num_subnets):
        subnet_name = f'subnet{i}'
        ip_range = '192.168.100.0/24'
        network.subnet(subnet_name, core_router_name, ip_range=ip_range)

    # Adding two server subnets
    network.subnet('server_subnet0',
                   core_router_name,
                   ip_range='192.168.100.0/24')
    network.subnet('server_subnet1',
                   core_router_name,
                   ip_range='192.168.101.0/24')

    # Define server and workstation types
    server_types = [
        'mail_server',
        'file_server',
        'web_server',
        'ssh_jump_server',
        'proxy_server',
    ]

    # Add hosts to subnets
    subnet_idx = 0
    for i in range(total_nodes):
        # Switch to the next subnet after filling one
        if i != 0 and i % num_hosts_per_subnet == 0:
            subnet_idx += 1
            network.interface(f'host{i}', f'host{i-1}')
            network.interface(f'host{i-1}', f'host{i}')

        host_name = f'host{i}'
        subnet_name = f'subnet{subnet_idx}'
        network.host(host_name, subnet_name, 'workstation')

    # Add servers to the server subnets
    for i in range(10):
        server_name = f'server{i}'
        server_subnet_name = 'server_subnet0'
        server_type = random.choice(server_types)
        network.host(server_name, server_subnet_name, server_type)

        server_name2 = f'server{i+10}'
        server_subnet_name2 = 'server_subnet1'
        server_type2 = random.choice(server_types)
        network.host(server_name2, server_subnet_name2, server_type2)

    # Create interfaces between hosts and servers
    network.interface('server0', 'host0')
    network.interface('host0', 'server0')

    last_host_name = f'host{total_nodes - 1}'
    network.interface('server10', last_host_name)
    network.interface(last_host_name, 'server10')

    # Save the network configuration as a YAML file in the specified path
    config_path = files('cyberwheel.resources.configs').joinpath('network')
    network.output_yaml(config_path)

    # Generate a network diagram and save it as a PNG file
    yaml_file = config_path.joinpath(f'{network_name}.yaml')
    cyberwheel_network = Network.create_network_from_yaml(yaml_file)
    cyberwheel_network.draw(filename=fig_name)


if __name__ == '__main__':
    network_generator(num_subnets=1500, num_hosts_per_subnet=100)
