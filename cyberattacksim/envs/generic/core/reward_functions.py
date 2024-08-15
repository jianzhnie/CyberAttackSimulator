"""A collection of reward functions used be the generic network environment.

You can select the reward function that you wish to use in the config file under settings.
The reward functions take in a parameter called args. args is a dictionary that contains the
following information:
    -network_interface: Interface with the network
    -blue_action: The action that the blue agent has taken this turn
    -blue_node: The node that the blue agent has targeted for their action
    -start_state: The state of the nodes before the blue agent has taken their action
    -end_state: The state of the nodes after the blue agent has taken their action
    -start_vulnerabilities: The vulnerabilities before blue agents turn
    -end_vulnerabilities: The vulnerabilities after the blue agents turn
    -start_isolation: The isolation status of all the nodes at the start of a turn
    -end_isolation: The isolation status of all the nodes at the end of a turn
    -start_blue: The env as the blue agent can see it before the blue agents turn
    -end_blue: The env as the blue agent can see it after the blue agents turn

The reward function returns a single number (integer or float) that is the blue agents reward for that turn.
"""

# Functions:
from __future__ import annotations

import math

from cyberattacksim.envs.generic.core.network_interface import NetworkInterface

REMOVE_RED_POINTS = []
for i in range(0, 101):
    REMOVE_RED_POINTS.append(round(math.exp(-0.004 * i), 4))

REDUCE_VULNERABILITY_POINTS = []
for i in range(1, 20):
    REDUCE_VULNERABILITY_POINTS.append(2 / (10 + math.exp(4 - 10 * (i / 20))) +
                                       0.5)

SCANNING_USAGE_POINTS = []
for i in range(0, 100):
    SCANNING_USAGE_POINTS.append(-math.exp(-i) + 1)


def standard_rewards(args: dict) -> float:
    """Calculate the reward for the current state of the environment.
    这个函数计算当前环境状态下的奖励，主要基于蓝方（blue agent）的行动和其对网络状态的影响。
    蓝方的行动包括减少节点的脆弱性、恢复节点、安全化节点等。每种行动都有一个对应的成本和奖励机制。

    Actions cost a certain amount and blue gets rewarded for removing red nodes and
    reducing the vulnerability of nodes

    主要内容:

        1. 行动成本:

        - reduce_vulnerability、make_node_safe 等有不同的成本（如 0.5、1）。
        - do_nothing 行动会受到负面奖励（-0.5）。
        - add_deceptive_node 的成本较高（8）。

        2. 奖励计算:

        - 减少脆弱性：如果节点的脆弱性减少了，给予奖励。
        - 恢复节点：如果节点恢复正常，给予奖励。
        - 扫描：如果扫描揭示了大量的红色节点，给予奖励。
        - 隔离节点：对隔离节点的处罚不重复计入奖励。

        3.特殊条件:

        - 如果蓝方没有采取任何行动且环境中有大量红色节点，会受到处罚。
        - 连接节点的奖励会根据隔离状态的变化来调整。

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        The reward earned for this specific turn for the blue agent
    """
    # Get information about the current state of the environment
    network_interface: NetworkInterface = args['network_interface']
    blue_action = args['blue_action']
    start_state = args['start_state']
    end_state = args['end_state']
    start_vulnerabilities = args['start_vulnerabilities']
    end_vulnerabilities = args['end_vulnerabilities']
    start_isolation = args['start_isolation']
    end_isolation = args['end_isolation']
    start_blue = args['start_blue']
    end_blue = args['end_blue']

    # cost for actions
    action_cost = {
        'reduce_vulnerability': 0.5,
        'restore_node': 1,
        'make_node_safe': 0.5,
        'scan': 0,
        'isolate': 1,
        'connect': 0,
        'do_nothing': -0.5,
        'add_deceptive_node': 8,
    }

    # prevent isolate reward from being duplicated
    reward = -action_cost[blue_action] if blue_action != 'isolate' else 0

    # punish agent for every node it has isolated
    reward += -action_cost['isolate'] * sum(end_isolation.values())

    # calculating number of red nodes before and after the blue agents turn
    initial_cumulative_states = sum(start_state.values())
    final_cumulative_states = sum(end_state.values())

    # punish agent for doing nothing if there are large numbers or red controlled nodes in the environment
    if blue_action == 'do_nothing':
        reward = reward - (0.2 * final_cumulative_states)

    if blue_action == 'connect':
        if sum(end_isolation.values()) < sum(start_isolation.values()):
            reward += 5
        else:
            reward -= 5

    # rewards for removing red nodes
    if initial_cumulative_states > final_cumulative_states:
        reward += REMOVE_RED_POINTS[round(
            100 * final_cumulative_states /
            network_interface.current_graph.number_of_nodes())]

    # punish agent for doing nothing if there are large numbers or red controlled nodes in the environment
    if blue_action != 'make_node_safe' and blue_action != 'restore_node':
        amount = (final_cumulative_states /
                  network_interface.current_graph.number_of_nodes())
        if amount > 0.3:
            reward = reward - amount + 0.3

    # punish the blue agent for patching nodes that are already safe
    if blue_action == 'make_node_safe' or blue_action == 'restore_node':
        if initial_cumulative_states == final_cumulative_states:
            reward = reward - 3

    # punish the blue agent for reducing the vulnerability of a node that is already at minimum vulnerability
    if blue_action == 'reduce_vulnerability' or blue_action == 'restore_node':
        if sum(start_vulnerabilities.values()) == sum(
                end_vulnerabilities.values()):
            reward = reward - 0.5

    # reward for revealing red
    if blue_action == 'scan':
        number = 0
        for node, value in end_blue.items():
            if value == 1 and start_blue[node] == 0:
                if start_state[node] == 1:
                    number += 1
        if number >= 5:
            reward += 2.5
        else:
            reward += number * 0.5

    # rewards for reducing node vulnerabilities
    if (network_interface.game_mode.red.agent_attack.ignores_defences.value is
            False and blue_action == 'reduce_vulnerability'):
        initial_cumulative_vuln = sum(start_vulnerabilities.values())
        final_cumulative_vuln = sum(end_vulnerabilities.values())
        reward = reward + (initial_cumulative_vuln - final_cumulative_vuln) * 4

    if blue_action == 'add_deceptive_node':
        if network_interface.reached_max_deceptive_nodes:
            reward -= 5

    return reward


