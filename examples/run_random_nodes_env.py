import os
import sys

import networkx as nx
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy as PPOMlp
from yawning_titan.envs.generic.core.blue_interface import BlueInterface
from yawning_titan.envs.generic.core.network_interface import NetworkInterface
from yawning_titan.envs.generic.core.red_interface import RedInterface
from yawning_titan.envs.generic.generic_env import GenericNetworkEnv
from yawning_titan.game_modes.game_mode_db import default_game_mode

sys.path.append(os.getcwd())
import os
import time

from nasimulator.agents.action_loop import ActionLoop
from nasimulator.utils.env_utils import (get_network_from_edges_and_positions,
                                         read_nodes_edges_from_file)

if __name__ == '__main__':
    # get the current directory
    current_dir = os.getcwd()
    # directories
    log_dir = os.path.join(current_dir, 'work_dir', 'random_nodes_logs_dir')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    edges_file = os.path.join(log_dir, 'random_nodes.edgelist')

    start_time = time.time()
    G = nx.complete_graph(12)
    G = nx.cycle_graph(24)
    G = nx.wheel_graph(20)
    G = nx.erdos_renyi_graph(100, 0.5)
    G = nx.karate_club_graph()
    pos = nx.spring_layout(G, iterations=100, seed=42)
    nx.write_edgelist(G, edges_file)
    nodes, edges = read_nodes_edges_from_file(edges_file)
    network = get_network_from_edges_and_positions(edges, pos)
    # network = create_star(first_layer_size=8, group_size=5, group_connectivity=0.5)
    end_time = time.time()
    print(f'Network Created: {end_time-start_time} seconds!!!')
    start_time = time.time()
    network.set_random_entry_nodes = True
    network.num_of_random_entry_nodes = 3
    network.reset_random_entry_nodes()
    end_time = time.time()
    print(f'Network Reset: {end_time-start_time}')
    start_time = time.time()
    network.set_random_high_value_nodes = True
    network.num_of_random_high_value_nodes = 3
    network.reset_random_high_value_nodes()
    end_time = time.time()
    print(f'Network Reset: {end_time-start_time}')
    start_time = time.time()
    network.set_random_vulnerabilities = True
    network.reset_random_vulnerabilities()
    end_time = time.time()
    print(f'Network Reset: {end_time-start_time}')
    game_mode = default_game_mode()
    network_interface = NetworkInterface(game_mode=game_mode, network=network)
    red = RedInterface(network_interface)
    blue = BlueInterface(network_interface)
    env = GenericNetworkEnv(red, blue, network_interface)
    _ = env.reset()
    done = False
    steps = 0
    while not done:
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        env.render()
        print(reward)
        steps += 1
    print(f'Episode finished after {steps} steps')
    action_space = env.action_space
    agent = PPO(PPOMlp, env, verbose=1)
    agent.learn(total_timesteps=1000)
    loop = ActionLoop(env, agent, episode_count=5)
    loop.gif_action_loop(
        save_gif=True,
        render_network=True,
        save_webm=True,
        gif_output_directory=log_dir,
        webm_output_directory=log_dir,
    )
