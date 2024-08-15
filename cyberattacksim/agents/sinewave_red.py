import math
import random
from typing import Dict, List, Union

from cyberattacksim.envs.generic.core.red_interface import RedInterface


def calculate_number_moves(attack_strength):
    """Calculate the number of moves for the red agent to take.

    Args:
        attack_strength: Current red agent attack strength

    Returns:
        An int representing the number of moves the red agent can take that turn
    """
    amount = math.floor(attack_strength)
    random_value = random.randint(0, 10)
    diff = attack_strength - amount
    if diff * 10 > random_value:
        amount += 1

    return int(amount)


class SineWaveRedAgent(RedInterface):
    """An agent which is based on the RedInterface provided by the
    CyberAttackSim generic environment.

    This agent is an example of how the generic RedInterface can be extended to include custom red
    team behaviour - in this case, action selection.

    The agent uses a sine wave to allow the red agent to attack more randomly and in waves rather than constantly.

    这个类继承了 RedInterface，意味着它是一个自定义的红队代理，符合该模拟环境的接口要求。
    """

    def __init__(self, network_interface):
        self.time = 0
        self.sine_offset = random.randint(0, 10)
        self.cosine_offset = random.randint(0, 10)
        self.sine_multiplier = round(random.uniform(1.5, 2.25), 4)
        self.cosine_multiplier = round(random.uniform(2.75, 3.5), 4)
        super().__init__(network_interface)

        # network_interface: 这是传递给父类的网络接口对象，用于与模拟环境进行交互。
        # self.time: 初始化时间步长为 0，随着每次红队行动的调用而递增。
        # self.sine_offset 和 self.cosine_offset: 随机生成的正弦和余弦偏移量，用于改变波形的相位。
        # self.sine_multiplier 和 self.cosine_multiplier: 正弦和余弦的倍数，控制波形的周期和幅度。

    def perform_action(
            self) -> Dict[int, Dict[str, List[Union[bool, str, None]]]]:
        """Chooses and then performs an action. This is called for every one of
        the red agents turns.

        功能: 选择并执行一个或多个行动，这是红队代理在每回合执行的核心方法。
        返回值: 一个字典，键为行动编号，值为行动的详细信息（包括成功状态、目标、攻击节点等）。

        行动选择与执行的逻辑

        - 时间步进:
        - 重置时间和偏移:
            如果时间超过 50，时间和偏移量将被重置。
        - 计算当前攻击强度:
            通过正弦和余弦函数计算当前攻击的强度，并根据红队的技能值调整。如果强度低于红队技能值，则将强度提升至技能值。
        - 计算行动次数:
            根据当前的攻击强度计算本回合的攻击次数。
        - 自然传播攻击:
            如果配置允许，红队会执行一次自然传播攻击。
        - 零日攻击:
            尝试执行零日攻击（即未知漏洞的攻击），并检查是否成功。如果成功，记录该攻击。
        - 选择其他攻击:
            在零日攻击失败的情况下，代理会尝试其他类型的攻击，直到达到本回合的攻击次数限制或没有可攻击的目标。
        - 随机移动:
            如果没有可攻击的目标，红队将尝试随机移动到新的节点。
        - 更新攻击信息:
            将本回合所有攻击的结果（攻击节点、目标节点、成功与否）更新到网络接口。

        Returns:
            A tuple containing the name of the action, the success status, the target, the attacking node and any natural spreading attacks
        """

        current_turn_attack_info = {}
        action_counter = 0

        # advances the agents power time
        self.time += round(random.uniform(0.2, 0.8), 2)
        if self.time >= 50:
            self.time = 0
            self.sine_offset = random.randint(0, 10)
            self.cosine_offset = random.randint(0, 10)

        red_skill = self.network_interface.game_mode.red.agent_attack.skill.value.value

        # works out the current strength of the red agent
        current_strength = (
            (math.sin(self.sine_multiplier * self.time + self.sine_offset) +
             math.cos(self.cosine_multiplier * self.time + self.cosine_offset))
            + red_skill - 0.5)
        # uses the red agents skill as a baseline
        if current_strength < red_skill:
            current_strength = red_skill

        # calculate the number of attacks that the red agent will get this go
        number_runs = calculate_number_moves(current_strength)

        if self.network_interface.game_mode.red.action_set.spread.use.value:
            current_turn_attack_info[action_counter] = self.natural_spread()

        zd = False
        # tries to use a zero day attack if it is enabled (not in the main dictionary as it tries it every turn)
        if self.network_interface.game_mode.red.action_set.zero_day.use.value:
            inter = self.zero_day_attack()
            if True in inter['Successes']:
                current_turn_attack_info[action_counter] = inter
                zd = True
                action_counter += 1
        if zd is False:
            counter = 0
            name = ''
            while counter < number_runs and name != 'no_possible_targets':
                # chooses an action
                action = self.choose_action()

                current_turn_attack_info[action_counter] = self.action_dict[
                    action]()
                action_counter += 1

                counter += 1
                name = current_turn_attack_info[action_counter - 1]['Action']

            # If there are no possible targets for an attack then red will attempt to move to a new node
            if name == 'no_possible_targets' and number_runs >= counter:
                current_turn_attack_info[action_counter] = self.random_move()
                action_counter += 1

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

        self.network_interface.update_stored_attacks(all_attacking, all_target,
                                                     all_success)
        return current_turn_attack_info