def experimental_rewards(args: dict) -> float:
    """Calculate the reward for the current state of the environment.

    Actions cost a certain amount and blue gets rewarded for removing red nodes and
    reducing the vulnerability of nodes

    主要内容:

        1. 行动成本:

            - 大部分行动的成本被设置为较低（如 reduce_vulnerability 为 0）。
            - isolate 行动的成本较高（10）。

        2. 奖励计算:

            - 节点安全：如果节点变安全，给予奖励。
            - 做无事：如果蓝方选择不行动，且环境中的红色节点很多，则受到更高的处罚。
            - 视野分数：基于蓝方视图和实际状态之间的差异计算惩罚。

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        The reward earned for this specific turn for the blue agent
    """
    # Get information about the current state of the environment
    network_interface: NetworkInterface = args['network_interface']
    blue_action = args['blue_action']
    start_state = args['start_state']
    end_state = args['end_state']
    start_blue = args['start_blue']
    end_blue = args['end_blue']

    # cost for actions
    action_cost = {
        'reduce_vulnerability': 0,
        'restore_node': 1,
        'make_node_safe': 0,
        'scan': 0,
        'isolate': 10,
        'connect': 0,
        'do_nothing': -0.5,
        'add_deceptive_node': 2,
    }

    reward = -action_cost[blue_action]
    # calculating number of red nodes before and after the blue agents turn
    initial_cumulative_states = sum(start_state.values())
    final_cumulative_states = sum(end_state.values())
    # calculating the vulnerability of all the nodes before and after the blue agents turn
    # blue's view
    initial_blue_states = sum(start_blue.values())
    final_blue_states = sum(end_blue.values())

    # rewards for removing red nodes
    # gives between 0.5 and 1
    if blue_action == 'make_node_safe' or blue_action == 'restore_node':
        if initial_blue_states > final_blue_states:
            reward += REMOVE_RED_POINTS[round(
                100 * final_cumulative_states /
                network_interface.current_graph.number_of_nodes())]
        elif initial_cumulative_states > final_cumulative_states:
            pass
        else:
            reward -= 1

    # punish agent for doing nothing if there are large numbers or red controlled nodes in the environment
    if blue_action == 'do_nothing':
        reward = reward - (0.5 * final_cumulative_states)

    vision_score = 0.01 * (final_cumulative_states - final_blue_states)**2

    reward -= vision_score

    return reward


# A very simple example reward function
def one_per_timestep(args: dict) -> float:
    """Give a reward for 0.1 for every timestep that the blue agent is alive.
    每个时间步（timestep）给定固定的奖励（0.1），无论蓝方的具体行动或环境状态如何。

    主要内容:
        这个奖励函数非常简单，适用于测试基本的奖励机制或者作为一个基线奖励。

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        0.1
    """
    return 0.1


def zero_reward(args: dict) -> float:
    """Return zero reward per timestep. 每个时间步返回 0 的奖励。

    主要内容:
        这是一个占位符，用于测试或者在需要时提供零奖励。通常情况下，这种奖励函数用于特定的测试或调试场景。

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        0
    """
    return 0


