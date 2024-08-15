"""An interface to the parent red agent that selects what actions it wants to
use base on the settings and then uses a dictionary to call these actions."""

from typing import Dict, List, Union

from cyberattacksim.envs.generic.core.network_interface import NetworkInterface
from cyberattacksim.envs.generic.core.red_action_set import RedActionSet


class RedInterface(RedActionSet):
    """这段代码定义了一个名为 RedInterface 的类，它继承自 RedActionSet， 并为红方代理（Red
    Agents）提供了与模拟环境进行交互的接口。 红方代理在每个回合都会基于配置文件中的设置选择并执行某个动作。

    The interface used by the Red Agents to act within the environment.
    """

    def __init__(self, network_interface: NetworkInterface):
        """Initialise the red interface.

        Args:
            network_interface: Object from the NetworkInterface class
        """
        self.network_interface = network_interface
        self.non_attacking_actions = ['do_nothing', 'random_move']

        # self.action_dict 是一个字典，用于将动作编号与相应的动作方法关联。
        # action_set 是一个动作编号的列表，用于记录所有可用的动作。
        # probabilities_set 是一个列表，存储每个动作对应的执行概率。
        # action_number 用于跟踪动作的编号。

        self.action_dict = {}
        action_set = []
        probabilities_set = []
        action_number = 0

        # 代码通过一系列 if 语句来检查配置文件中的设置，决定哪些动作是启用的，
        # 并将其添加到 self.action_dict 中，同时记录对应的执行概率。
        # 如果 spread 动作在配置文件中被启用，则将该动作方法 self.spread 添加到 self.action_dict 中，并记录它的编号和执行概率。
        # 其他动作（如 random_infect, basic_attack, do_nothing, move）的处理方式类似。

        # Goes through the actions that the red agent can perform
        if self.network_interface.game_mode.red.action_set.spread.use.value:
            # If the action is enabled in the settings files then add to list of possible actions
            self.action_dict[action_number] = self.spread
            action_set.append(action_number)
            # also gets the weight for the action (likelihood action is performed) from the settings file
            probabilities_set.append(self.network_interface.game_mode.red.
                                     action_set.spread.likelihood.value)
            action_number += 1
        if self.network_interface.game_mode.red.action_set.random_infect.use.value:
            self.action_dict[action_number] = self.intrude
            action_set.append(action_number)
            probabilities_set.append(self.network_interface.game_mode.red.
                                     action_set.random_infect.likelihood.value)
            action_number += 1
        if self.network_interface.game_mode.red.action_set.basic_attack.use.value:
            self.action_dict[action_number] = self.basic_attack
            action_set.append(action_number)
            probabilities_set.append(self.network_interface.game_mode.red.
                                     action_set.basic_attack.likelihood.value)
            action_number += 1
        if self.network_interface.game_mode.red.action_set.do_nothing.use.value:
            self.action_dict[action_number] = self.do_nothing
            action_set.append(action_number)
            probabilities_set.append(self.network_interface.game_mode.red.
                                     action_set.do_nothing.likelihood.value)
            action_number += 1
        if self.network_interface.game_mode.red.action_set.move.use.value:
            self.action_dict[action_number] = self.random_move
            action_set.append(action_number)
            probabilities_set.append(self.network_interface.game_mode.red.
                                     action_set.move.likelihood.value)
            action_number += 1

        # probabilities_set_normal 对 probabilities_set 进行归一化处理，
        # 以确保所有概率之和为 1，从而使这些概率能够被 numpy 等库用作权重。
        # normalises the weights so they work with numpy choices
        probabilities_set_normal = [
            float(i) / sum(probabilities_set) for i in probabilities_set
        ]

        # 通过 super() 调用父类 RedActionSet 的构造函数，并传递 network_interface、action_set 和归一化后的概率集 probabilities_set_normal。

        super().__init__(network_interface, action_set,
                         probabilities_set_normal)

    def perform_action(
            self) -> Dict[int, Dict[str, List[Union[bool, str, None]]]]:
        """Chooses and then performs an action.

        - perform_action 方法选择并执行一个动作，这是红方代理在每个回合都会调用的方法。
        - 返回值是一个字典，包含动作的名称、成功状态、目标节点、攻击节点以及可能的自然传播攻击信息。

        This is called for every one of the red agents turns

        Returns:
            A tuple containing the name of the action, the success status, the target, the attacking node and any natural spreading attacks
        """
        # current_turn_attack_info 是一个字典，用于存储当前回合中所有执行的动作信息。
        # action_count 用于跟踪动作的计数。
        current_turn_attack_info = {}
        action_count = 0

        # 如果自然传播（natural spreading）在配置文件中被启用，
        # 则执行 self.natural_spread() 并将其结果记录到 current_turn_attack_info 中。

        if self.network_interface.game_mode.red.natural_spreading.capable.value:
            current_turn_attack_info[action_count] = self.natural_spread()
            action_count += 1

        # 如果启用了零日攻击（zero-day attack），红方代理会尝试进行攻击，
        # 如果成功，将结果记录到 current_turn_attack_info 中。

        zd = False
        # tries to use a zero day attack if it is enabled (not in the main dictionary as it tries it every turn)
        if self.network_interface.game_mode.red.action_set.zero_day.use.value:
            inter = self.zero_day_attack()
            if True in inter['Successes']:
                current_turn_attack_info[action_count] = inter
                zd = True
                action_count += 1

        # 如果未进行零日攻击，红方代理会随机选择一个动作并执行。
        if zd is False:
            # chooses an action
            action = self.choose_action()

            # performs the action
            current_turn_attack_info[action_count] = self.action_dict[action]()
            action_count += 1

            # If there are no possible targets for an attack then red will attempt to move to a new node
            if (current_turn_attack_info[action_count - 1]['Action'] ==
                    'no_possible_targets'):
                current_turn_attack_info[action_count] = self.random_move()
                action_count += 1
        # increments the day for the zero day
        if self.network_interface.game_mode.red.action_set.zero_day.use.value:
            self.increment_day()

        all_attacking = [
            node for l_nodes in list(
                map(
                    lambda y: y['Attacking_Nodes'],
                    filter(
                        lambda x: x['Action'] not in self.
                        non_attacking_actions,
                        current_turn_attack_info.values(),
                    ),
                )) for node in l_nodes
        ]

        all_target = [
            node for l_nodes in list(
                map(
                    lambda y: y['Target_Nodes'],
                    filter(
                        lambda x: x['Action'] not in self.
                        non_attacking_actions,
                        current_turn_attack_info.values(),
                    ),
                )) for node in l_nodes
        ]

        all_success = [
            node for l_nodes in list(
                map(
                    lambda y: y['Successes'],
                    filter(
                        lambda x: x['Action'] not in self.
                        non_attacking_actions,
                        current_turn_attack_info.values(),
                    ),
                )) for node in l_nodes
        ]
        # 最后，更新网络接口中存储的攻击信息。
        self.network_interface.update_stored_attacks(all_attacking, all_target,
                                                     all_success)

        return current_turn_attack_info
