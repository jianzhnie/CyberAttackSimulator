from __future__ import annotations

import copy
import itertools
import json
import math
import random
from collections import defaultdict
from datetime import datetime
from logging import getLogger
from typing import Dict, List, Tuple, Union

import networkx as nx
import numpy as np

from cyberattacksim.game_modes.game_mode import GameMode
from cyberattacksim.networks.network import Network
from cyberattacksim.networks.node import Node

_LOGGER = getLogger(__name__)


class NetworkInterface:
    """The primary interface between both red and blue agents and the
    underlying environment.

    这段代码定义了一个 NetworkInterface 类，负责在红方和蓝方代理之间以及环境之间进行交互。
    它实现了一系列方法来管理网络状态、获取网络特性、以及生成给定场景下的观察空间。
    """

    def __init__(self, game_mode: GameMode, network: Network):
        """Initialise the Network Interface and initialises all the necessary
        components.

        :param game_mode: the :class:`~cyberattacksim.game_modes.game_mode.GameMode` that defines the abilities of the agents.
        :param network: the :class:`~cyberattacksim.networks.network.Network` that defines the network within which the agents act.
        """
        # opens the fle the user has specified to be the location of the game_mode

        self.game_mode: GameMode = game_mode
        self.current_graph: Network = network

        self.random_seed = self.game_mode.miscellaneous.random_seed.value

        # initialise the base graph
        self.base_graph = copy.deepcopy(self.current_graph)
        self.initial_base_graph = copy.deepcopy(self.current_graph)

        # initialises the deceptive nodes and their names and amount
        # initialise_deceptive_nodes() 初始化了欺骗节点，欺骗节点是用于防御或迷惑对方的特殊节点。
        self.initialise_deceptive_nodes()

        # a pointer to to point to the current deceptive node (when a new node is added but the max is reached the
        # oldest node is replaced)
        # deceptive_node_pointer 用于指向当前正在使用的欺骗节点，当添加新的节点时，旧的节点可能会被替换。
        self.deceptive_node_pointer = 0
        self.current_deceptive_nodes = 0
        self.reached_max_deceptive_nodes = False

        # a edge dictionary to give each edge a unique single number
        # 一个包含 `网络边` 的字典映射
        self.initialise_edge_map()

        self.red_current_location: Node = None

        # a list of all of the failed attacks that occurred on this turn
        self.true_attacks = []
        # a list of all the failed attacks that blue has been able to detect
        self.detected_attacks = []

        # 计算网络的连通性
        edges_per_node = len(
            self.current_graph.edges) / (2 * len(self.current_graph.nodes))

        self.connectivity = -math.exp(-0.1 * edges_per_node) + 1

        # 转换当前图为邻接矩阵 (adj_matrix)
        self.adj_matrix = nx.to_numpy_array(self.current_graph)

    # GETTERS (下面这些方法是为了获取当前网络状态的不同属性。)
    # The following block of code contains the getters for the network interface. Getters are methods that (given
    # parameters) will return some attribute from the class

    # 获取每个节点到目标节点的最短距离。
    def get_shortest_distances_to_target(self,
                                         nodes: List[Node]) -> List[float]:
        """Get a list of the shortest distances from each node to the
        target."""
        # TODO: add option where only shortest distance provided

        dist_matrix = dict(
            nx.single_source_shortest_path_length(self.current_graph,
                                                  self.get_target_node()))
        distances = [dist_matrix[n] for n in nodes]
        return distances

    # 获取被攻击的目标节点。
    def get_target_node(self) -> Node:
        """Get the node which is being targeted in the config.

        Returns:
            The target node if it exists
        """
        return self.current_graph.get_node_from_name(
            self.game_mode.red.target_mechanism.target_specific_node.target.
            value)

    # 获取包括尚未使用的欺骗节点在内的节点总数。
    def get_total_num_nodes(self) -> int:
        """Get the total number of nodes including any yet to be placed
        deceptive nodes.

        Returns:
            The number of nodes that there are including deceptive nodes that may not have been placed yet
        """
        return (self.current_graph.number_of_nodes() +
                self.get_number_unused_deceptive_nodes())

    # 获取两个节点的中间位置
    def get_midpoint(self, node1: Node, node2: Node) -> Tuple[float, float]:
        """Get the midpoint between the position of two nodes.

        Args:
            node1: the name of the first node to get the midpoint from
            node2: the name of the second node to get the midpoint from

        Returns:
            The x and y coordinates of the midpoint between two nodes
        """
        # calculate midpoint
        x = (float(node1.x_pos) + float(node2.x_pos)) / 2
        y = (float(node1.y_pos) + float(node2.y_pos)) / 2

        return x, y

    # 获取当前图中节点连接的所有节点
    def get_current_connected_nodes(self, node: Node) -> List[Node]:
        """Get all of the nodes currently connected to a target node.

        Args:
            node: The name of the node to get the current connections of

        Returns:
            A list of nodes
        """
        return [
            self.current_graph.get_node_from_uuid(n.uuid)
            for n in self.current_graph.neighbors(node)
        ]

    # 获取基础图中和目标节点连接的所有节点
    def get_base_connected_nodes(self, node: Node) -> List[Node]:
        """Get all of the nodes connected to the given node in the base graph.

        Args:
            node: The name of the node to get the current connections of

        Returns:
            A list of nodes
        """
        return [
            self.base_graph.get_node_from_uuid(n.uuid)
            for n in self.base_graph.neighbors(node)
        ]

    # 将当前图转为字典
    def get_current_graph_as_dict(self) -> Dict:
        """Get the current networkx graph for the environment and convert it to
        a dict of dicts.

        Returns:
            The networkx graph as a dict  of dicts
        """
        return nx.to_dict_of_dicts(self.current_graph)

    # 获取当前图中包含属性 key 的所有节点属性字典
    def get_attributes_from_key(self,
                                key: str,
                                key_by_uuid: bool = True) -> dict:
        """Take in a key and return a dictionary.

        The keys are the names of the nodes and the values are the attribute values that are stored for
        that node under the specified key

        :param key: The name of the attribute to extract
        :param key_by_uuid: Use the nodes uuid attribute as the key if True otherwise use the node object itself.

        Returns:
            A dictionary of attributes
        """
        if key_by_uuid:
            return {
                n.uuid: getattr(n, key)
                for n in self.current_graph.get_nodes()
            }
        return {n: getattr(n, key) for n in self.current_graph.get_nodes()}

    # 获取所有节点的 ·脆弱性得分·
    def get_all_vulnerabilities(self) -> dict:
        """Get a dictionary of vulnerability scores."""
        return self.get_attributes_from_key('vulnerability_score')

    # 获取所有节点的 ·孤立状态·
    def get_all_isolation(self) -> dict:
        """Get a dictionary of the isolation status of all the nodes."""
        return self.get_attributes_from_key('isolated')

    # 获取所有节点的 ·受损状态·
    def get_all_node_compromised_states(self) -> dict:
        """Get a dictionary of compromised states."""
        return self.get_attributes_from_key('true_compromised_status')

    # 获取所有蓝方可以观测到的 ·节点受损状态·
    def get_all_node_blue_view_compromised_states(self) -> dict:
        """Get a dictionary of compromised states."""
        return self.get_attributes_from_key('blue_view_compromised_status')

    # 获取所有节点的位置
    def get_all_node_positions(self) -> dict:
        """Get a dictionary of node positions."""
        return self.get_attributes_from_key('node_position', key_by_uuid=False)

    # 获取 未使用的 ·欺骗节点· 的数量
    def get_number_unused_deceptive_nodes(self):
        """Get the current number of unused deceptive nodes."""
        return (
            self.game_mode.blue.action_set.deceptive_nodes.max_number.value -
            self.current_deceptive_nodes)

    def get_current_observation(self) -> np.array:
        # 构建环境观察空间
        """Get the current observation of the environment.

        The composition of the observation space is based on the configuration file used for the scenario.

        Returns:
            numpy array containing the above details
        """
        # number of spaces open for deceptive nodes
        # 这个变量表示当前有多少个欺骗节点尚未被放置。
        # 这些未放置的节点将被考虑到观察空间中，并通过填充相关矩阵来补偿它们。

        open_spaces = self.get_number_unused_deceptive_nodes()

        # Builds the observation space using multiple different metrics from the env

        # Gets the adj matrix for the current graph
        # 节点连接矩阵 (node_connections)：这是当前网络的邻接矩阵，表示节点之间的连接情况。
        # 若观察空间要求包含节点连接信息，则将邻接矩阵填充到考虑未使用的欺骗节点的情况下。
        node_connections = []

        # 隔离状态 (isolated_state)：表示每个节点是否被隔离（用0或1表示）。
        # 同样会考虑未使用的欺骗节点，并进行填充

        # Gets the isolation states for each node
        isolated_state = []
        if self.game_mode.observation_space.node_connections.value:
            node_connections = self.adj_matrix
            # pads the array to account for any missing deceptive nodes that may not have been placed yet
            node_connections = np.pad(node_connections, (0, open_spaces),
                                      'constant')

            # array used to keep track of which nodes are being isolated
            isolated_state = np.asarray(
                list(self.get_attributes_from_key(
                    'isolated').values())).astype(int)

            # pad array to account for deceptive nodes
            isolated_state = np.pad(isolated_state, (0, open_spaces),
                                    'constant')

        # Gets the current safe/compromised status of all of the nodes
        # 受损状态 (compromised_state)：表示节点是否被攻破。这个状态是基于蓝方的视角（即蓝方所能看到的节点状态）。
        compromised_state = []
        if self.game_mode.observation_space.compromised_status.value:
            compromised_state = np.asarray(
                list(
                    self.get_attributes_from_key(
                        'blue_view_compromised_status').values()))
            compromised_state = np.pad(compromised_state, (0, open_spaces),
                                       'constant')
        # Gets the vulnerability score of all of the nodes
        # 漏洞评分 (vulnerabilities)：表示每个节点的漏洞评分，评分越高表示节点越容易被攻破。
        vulnerabilities = []
        if self.game_mode.observation_space.vulnerabilities.value:
            vulnerabilities = np.asarray(
                list(
                    self.get_attributes_from_key(
                        'vulnerability_score').values()))
            vulnerabilities = np.pad(vulnerabilities, (0, open_spaces),
                                     'constant')

        # Gets the average vulnerability of all the nodes
        # 平均漏洞评分 (avg_vuln)：计算所有节点的平均漏洞评分，作为整体网络的一个衡量指标。
        avg_vuln = []
        if self.game_mode.observation_space.average_vulnerability.value:
            all_vuln = self.get_attributes_from_key(
                'vulnerability_score').values()
            avg_vuln = [sum(all_vuln) / len(all_vuln)]

        # Gets the connectivity of the graph, closer to 1 means more edges per node
        # 连通性 (connectivity)：用于度量网络的连通程度，越接近1表示每个节点之间的连接越多。
        connectivity = []
        if self.game_mode.observation_space.graph_connectivity.value:
            connectivity = [self.connectivity]

        # Gets the attacks that the blue agent detected
        # 攻击节点 (attacking_nodes) 和 被攻击节点 (attacked_nodes)
        # 分别表示当前已知的攻击行为的发起节点和受攻击的目标节点。
        attacking_nodes = []
        attacked_nodes = []
        if (self.game_mode.observation_space.attacking_nodes.value
                or self.game_mode.observation_space.attacked_nodes.value):
            attacking = {n: 0 for n in self.current_graph.get_nodes()}
            attacked = {n: 0 for n in self.current_graph.get_nodes()}
            for node_set in self.detected_attacks:
                if node_set[0] is not None:
                    # extract the attacking node (as long as the attacking node is not None)
                    attacking[node_set[0]] = 1
                # extract the node that was attacked
                attacked[node_set[1]] = 1
            if self.game_mode.observation_space.attacking_nodes.value:
                # attacking nodes
                attacking_nodes = list(attacking.values())
                attacking_nodes = np.pad(attacking_nodes, (0, open_spaces),
                                         'constant')
            if self.game_mode.observation_space.attacked_nodes.value:
                # nodes attacked
                attacked_nodes = list(attacked.values())
                attacked_nodes = np.pad(attacked_nodes, (0, open_spaces),
                                        'constant')

        # Gets the locations of any special nodes in the network (entry nodes and high value nodes)
        # 特殊节点（入口节点、高价值节点和目标节点）的位置：
        entry_nodes = []
        nodes = []
        target_nodes = []

        # 入口节点 (entry_nodes)
        if self.game_mode.observation_space.special_nodes.value:
            # gets the entry nodes
            entry_nodes = {n: 0 for n in self.current_graph.get_nodes()}
            for n in self.current_graph.entry_nodes:
                entry_nodes[n] = 1
            entry_nodes = list(entry_nodes.values())
            entry_nodes = np.pad(entry_nodes, (0, open_spaces), 'constant')

            # 目标节点 (target_nodes)
            if self.game_mode.game_rules.blue_loss_condition.target_node_lost.value:
                # gets the target node
                target_nodes = {n: 0 for n in self.current_graph.get_nodes()}
                target_nodes[self.get_target_node()] = 1
                target_nodes = list(target_nodes.values())
                target_nodes = np.pad(target_nodes, (0, open_spaces),
                                      'constant')

            # 高价值节点 (nodes)、
            if self.game_mode.game_rules.blue_loss_condition.high_value_node_lost.value:
                # gets the high value node nodes
                nodes = {n: 0 for n in self.current_graph.get_nodes()}

                # set high value nodes to 1
                for node in self.current_graph.high_value_nodes:
                    nodes[node] = 1

                nodes = list(nodes.values())
                nodes = np.pad(nodes, (0, open_spaces), 'constant')

        # gets the skill of the red agent
        # 蓝方观测到的 红方代理的技能
        # 技能 (skill)：表示红方代理的技能水平，可能会影响蓝方代理的决策。
        skill = []
        if self.game_mode.observation_space.red_agent_skill.value:
            skill = [self.game_mode.red.agent_attack.skill.value.value]

        # combines all of the env observations together to create the observation that the blue agent gets
        # 所有上述信息会被组合到一起，形成最终的观察空间，这是蓝方代理根据当前环境状态做出决策的主要依据。
        obs = np.concatenate(
            (
                node_connections,
                isolated_state,
                compromised_state,
                vulnerabilities,
                avg_vuln,
                connectivity,
                attacking_nodes,
                attacked_nodes,
                entry_nodes,
                nodes,
                target_nodes,
                skill,
            ),
            axis=None,
            dtype=np.float32,
        )
        return obs

    def get_observation_size_base(self, with_feather: bool) -> int:
        # 目的: 根据当前游戏模式下开启或关闭的特性，计算环境的观察空间的大小。
        # 通过这些方法，系统能够动态计算观察空间的大小，确保蓝方代理接收到的信息量与当前游戏模式下开启的特性相符。
        # 不同的配置可能会产生不同大小的观察空间，确保在游戏中能够灵活应对不同的场景和策略需求。
        """Get the size of the observation space.

        This is based on the game_mode that are turned on/off.

        Returns:
            The size of the observation space
        """
        # gets the max number of nodes in the env (including deceptive nodes)
        # 如果 with_feather 为 True，节点连接矩阵的大小被固定为500。
        # 否则，矩阵的大小为 max_number_of_nodes * max_number_of_nodes，即所有可能的节点之间的连接情况。

        observation_size = 0
        max_number_of_nodes = self.get_total_num_nodes()
        if with_feather:
            node_connections = 500
        else:
            node_connections = max_number_of_nodes * max_number_of_nodes

        # calculate the size of the observation space
        # the size depends on what observations are turned on/off in the config file
        # 如果节点连接信息被启用，则将节点连接矩阵的大小和隔离节点的大小加到观察空间大小中。
        if self.game_mode.observation_space.node_connections.value:
            # add node connections to observation size
            observation_size += node_connections
            # add isolated nodes to observation size
            observation_size += max_number_of_nodes
        # 节点受损信息
        if self.game_mode.observation_space.compromised_status.value:
            observation_size += max_number_of_nodes
        # 节点脆弱性值
        if self.game_mode.observation_space.vulnerabilities.value:
            observation_size += max_number_of_nodes
        if self.game_mode.observation_space.average_vulnerability.value:
            observation_size += 1
        # 节点连通性值
        if self.game_mode.observation_space.graph_connectivity.value:
            observation_size += 1
        # 正在攻击的节点和已经攻击的节点
        if self.game_mode.observation_space.attacking_nodes.value:
            observation_size += max_number_of_nodes
        if self.game_mode.observation_space.attacked_nodes.value:
            observation_size += max_number_of_nodes
        # 包括特殊节点（如入口节点、高价值节点、目标节点）的信息。
        # 若配置文件中启用了这些特性，则将其相应的大小加到观察空间中。
        if self.game_mode.observation_space.special_nodes.value:
            observation_size += max_number_of_nodes
            if self.game_mode.game_rules.blue_loss_condition.target_node_lost.value:
                observation_size += max_number_of_nodes
            if self.game_mode.game_rules.blue_loss_condition.high_value_node_lost.value:
                observation_size += max_number_of_nodes
        # 红方代理技能:
        if self.game_mode.observation_space.red_agent_skill.value:
            observation_size += 1
        return observation_size

    def get_observation_size(self) -> int:
        """Use base observation size calculator with feather switched off.

        目的: 使用基础的观察空间大小计算器，并默认 with_feather 为 False。
        """
        return self.get_observation_size_base(False)

    # SETTERS
    # The following block of code contains the setters for the network_interface.
    # Setters are a type of method that update or change a class attribute
    # 这段代码涉及网络安全模拟环境中的几项关键功能，包括初始化欺骗节点、初始化边映射、以及更新记录的攻击。

    def initialise_deceptive_nodes(self):
        """Create a separate list of :class:

        `~cyberattacksim.networks.node.Node` objects take represent deceptive
        nodes.

        目的: 初始化一组欺骗节点，这些节点是用于迷惑红方攻击者的虚假节点。
        """
        self.available_deceptive_nodes: List[Node] = []
        for i in range(self.game_mode.blue.action_set.deceptive_nodes.
                       max_number.value):
            name = 'd' + str(i)
            deceptive_node = Node(
                name=name,
                vulnerability=self.current_graph.
                _generate_random_vulnerability(),
            )
            deceptive_node.deceptive_node = True
            self.available_deceptive_nodes.append(deceptive_node)

    def initialise_edge_map(self):
        """Create a lookup that maps a unique integer key to an networkx edge
        (node pair).

        目的: 创建一个边映射 (edge_map)，将唯一整数键映射到网络中的边（即节点对）。
        """
        self.edge_map = {}
        edges: List[Tuple[Node, Node]] = self.current_graph.edges
        for i, node_pair in enumerate(edges):
            self.edge_map[i] = node_pair

    def update_stored_attacks(self, attacking_nodes: List[Node],
                              target_nodes: List[Node], success: List[bool]):
        """Update this turns current attacks.
        目的: 更新当前回合的攻击信息，包括记录所有成功或失败的攻击，并判断蓝方是否检测到这些攻击。

        This function collects all of the failed attacks and stores them for the
        blue agent to use in their action decision

        Args:
            attacking_nodes: Nodes red has attacked from， 红方发起攻击的节点列表。
            target_nodes: Nodes red is attacking，红方攻击的目标节点列表。
            success: If the attacks were a success or not， 布尔列表，表示每次攻击是否成功。


        - 遍历攻击节点、目标节点和攻击成功标志的组合，依次处理每个攻击事件。

        - 根据攻击目标是否为欺骗节点以及攻击是否成功，分别处理：
           - 对于欺骗节点，依据不同的成功与失败情况，蓝方有一定几率检测到攻击。
           - 对于普通节点，如果攻击失败并且配置允许，蓝方可能会检测到攻击；如果攻击成功，蓝方同样可能基于节点的已知或未知受损状态检测到攻击。

        - 所有已检测到的攻击都会被添加到 self.detected_attacks 列表中，而所有攻击（包括未检测到的）都会被添加到 self.true_attacks 列表中。

        """
        # Runs through all the nodes attacked
        for attacking_node, target_node, success in zip(
                attacking_nodes, target_nodes, success):
            # Deceptive nodes have a different chance of detecting attacks
            if target_node.deceptive_node:
                if success:
                    # chance of seeing the attack if the attack succeeded
                    if (100 * self.game_mode.blue.attack_discovery.
                            succeeded_attacks_known_compromise.chance.
                            deceptive_node.value > random.randint(0, 99)):
                        self.detected_attacks.append(
                            [attacking_node, target_node])
                else:
                    # chance of seeing the attack if the attack fails
                    if (100 * self.game_mode.blue.attack_discovery.
                            failed_attacks.chance.deceptive_node.value >
                            random.randint(0, 99)):
                        self.detected_attacks.append(
                            [attacking_node, target_node])
            else:
                # If the attack did not succeed
                if not success:
                    if self.game_mode.blue.attack_discovery.failed_attacks.use.value:
                        if (100 * self.game_mode.blue.attack_discovery.
                                failed_attacks.chance.standard_node.value >
                                random.randint(0, 99)):
                            # Adds the attack to the list of current attacks for this turn
                            self.detected_attacks.append(
                                [attacking_node, target_node])
                else:
                    # If the attack succeeded and the blue agent detected it
                    if target_node.blue_view_compromised_status == 1:
                        if self.game_mode.blue.attack_discovery.succeeded_attacks_known_compromise.use.value:
                            if (self.game_mode.blue.attack_discovery.
                                    succeeded_attacks_known_compromise.chance.
                                    standard_node.value > random.randint(
                                        0, 99)):
                                self.detected_attacks.append(
                                    [attacking_node, target_node])
                    else:
                        # If the attack succeeded but blue did not detect it
                        if self.game_mode.blue.attack_discovery.succeeded_attacks_unknown_compromise.use.value:
                            if (100 * self.game_mode.blue.attack_discovery.
                                    succeeded_attacks_unknown_compromise.
                                    chance.standard_node.value >
                                    random.randint(0, 99)):
                                self.detected_attacks.append(
                                    [attacking_node, target_node])
            # Also compiles a list of all the attacks even those that blue did not "see"
            self.true_attacks.append([attacking_node, target_node])

    # RESET METHODS
    # The following block of code contains the methods that are used to reset some portion of the network interface
    # 这段代码提供了两个关键的方法：reset_stored_attacks 和 reset。这些方法用于在每个时间步重置攻击记录，并将网络恢复到默认状态。

    def reset_stored_attacks(self):
        """Reset the attacks list.
        目的: 在每个时间步调用此方法，以确保 true_attacks 和 detected_attacks 列表只包含当前时间步的攻击。

        This needs to be called every timestep to ensure that only the current
        attacks are contained.
        """
        #  被重置为空列表，清除所有记录的攻击。
        self.true_attacks = []
        #  也被重置为空列表，确保在每个时间步开始时，只有当前回合检测到的攻击会被记录。
        self.detected_attacks: List[List[Node]] = []

    def reset(self):
        """Reset the network back to its default state.
        目的: 重置网络回到其默认状态。这通常在每次游戏或模拟的重置时调用。

        reset 方法将整个网络状态重置到其初始状态，包括图的结构、节点的状态和攻击记录的清空等。这对于游戏或模拟的每次重新开始都至关重要，以确保公平和一致的初始条件。


        操作：
            - 红方位置重置: self.red_current_location 被设置为 None，意味着红方的当前位置被重置。
            - 图的重置:
                - 使用深拷贝 (copy.deepcopy) 重置当前图 (self.current_graph) 和基础图 (self.base_graph) 为初始状态 (self.initial_base_graph)。
            - 边映射和欺骗节点初始化:
                - 调用 initialise_edge_map 方法重新初始化边映射，以适应新重置的图。
                - 调用 initialise_deceptive_nodes 方法重新初始化欺骗节点。
            - 欺骗节点的指针和状态重置:
                - self.deceptive_node_pointer 被设置为 0，表示下一个将被使用的欺骗节点的索引。
                - self.current_deceptive_nodes 被设置为 0，表示当前使用的欺骗节点数量。
                - self.reached_max_deceptive_nodes 被设置为 False，表示尚未达到最大欺骗节点数量。
            - 攻击记录重置:
                - 调用 reset_stored_attacks 方法，清除所有先前的攻击记录。
            - 邻接矩阵更新:
                - 使用 networkx 库的 to_numpy_array 方法，将当前图的邻接矩阵 (adj_matrix) 更新为 NumPy 数组形式。
            - 基于配置的图调整:
                - 如果 self.game_mode.on_reset.choose_new_entry_nodes.value 为真，调用 self.current_graph.reset_random_entry_nodes() 方法随机选择新的入口节点。
                - 如果 self.game_mode.on_reset.choose_new_high_value_nodes.value 为真，调用 self.current_graph.reset_random_high_value_nodes() 方法随机选择新的高价值节点。
                - 如果 self.game_mode.on_reset.randomise_vulnerabilities.value 为真，调用 self.current_graph.reset_random_vulnerabilities() 方法随机化节点的漏洞。
        """
        # red location
        # 红方位置重置: self.red_current_location 被设置为 None，意味着红方的当前位置被重置。

        self.red_current_location = None

        # resets the network graph from the saved base graph
        self.current_graph = copy.deepcopy(self.initial_base_graph)
        self.base_graph = copy.deepcopy(self.initial_base_graph)

        # resets the edge map to match the new current graph
        self.initialise_edge_map()
        self.initialise_deceptive_nodes()

        # pointers and helpers for deceptive nodes are reset
        self.deceptive_node_pointer = 0
        self.current_deceptive_nodes = 0
        self.reached_max_deceptive_nodes = False

        # any previous attacks are removed
        # reset_stored_attacks 方法确保每个时间步开始时，攻击记录被清空，只保留当前时间步的攻击数据。
        self.reset_stored_attacks()

        # updates the stored adj matrix
        self.adj_matrix = nx.to_numpy_array(self.current_graph)

        if self.game_mode.on_reset.choose_new_entry_nodes.value:
            self.current_graph.reset_random_entry_nodes()

        # set high value nodes
        if self.game_mode.on_reset.choose_new_high_value_nodes.value:
            self.current_graph.reset_random_high_value_nodes()

        if self.game_mode.on_reset.randomise_vulnerabilities.value:
            self.current_graph.reset_random_vulnerabilities()

    # STANDARD METHODS
    # The following block of code contains the standard methods that are used to interact with the network interface in
    # in some complex way.

    # 下面的代码实现了一个网络攻击模拟环境，其中包括红方和蓝方的角色。红方代表攻击者，蓝方代表防御者。
    # 代码中定义的方法用于管理网络中的节点、模拟攻击和防御操作，以及处理节点间的连接和状态更新。

    def __push_red(self):
        """Remove red from the target node and move to a new location.

        If the blue agent patches the node that the red agent is in the red
        agent will be pushed to a connected compromised node. If there are none
        then the red agent will be pushed out of the network

        私有方法用于在蓝方修补（即防御）当前红方所在的节点时，将红方从该节点移除，并移动到另一个已被攻破的节点。
        如果没有可移到的节点，红方将被移出网络。

        过程：
            获取与红方当前所在节点相连的所有节点。
            随机打乱这些节点的顺序，以随机选择一个节点。
            如果找到已被攻破的节点，红方将移动到该节点。
            如果没有找到已被攻破的节点，红方将被移出网络（red_current_location = None）。
        """
        connected = self.get_current_connected_nodes(self.red_current_location)
        # Randomises the order of the nodes to pick a random one
        random.shuffle(connected)
        done = False
        for node in connected:
            if node.true_compromised_status == 1:
                self.red_current_location = node
                done = True
                break
        if done is False:
            # If there were no nodes then the agent is removed from the network
            self.red_current_location = None

    def add_deceptive_node(self, node1: Node,
                           node2: Node) -> Union[bool, Node]:
        """Add a deceptive node into the network.

        The deceptive node will sit between two actual nodes and act as a normal node in all
        regards other than the fact that it give more information when it is attacked

        这个方法用于在两个节点之间添加一个欺骗节点。欺骗节点的作用是，当攻击者攻击它时，
        它会提供更多的信息，同时在网络中表现得像一个正常节点。

        过程：
            检查在这两个节点之间是否存在一条边。
            如果红方在一个欺骗节点中，则将红方移出该节点。
            在两个节点之间插入欺骗节点，更新基础图（base_graph）和当前图（current_graph）。
            如果节点处于隔离状态，则会根据其连接状态相应地添加连接。
            更新节点位置和当前的邻接矩阵，并管理欺骗节点的计数器。

        Args:
            node1: Name of the first node to connect to the deceptive node
            node2: Name of the second to connect to the deceptive node

        Returns:
            False if failed, the name of the new node if succeeded
        """
        # Check if there exists an edge between the two nodes
        if self.base_graph.has_edge(node1, node2):
            # If the red agent is in the deceptive node at its old position, push it out to a surrounding node
            if (self.red_current_location is not None
                    and self.red_current_location.deceptive_node):
                self.__push_red()

            # get the new node and add the new node
            deceptive_node = self.available_deceptive_nodes[
                self.deceptive_node_pointer]

            # If the node is already in use, remove it from the base graph
            if self.base_graph.has_node(deceptive_node):
                self.__remove_node_yt(deceptive_node, self.base_graph)

            # inserts a new node on the base graph
            # self.__insert_node_between(copy.deepcopy(deceptive_node), node1, node2, self.base_graph)
            self.__insert_node_between(deceptive_node, node1, node2,
                                       self.base_graph)

            # If the node is already in use, remove it from the current graph
            if self.current_graph.has_node(deceptive_node):
                self.__remove_node_yt(deceptive_node, self.current_graph)

            # check the isolation status of the nodes
            if not node1.isolated and not node2.isolated:
                # neither are isolated: use the insert between method to insert the new node on the current graph
                self.__insert_node_between(deceptive_node, node1, node2,
                                           self.current_graph)
            elif not node1.isolated:
                # one node is isolated: add the node to the graph and add a single edge to the non-isolated node
                self.current_graph.add_node(deceptive_node)
                self.current_graph.add_edge(node1, deceptive_node)
            elif not node2.isolated:
                # one node is isolated: add the node to the graph and add a single edge to the non-isolated node
                self.current_graph.add_node(deceptive_node)
                self.current_graph.add_edge(node2, deceptive_node)
            else:
                # both nodes are isolated: add the node to the graph
                self.current_graph.add_node(deceptive_node)

            # increase the pointer to point to the next element in the list (the next deceptive node to use)
            self.deceptive_node_pointer += 1
            if not self.reached_max_deceptive_nodes:
                # checks if all the deceptive nodes are in play
                self.current_deceptive_nodes += 1
            if (self.deceptive_node_pointer == self.game_mode.blue.action_set.
                    deceptive_nodes.max_number.value):
                self.deceptive_node_pointer = 0
            if (self.current_deceptive_nodes == self.game_mode.blue.action_set.
                    deceptive_nodes.max_number.value):
                self.reached_max_deceptive_nodes = True
            if self.game_mode.blue.action_set.deceptive_nodes.new_node_on_relocate.value:
                # TODO: check if the following can be replaced by a node reset method
                deceptive_node.vulnerability = (
                    self.current_graph._generate_random_vulnerability())
                deceptive_node.true_compromised_status = 0
                deceptive_node.blue_view_compromised_status = 0
                deceptive_node.node_position = [0, 0]
                deceptive_node.deceptive_node = True
                deceptive_node.blue_knows_intrusion = False
                deceptive_node.isolated = False

            # updates the position of the node based on its new location
            deceptive_node.node_position = self.get_midpoint(node1, node2)
            # updates the current adjacency matrix
            self.adj_matrix = nx.to_numpy_array(self.current_graph)
            return deceptive_node
        else:
            # If no edge return false as the deceptive node cannot be put here
            return False

    def __remove_node_yt(self, node: Node, graph: nx.Graph) -> None:
        """Remove a node from a graph. 于从图中移除一个节点，包括它的所有连接。

        Removing a node removes all connections to and from that node

        过程：
            - 先将该节点的连接重新连接到其他节点上，然后移除该节点。
            - 重新建立连接，确保移除节点后的图仍然保持正确的路径。
        Args:
            node: the name of the node to remove
            graph: the networkx graph to remove the node from
        """
        self.reconnect_node(
            node
        )  # TODO: check this is correct. This is a workaround to reattach connections to the node to delete so as to establish
        # the correct paths to reform.

        # extracts the 0th element from a list where a variable "to_remove" has been removed
        extract_connections = lambda x, to_remove: list(  # noqa
            filter(lambda z: z != to_remove, x)  # noqa
        )[0]  # noqa

        # gets all of the edges from a node
        links = graph.edges(node)

        # gets the connections to this node using the extract_connections lambda function
        connections = [extract_connections(x, node) for x in links]
        if len(connections) >= 2:
            # generates the new connections
            new_links = list(itertools.combinations(connections, 2))
            # adds the new edges
            graph.add_edges_from(new_links)
        # removes the old node
        graph.remove_node(node)

    def __insert_node_between(self, new_node: Node, node1: Node, node2: Node,
                              graph: Network) -> None:
        """Insert a node in between two nodes. 用于在两个现有节点之间插入一个新节点。

        过程：
            - 移除两个节点之间的边。
            - 将新节点添加到图中，并在新节点与两个节点之间创建边。

        Args:
            new_node: the name of the new node
            node1: the name of the first node the new node will be connected to
            node2: the name of the second node the new node will be connected to
            graph: the networkx graph to add the new node to
        """
        # removes the old edge between the nodes
        if graph.has_edge(node1, node2):
            graph.remove_edge(node1, node2)
        graph.add_node(new_node)
        # adds the new node in and updates the edges
        graph.add_edge(node1, new_node)
        graph.add_edge(new_node, node2)

    def isolate_node(self, node: Node):
        """Isolate a node (disable all of the nodes connections).
        用于隔离一个节点，禁用它的所有连接。

        过程：
            - 将节点标记为隔离状态。
            - 从当前图中移除该节点与其他节点之间的所有边。

        Args:
            node: the node to disable the connections of
        """
        node.isolated = True
        current_connections = self.get_current_connected_nodes(node)
        for cn in current_connections:
            self.current_graph.remove_edge(node, cn)

        # self.adj_matrix = nx.to_numpy_array(self.current_graph)

    def reconnect_node(self, node: Node):
        """Re-enable any connections that may have previously been disabled.
        这个方法用于重新启用之前被禁用的节点连接。

        过程：
            - 如果节点被标记为隔离，则取消隔离状态。
            - 根据基础图中的连接状态，重新建立该节点与其他节点的连接。

        Args:
            node: the node to re-enable
        """
        if node.isolated:
            node.isolated = False
            base_connections = self.get_base_connected_nodes(node)
            for bn in base_connections:
                cn = self.current_graph.get_node_from_uuid(bn.uuid)
                if (
                        not cn.isolated
                ):  # ensure a different isolated node cannot be reconnected
                    self.current_graph.add_edge(node, cn)

            # self.adj_matrix = nx.to_numpy_array(self.current_graph)

    def attack_node(
        self,
        node: Node,
        skill: float = 0.5,
        use_skill: bool = False,
        use_vulnerability: bool = False,
        guarantee: bool = False,
    ) -> bool:
        """Attack a target node.

        用于尝试攻击一个节点，成功与否取决于攻击者的技能、节点的漏洞以及一定的随机因素。

        过程：
            - 根据技能和漏洞计算攻击得分，得分越高，攻击成功的可能性越大。
            - 根据得分和随机数来判断攻击是否成功，如果成功，则更新节点的被攻破状态。

        Uses a random chance to succeed that is modified by the skill of the attack and the
        vulnerability of the node. Both the skill and the vulnerability can be toggled to either be used or not

        Args:
            node: The name of the node to target
            skill: The skill of the attacker
            use_skill: A boolean value that is used to determine if skill is used in the calculation to check if the
                       attack succeeds
            use_vulnerability: A boolean value that is used to determine if vulnerability is used in the calculation to
                               check if the attack succeeds
            guarantee: If True then attack automatically succeeds

        Returns:
            A boolean value that represents if the attack succeeded or not
        """
        # check if vulnerability and score are being used. If they are not then select a value
        if use_vulnerability:
            defence = 1 - node.vulnerability_score
        else:
            defence = 0
        if not use_skill:
            skill = 1

        # calculate the attack score, the higher the score the more likely the attack is to succeed
        attack_score = ((skill * skill) / (skill + defence)) * 100
        # check if the attack hits based on the attack score
        if guarantee or (attack_score > random.randint(0, 100)):
            node.true_compromised_status = 1
            self.__immediate_attempt_view_update(node)
            return True
        else:
            return False

    def make_node_safe(self, node: Node):
        """Make the state for a given node safe. 用于将一个节点标记为安全状态。

        过程：
            - 重置节点的被攻破状态。
            - 如果红方在该节点，则将其移出该节点。


        Args:
            node: the node to make safe
        """
        node.true_compromised_status = 0
        node.blue_view_compromised_status = 0
        if self.red_current_location == node:
            # If the red agent is in the node that just got made safe then the red agent needs to be pushed back
            self.__push_red()
        node.blue_knows_intrusion = False

    def __immediate_attempt_view_update(self,
                                        node: Node,
                                        chance: float = None):
        """Attempt to update the view of a specific node for the blue agent.
        用于尝试更新蓝方对特定节点的视图，反映其当前的被攻破状态。

        过程：
            如果蓝方已知晓入侵情况，则更新视图。
            否则，根据随机机会判断是否发现入侵。

        There is a chance that intrusions will not be detected.

        :param node: the node to try and update the view for
        """
        if node.blue_knows_intrusion is True:
            # if we have seen the intrusion before we don't want to forget about it
            node.blue_view_compromised_status = node.true_compromised_status
        if node.true_compromised_status == 1:
            if chance is None and (random.randint(
                    0, 99) < self.game_mode.blue.intrusion_discovery_chance.
                                   immediate.standard_node.value * 100
                                   or node.deceptive_node):
                node.blue_view_compromised_status = node.true_compromised_status
                # remember this intrusion so we don't forget about it
                node.blue_knows_intrusion = True
            elif chance is not None and (random.randint(0, 99) < chance * 100):
                node.blue_view_compromised_status = node.true_compromised_status

        else:
            node.blue_view_compromised_status = node.true_compromised_status

    def scan_node(self, node: Node) -> None:
        """Scan a target node to determine compromise based on the chance of
        discovery of compromise.

        用于扫描一个节点以确定其是否被攻破，并相应地更新蓝方的视图。

        过程：
            如果蓝方已知晓入侵情况，则更新视图。
            否则，根据随机机会判断是否发现入侵。
        Args:
            node: The node to be scanned
        """
        if node.blue_knows_intrusion:
            node.blue_view_compromised_status = 1
        elif node.true_compromised_status == 1:
            if (random.randint(
                    0, 99) < self.game_mode.blue.intrusion_discovery_chance.
                    on_scan.standard_node.value * 100 or node.deceptive_node):
                node.blue_knows_intrusion = True
                node.blue_view_compromised_status = 1

    def save_json(self, data_dict: dict, ts: int) -> None:
        """Save a given dictionary to a json file. 用于将给定的数据字典保存为JSON文件。

        过程：
            生成一个时间戳并创建文件名。
            将数据字典保存为JSON文件。
        Args:
            data_dict: Data to save to the json file
            ts: The current timestamp of the data
        """
        now = datetime.now()
        time_stamp = str(datetime.timestamp(now)).replace('.', '')
        name = ('cyberattacksim/envs/helpers/json_timesteps/output_' +
                str(ts) + '_' + str(time_stamp) + '.json')
        with open(name, 'w+') as json_file:
            json.dump(data_dict, json_file)

    def create_json_time_step(self) -> dict:
        """Create a dictionary that contains the current state of the
        environment and returns it.

        用于创建一个包含当前环境状态的字典并返回。

        过程：
            从当前图中获取边信息以及节点的状态和漏洞信息。
            将这些信息组合成一个字典并返回。


        Returns:
            A dictionary containing the node connections, states and vulnerability scores
        """
        convert_str = lambda x: str(x) if x is not None else None  # noqa

        # Gets the edges from the networkx object
        connections = [
            list(map(convert_str, list(e))) for e in self.current_graph.edges
        ]
        # Gets the vulnerability and compromised status
        node_states = self.get_all_node_compromised_states()
        node_vulnerabilities = self.get_all_vulnerabilities()

        # Combines the features into a defaultdict and then returns a dictionary
        combined_features = defaultdict(list)

        for feature in (node_states, node_vulnerabilities):
            for key, value in feature.items():
                combined_features[key].append(value)

        current_state_dict = {
            'edges': connections,
            'features': combined_features
        }

        return current_state_dict