def safe_nodes_give_rewards(args: dict) -> float:
    """Give 1 reward for every safe node at that timestep. 根据网络中安全节点的比例给予奖励。

    主要内容:
        奖励等于安全节点的数量，即网络中总节点数减去红色节点的数量。

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        The reward earned for this specific turn for the blue agent
    """
    # Get information about the current state of the environment
    end_state = args['end_state']

    final_cumulative_states = sum(end_state.values())

    # reward is equal to the number of safe nodes
    reward = len(end_state) - final_cumulative_states

    return reward


def punish_bad_actions(args: dict) -> float:
    """Just punishes bad actions bad moves.

    目的:
        惩罚不好的行动，比如没有采取行动或修复已经安全的节点。

    主要内容:

        1.不行动的惩罚:
            如果蓝方选择不行动，会受到与最终红色节点数量相关的惩罚。

        2.修复已经安全的节点:
            如果修复的节点本来已经安全，则受到惩罚。

        3.减少脆弱性的惩罚:
            如果节点的脆弱性没有减少，也会受到惩罚。

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        The reward earned for this specific turn for the blue agent
    """
    # Get information about the current state of the game
    network_interface: NetworkInterface = args['network_interface']
    blue_action = args['blue_action']
    start_state = args['start_state']
    end_state = args['end_state']
    start_vulnerabilities = args['start_vulnerabilities']
    end_vulnerabilities = args['end_vulnerabilities']

    # Get number of safe states before and after the blue agents turn
    initial_cumulative_states = sum(start_state.values())
    final_cumulative_states = sum(end_state.values())

    reward = 0

    # punish agent for doing nothing if there are large numbers or red controlled nodes in the environment
    if blue_action == 'do_nothing':
        reward = reward - (0.5 * final_cumulative_states)
    # punish the blue agent for patching nodes that are already safe
    if blue_action == 'make_node_safe' or blue_action == 'restore_node':
        if initial_cumulative_states == final_cumulative_states:
            reward = reward - (0.2 * initial_cumulative_states)

    # punish the blue agent for reducing the vulnerability of a node that is already at minimum vulnerability
    if blue_action == 'reduce_vulnerability' and (sum(
            start_vulnerabilities.values()) == sum(
                end_vulnerabilities.values())):
        reward = reward - 1

    # punish for relocating deceptive nodes (after it has already been placed)
    if blue_action == 'add_deceptive_node':
        if network_interface.reached_max_deceptive_nodes:
            reward = reward - 5

    return reward


def num_nodes_safe(args: dict) -> float:
    """Provide reward based on the proportion of nodes safe within the
    environment.

    根据网络中安全节点的比例计算奖励。

    主要内容:
        奖励等于安全节点的数量除以总节点数。这个函数奖励网络中更多的安全节点。

    Args:
        args: A dictionary containing information from the
        environment for the given timestep

    Returns:
        The calculated reward
    """
    total_n_nodes = len(args['end_state'].values())
    n_compromised = sum(args['end_state'].values())
    n_safe = total_n_nodes - n_compromised

    return n_safe / total_n_nodes


def dcbo_cost_func(args: dict) -> float:
    """Calculate the cost function for DCBO using a set of fixed action cost
    values.

    计算 DCBO（Dynamic Cost-Benefit Optimization）方法的成本函数。

    主要内容:
        行动成本: 各种行动的固定成本。
        总成本: 基于最终红色节点数量的总成本计算公式，负值表示成本。

    Args:
        args: A dictionary containing the following items:
            network_interface: Interface with the network
            blue_action: The action that the blue agent has taken this turn
            blue_node: The node that the blue agent has targeted for their action
            start_state: The state of the nodes before the blue agent has taken their action
            end_state: The state of the nodes after the blue agent has taken their action
            start_vulnerabilities: The vulnerabilities before blue agents turn
            end_vulnerabilities: The vulnerabilities after the blue agents turn
            start_isolation: The isolation status of all the nodes at the start of a turn
            end_isolation: The isolation status of all the nodes at the end of a turn
            start_blue: The env as the blue agent can see it before the blue agents turn
            end_blue: The env as the blue agent can see it after the blue agents turn

    Returns:
        The cost for DCBO
    """
    # Get information about the current state of the environment
    blue_action = args['blue_action']
    end_state = args['end_state']

    # cost for actions
    action_cost = {
        'reduce_vulnerability': 0,
        'restore_node': 1,
        'make_node_safe': 1,
        'scan': 0,
        'isolate': 1,
        'connect': 0,
        'do_nothing': 0,
        'add_deceptive_node': 0,
    }

    reward = action_cost[blue_action]
    # calculating number of red nodes before and after the blue agents turn
    final_cumulative_states = sum(end_state.values())

    cost = final_cumulative_states * 10 + reward

    return 0 - cost
