from typing import Tuple

from cyberattacksim.envs.generic.core.blue_action_set import BlueActionSet
from cyberattacksim.envs.generic.core.network_interface import NetworkInterface
from cyberattacksim.networks.node import Node

# 这个代码定义了 BlueInterface 类，它继承自 BlueActionSet，为蓝方代理提供了一个接口，使其能够在网络环境中执行各种动作。
# 这些动作被分为三大类：标准动作、欺骗动作和全局动作。
# BlueInterface 通过 perform_action 方法来执行这些动作，并根据输入的动作编号决定具体执行哪个动作。


class BlueInterface(BlueActionSet):
    """The interface used by the Blue Agents to act within the environment."""

    def __init__(self, network_interface: NetworkInterface):
        """Initialise the blue interface.

        Args:
            network_interface: Object from the NetworkInterface class
        """
        super().__init__(network_interface)

        # action_dict 保存了标准动作，每个动作都与一个编号关联。
        # deceptive_actions 记录了欺骗动作的数量，这个数量与网络中边的数量相关。
        # global_action_dict 保存了全局动作，同样与编号关联。
        # number_of_actions 和 number_global_action 分别记录了标准动作和全局动作的数量。

        # standard actions (apply to a single node)
        self.action_dict = {}
        action_number = 0
        self.deceptive_actions = 0
        # all of the actions that blue can do
        if self.network_interface.game_mode.blue.action_set.reduce_vulnerability.value:
            # Checks if the action is enabled in the settings file
            self.action_dict[action_number] = self.reduce_node_vulnerability
            action_number += 1
        if self.network_interface.game_mode.blue.action_set.restore_node.value:
            self.action_dict[action_number] = self.restore_node
            action_number += 1
        if self.network_interface.game_mode.blue.action_set.make_node_safe.use.value:
            self.action_dict[action_number] = self.make_safe_node
            action_number += 1
        if self.network_interface.game_mode.blue.action_set.isolate_node.value:
            self.action_dict[action_number] = self.isolate_node
            action_number += 1
        if self.network_interface.game_mode.blue.action_set.reconnect_node.value:
            self.action_dict[action_number] = self.reconnect_node
            action_number += 1

        # deceptive actions -> since the number of edges is not equal to the number of nodes this has to be done
        # separately
        if self.network_interface.game_mode.blue.action_set.deceptive_nodes.use.value:
            self.deceptive_actions = self.network_interface.base_graph.number_of_edges(
            )

        # global actions (don't apply to a single node)
        self.global_action_dict = {}
        global_action_number = 0
        if self.network_interface.game_mode.blue.action_set.scan.value:
            # scans all of the nodes in the network
            self.global_action_dict[global_action_number] = self.scan_all_nodes
            global_action_number += 1
        if self.network_interface.game_mode.blue.action_set.do_nothing.value:
            # does nothing
            self.global_action_dict[global_action_number] = self.do_nothing
            global_action_number += 1
        self.number_of_actions = action_number
        self.number_global_action = global_action_number

    def perform_action(self, action: int) -> Tuple[str, Node]:
        """Perform an action within the environment.

        perform_action 方法根据传入的 action 编号来执行相应的动作。

        - 如果编号超出动作范围，则执行 do_nothing。
        - 如果编号在欺骗动作范围内，则执行对应的欺骗动作。
        - 如果编号对应全局动作，则执行全局动作。
        - 否则，执行标准动作，标准动作会应用到特定的节点上。

        执行流程:
        - 检查 action 是否超出动作范围，如果超出，则执行 do_nothing。
        - 检查 action 是否属于欺骗动作，如果是，则执行相应的欺骗动作。
        - 检查 action 是否属于全局动作，如果是，则执行相应的全局动作。
        - 如果都不是，则将 action 映射到一个标准动作，并将该动作应用于特定的节点上。

        Takes in an action number and then maps this to the correct action to perform. There are 3 different item_types of
        actions:
            - standard actions
            - deceptive actions
            - global actions

        --standard actions--
        Standard actions are actions that can apply to all nodes. For each standard action there are n actions (where n
        is the number of nodes in the network). An example of this action would be to isolate a node. The agent has to
        pick the isolate action and then the node it is being applied to.

        --deceptive actions--
        Actions relating to deceptive nodes. Since the number of deceptive actions relate to the edges not the nodes
        (see deceptive nodes for more info), the deceptive actions cannot come under the standard actions. An example
        would be to place a deceptive node. The deceptive nodes can only be placed on an edge so the agent has to pick
        the "place deceptive node" action and then the edge to place it on.

        --global actions--
        Global actions are actions where the agent does not need to pick any sub action other than the action. For
        example an action that applies to all nodes so the agent does not need to pick a specific node to apply the
        action to. "Do nothing" is an example of a global action as there is no secondary choice to be made.


        The function also maps any actions outside of the action space to the "do nothing" action.

        Order of operations:
        1- check if the action is inside the action space --> perform "do nothing"
        2- check if the action is a deceptive action --> perform action
        3- check if the action is a global action --> perform action
        4- perform the standard action

        Args:
            action: the action to perform

        Returns:
            The action that has been taken
            The node the action was performed on
        """
        if action >= self.get_number_of_actions():
            blue_action, blue_node = self.do_nothing()
        elif action < self.deceptive_actions:
            # use a deceptive action
            blue_action, blue_node = self.add_deceptive_node(action)
        # global actions
        else:
            action = action - self.deceptive_actions
            # global actions
            if action < self.number_global_action:
                blue_action, blue_node = self.global_action_dict[action]()
            else:
                # standard actions
                action = action - self.number_global_action
                action_node_number = int(action / self.number_of_actions)

                if (action_node_number >=
                        self.network_interface.current_graph.number_of_nodes()
                    ):
                    blue_action, blue_node = self.do_nothing()
                else:
                    nodes = self.network_interface.current_graph.get_nodes()
                    action_node = sorted(nodes)[action_node_number]
                    action_taken = int(action % self.number_of_actions)

                    blue_action, blue_node = self.action_dict[action_taken](
                        action_node)

        return blue_action, blue_node

    def get_number_of_actions(self) -> int:
        """Get the number of actions that this blue agent can perform.

        这个方法返回蓝方代理可以执行的总动作数量，包括标准动作、欺骗动作和全局动作。
        总数是标准动作数量乘以节点数量，再加上全局动作数量和欺骗动作数量。

        There are three item_types of actions:
            - global actions (apply to all nodes) - need 1 action space
            - deceptive actions (Add new nodes to environment)
            - standard actions (apply to a single node) - need 2 action space (action and node to perform on)

        Returns:
            The number of actions that this agent can perform
        """
        return ((self.number_of_actions *
                 self.network_interface.get_total_num_nodes()) +
                self.number_global_action + self.deceptive_actions)
