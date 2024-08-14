from __future__ import annotations

from typing import Optional, Union

from cyberattacksim.config.core import ConfigGroup, ConfigGroupValidation
from cyberattacksim.config.groups.core import (ActionLikelihoodChanceGroup,
                                               ActionLikelihoodGroup,
                                               UseValueGroup)
from cyberattacksim.config.groups.validation import AnyUsedGroup
from cyberattacksim.config.item_types.bool_item import BoolItem, BoolProperties
from cyberattacksim.config.item_types.float_item import (FloatItem,
                                                         FloatProperties)
from cyberattacksim.config.item_types.int_item import IntItem, IntProperties
from cyberattacksim.config.item_types.str_item import StrItem, StrProperties
from cyberattacksim.exceptions import ConfigGroupValidationError

# -- Tier 0 groups ---
# 这段代码定义了四个类，它们用于配置和验证红方（攻击者）的行为和特性。
# 每个类都是从一个基类 ConfigGroup 继承而来，并定义了红方的不同配置选项。以下是每个类的详细解释：


class ZeroDayGroup(ConfigGroup):
    """Group of values that collectively describe the red zero day action.

    这个类描述了红方使用零日攻击（zero day attack）的相关配置。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        start_amount: Optional[int] = 0,
        days_required: Optional[int] = 0,
    ) -> None:
        """
        - use: 一个布尔值，表示红方是否使用零日攻击。如果为 True，红方会选择一个安全的节点（已感染节点的连接节点）并将其攻陷，成功率为100%，但只能在每隔 n 个时间步长执行一次。
        - start_amount: 一个整数，表示红方在游戏开始时拥有的零日攻击的数量。
        - days_required: 一个整数，表示红方在获得一次新的零日攻击前需要经过的“进度”时间。
        """
        self.use: BoolItem = BoolItem(
            value=use,
            doc=
            'The red agent will pick a safe node connected to an infected node and take it over with a 100% chance to succeed (can only happen every n timesteps).',
            properties=BoolProperties(allow_null=False, default=False),
            alias='red_uses_zero_day_action',
        )
        self.start_amount: IntItem = IntItem(
            value=start_amount,
            doc=
            'The number of zero-day attacks that the red agent starts with.',
            properties=IntProperties(allow_null=True,
                                     default=0,
                                     min_val=0,
                                     inclusive_min=True),
            alias='zero_day_start_amount',
        )
        self.days_required: IntItem = IntItem(
            value=days_required,
            doc=
            "The amount of 'progress' that need to have passed before the red agent gains a zero day attack.",
            properties=IntProperties(allow_null=True,
                                     default=0,
                                     min_val=0,
                                     inclusive_min=True),
            alias='days_required_for_zero_day',
        )
        super().__init__(doc)


class AttackSourceGroup(ConfigGroup):
    """The ConfigGroup to represent to the source of the red agents attacks.

    这个类用于配置红方发起攻击的来源节点。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        only_main_red_node: Optional[bool] = False,
        any_red_node: Optional[bool] = False,
    ) -> None:
        """
        Args:
            only_main_red_node: 一个布尔值，表示红方是否只能从它的主节点发起攻击。
            any_red_node: 一个布尔值，表示红方是否可以从它控制的任何节点发起攻击。
        """
        self.only_main_red_node = BoolItem(
            value=only_main_red_node,
            doc='Red agent can only attack from its main node on that turn.',
            properties=BoolProperties(allow_null=False, default=False),
            alias='red_can_only_attack_from_red_agent_node',
        )
        self.any_red_node = BoolItem(
            value=any_red_node,
            doc='Red can attack from any node that it controls.',
            properties=BoolProperties(allow_null=False, default=False),
            alias='red_can_attack_from_any_red_node',
        )

        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this
        :class: `~cyberattacksim.config.core.ConfigGroup`."""
        super().validate()
        try:
            if self.only_main_red_node.value and self.any_red_node.value:
                msg = (
                    'The red agent cannot attack from multiple sources simultaneously.'
                )
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


class NaturalSpreadChanceGroup(ConfigGroup):
    """The ConfigGroup to represent the chances of reads natural spreading to
    different node types.

    这个类定义了红方自然传播的概率。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        to_connected_node: Optional[Union[int, float]] = 0,
        to_unconnected_node: Optional[Union[int, float]] = 0,
    ) -> None:
        """
        Args:
            to_connected_node: 一个浮点数，表示如果一个节点连接到已感染的节点，它在每个时间步长中被感染的概率。
            to_unconnected_node: 一个浮点数，表示如果一个节点没有连接到已感染的节点，它在每个时间步长中随机被感染的概率。
        """
        self.doc = doc
        self.to_connected_node = FloatItem(
            value=to_connected_node,
            doc=
            ' If a node is connected to a compromised node what chance does it have to become compromised every turn through natural spreading.',
            properties=FloatProperties(
                allow_null=True,
                default=0,
                min_val=0,
                max_val=1,
                inclusive_min=True,
                inclusive_max=True,
            ),
            alias='chance_to_spread_to_connected_node',
        )
        self.to_unconnected_node = FloatItem(
            value=to_unconnected_node,
            doc=
            'If a node is not connected to a compromised node what chance does it have to become randomly infected through natural spreading.',
            properties=FloatProperties(
                allow_null=True,
                default=0,
                min_val=0,
                max_val=1,
                inclusive_min=True,
                inclusive_max=True,
            ),
            alias='chance_to_spread_to_unconnected_node',
        )
        super().__init__()


class TargetNodeGroup(ConfigGroup):
    """The Config group to represent the information relevant to the red agents
    target node.

    这个类描述了红方攻击的目标节点的相关信息。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        target: Optional[str] = None,
        always_choose_shortest_distance: Optional[bool] = False,
    ) -> None:
        """
        Args:
            use: 一个布尔值，表示红方是否要瞄准特定的目标节点。
            target: 一个字符串，表示红方瞄准的目标节点的名称。
            always_choose_shortest_distance: 一个布尔值，表示红方是否总是选择到目标节点的最短路径进行攻击，或者是根据距离的倒数权重来选择攻击路径。
        """
        self.use: BoolItem = BoolItem(
            value=use,
            doc='Red targets a specific node.',
            properties=BoolProperties(allow_null=False, default=False),
        )
        self.target: StrItem = StrItem(
            value=target,
            doc='The name of a node that the red agent targets.',
            properties=StrProperties(allow_null=True),
            alias='red_target_node',
        )
        self.always_choose_shortest_distance: BoolItem = BoolItem(
            value=always_choose_shortest_distance,
            doc=
            'Whether red should pick the absolute shortest distance to the target node or choose nodes to attack based on a chance weighted inversely by distance',
            properties=BoolProperties(allow_null=True),
            alias='red_always_chooses_shortest_distance_to_target',
        )
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this
        :class: `~cyberattacksim.config.core.ConfigGroup`."""
        super().validate()
        try:
            if self.target.value and not self.use.value:
                msg = f'Red is set to target {self.target.value}, if the red agent is set to a specific node then the element must have `used` set to True'
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


# --- Tier 1 groups ---
# 这段代码定义了多个配置类，用于表示红方（攻击者）的各种行为和能力。
# 每个类封装了特定的配置组，并提供了初始化和验证机制，以确保配置的合理性。


class RedActionSetGroup(AnyUsedGroup):
    """The ConfigGroup to represent all permissable actions the red agent can
    perform."""

    def __init__(
        self,
        doc: Optional[
            str] = 'All permissable actions the red agent can perform.',
        spread: Optional[ActionLikelihoodChanceGroup] = None,
        random_infect: Optional[ActionLikelihoodChanceGroup] = None,
        move: Optional[ActionLikelihoodGroup] = None,
        basic_attack: Optional[ActionLikelihoodGroup] = None,
        do_nothing: Optional[ActionLikelihoodGroup] = None,
        zero_day: Optional[ZeroDayGroup] = None,
    ):
        """The ActionLikelihoodChanceGroup constructor.

        :param spread: The likelihood of the action.
        :param random_infect: The chance of the action.
        :param doc: An optional descriptor.

        - spread: 表示红方尝试传播到每个已感染节点连接的节点及其发生概率的配置组。
        - random_infect: 表示红方尝试随机感染每个安全节点及其发生概率的配置组。
        - move: 表示红方移动到另一个节点及其发生概率的配置组。
        - basic_attack: 表示红方选择一个连接到已感染节点的单一节点并尝试攻击和占领该节点及其发生概率的配置组。
        - do_nothing: 表示红方在特定回合内不执行任何攻击及其发生概率的配置组。
        - zero_day: 表示零日攻击相关的配置组。
        """
        self.spread: ActionLikelihoodChanceGroup = (
            spread if spread else ActionLikelihoodChanceGroup(
                doc=
                'Whether red tries to spread to every node connected to an infected node and the associated likelihood of this occurring.'
            ))
        self.random_infect: ActionLikelihoodChanceGroup = (
            random_infect if random_infect else ActionLikelihoodChanceGroup(
                doc=
                'Whether red tries to infect every safe node in the environment and the associated likelihood of this occurring.'
            ))
        self.move: ActionLikelihoodGroup = (
            move if move else ActionLikelihoodGroup(
                doc=
                'Whether the red agent moves to a different node and the associated likelihood of this occurring.'
            ))
        self.basic_attack: ActionLikelihoodGroup = (
            basic_attack if basic_attack else ActionLikelihoodGroup(
                doc=
                'Whether the red agent picks a single node connected to an infected node and tries to attack and take over that node and the associated likelihood of this occurring.'
            ))
        self.do_nothing: ActionLikelihoodGroup = (
            do_nothing if do_nothing else ActionLikelihoodGroup(
                doc=
                'Whether the red agent is able to perform no attack for a given turn and the likelihood of this occurring.'
            ))
        self.zero_day: ZeroDayGroup = (zero_day if zero_day else ZeroDayGroup(
            doc=
            'Group of values that collectively describe the red zero day action.'
        ))

        self.spread.use.alias = 'red_uses_spread_action'

        self.random_infect.use.alias = 'red_uses_random_infect_action'

        self.move.use.alias = 'red_uses_move_action'

        self.basic_attack.use.alias = 'red_uses_basic_attack_action'

        self.do_nothing.use.alias = 'red_uses_do_nothing_action'

        self.spread.likelihood.alias = 'spread_action_likelihood'

        self.random_infect.likelihood.alias = 'random_infect_action_likelihood'

        self.move.likelihood.alias = 'move_action_likelihood'

        self.basic_attack.likelihood.alias = 'basic_attack_action_likelihood'

        self.do_nothing.likelihood.alias = 'do_nothing_action_likelihood'

        self.spread.chance.alias = 'chance_for_red_to_spread'

        self.random_infect.chance.alias = 'chance_for_red_to_random_compromise'

        super().__init__(doc)


class RedAgentAttackGroup(ConfigGroup):
    """The ConfigGroup to represent the information related to the red agents
    attacks.

    这个类表示与红方攻击相关的信息。
    """

    def __init__(
        self,
        doc: Optional[
            str] = 'The ConfigGroup to represent the information related to the red agents attacks.',
        ignores_defences: Optional[bool] = False,
        always_succeeds: Optional[bool] = False,
        skill: Optional[UseValueGroup] = None,
        attack_from: Optional[AttackSourceGroup] = None,
    ) -> None:
        """

        Args:
            ignores_defences: 布尔值，表示红方是否忽略节点的防御。
            always_succeeds: 布尔值，表示红方的攻击是否总是成功。
            skill: 表示红方在攻击节点时使用的技能修正值的配置组。
            attack_from: 表示红方发起攻击的来源节点的配置组。
        """
        self.ignores_defences = BoolItem(
            value=ignores_defences,
            doc='The red agent ignores the defences of nodes.',
            properties=BoolProperties(allow_null=False, default=False),
            alias='red_ignores_defences',
        )
        self.always_succeeds = BoolItem(
            value=always_succeeds,
            doc='Reds attacks always succeed.',
            properties=BoolProperties(allow_null=False, default=False),
            alias='red_always_succeeds',
        )
        self.skill = (skill if skill else UseValueGroup(
            doc='Red uses its skill modifier when attacking nodes.'))
        self.attack_from = (attack_from if attack_from else AttackSourceGroup(
            doc=
            ('The red agent will only ever be in one node however it can control any amount of nodes. '
             'Can the red agent only attack from its one main node or can it attack from any node that it controls.'
             )))

        self.skill.use.alias = 'red_uses_skill'

        self.skill.value.alias = 'red_skill'

        super().__init__(doc)


class RedNaturalSpreadingGroup(ConfigGroup):
    """The ConfigGroup to represent the information related to the red agents
    natural spreading ability.

    这个类表示与红方自然传播能力相关的信息。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        capable: Optional[bool] = False,
        chance: Optional[NaturalSpreadChanceGroup] = None,
    ) -> None:
        """
        Args:
            - capable: 布尔值，表示红方的感染是否能够自然传播到周围的节点。
            - chance: 表示红方自然传播到不同类型节点的概率的配置组。
        """
        self.capable = BoolItem(
            value=capable,
            doc=
            'Whether the red agents infection can naturally spread to surrounding nodes',
            properties=BoolProperties(allow_null=False, default=False),
            alias='red_can_naturally_spread',
        )
        self.chance = (chance if chance else NaturalSpreadChanceGroup(
            doc=
            'the chances of reads natural spreading to different node types.'))
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this
        :class: `~cyberattacksim.config.core.ConfigGroup`."""
        super().validate()
        if self.capable.value:
            try:
                elements = self.chance.get_config_elements(
                    [IntItem, FloatItem])
                if not any(e.value > 0 for e in elements.values()
                           if type(e.value) in [int, float]):
                    msg = (
                        f"At least 1 of {', '.join(elements.keys())} should be above 0"
                    )
                    raise ConfigGroupValidationError(msg)
            except ConfigGroupValidationError as e:
                self.validation.add_validation(msg, e)
        return self.validation


class RedTargetMechanismGroup(AnyUsedGroup):
    """The ConfigGroup to represent all possible target mechanism the red agent
    can use.

    这个类表示红方可以使用的所有目标选择机制
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        random: Optional[bool] = False,
        prioritise_connected_nodes: Optional[bool] = False,
        prioritise_unconnected_nodes: Optional[bool] = False,
        prioritise_vulnerable_nodes: Optional[bool] = False,
        prioritise_resilient_nodes: Optional[bool] = False,
        target_specific_node: Optional[TargetNodeGroup] = None,
    ) -> None:
        """
        Args:
            - random: 布尔值，表示红方是否随机选择目标节点。
            - prioritise_connected_nodes: 布尔值，表示红方是否优先选择连接最多的节点作为攻击目标。
            - prioritise_unconnected_nodes: 布尔值，表示红方是否优先选择连接最少的节点作为攻击目标。
            - prioritise_vulnerable_nodes: 布尔值，表示红方是否优先选择最脆弱的节点作为攻击目标。
            - prioritise_resilient_nodes: 布尔值，表示红方是否优先选择最坚固的节点作为攻击目标。
            - target_specific_node: 表示红方特定目标节点的配置信息。
        """
        self.random = BoolItem(
            doc='Red randomly chooses nodes to target',
            value=random,
            properties=BoolProperties(default=False, allow_null=True),
            alias='red_chooses_target_at_random',
        )
        self.prioritise_connected_nodes = BoolItem(
            doc=
            'Red sorts the nodes it can attack and chooses the one that has the most connections',
            value=prioritise_connected_nodes,
            properties=BoolProperties(default=False, allow_null=True),
            alias='red_prioritises_connected_nodes',
        )
        self.prioritise_unconnected_nodes = BoolItem(
            doc=
            'Red sorts the nodes it can attack and chooses the one that has the least connections',
            value=prioritise_unconnected_nodes,
            properties=BoolProperties(default=False, allow_null=True),
            alias='red_prioritises_un_connected_nodes',
        )
        self.prioritise_vulnerable_nodes = BoolItem(
            doc=
            'Red sorts the nodes is can attack and chooses the one that is the most vulnerable',
            value=prioritise_vulnerable_nodes,
            properties=BoolProperties(default=False, allow_null=True),
            alias='red_prioritises_vulnerable_nodes',
        )
        self.prioritise_resilient_nodes = BoolItem(
            doc=
            'Red sorts the nodes is can attack and chooses the one that is the least vulnerable',
            value=prioritise_resilient_nodes,
            properties=BoolProperties(default=False, allow_null=True),
            alias='red_prioritises_resilient_nodes',
        )
        self.target_specific_node = (
            target_specific_node if target_specific_node else TargetNodeGroup(
                doc=
                'The Config group to represent the information relevant to the red agents target node.'
            ))
        super().__init__(doc)


# --- Tier 2 group ---


class Red(ConfigGroup):
    """The ConfigGroup to represent all items necessary to configure the Red
    agent.

    Red 类是一个配置组，代表了红方（攻击者）在网络攻击模拟中的所有必要配置。 这个类将多个相关的配置组组合在一起，并提供了验证逻辑以确保配置的正确性。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        agent_attack: Optional[RedAgentAttackGroup] = None,
        action_set: Optional[RedActionSetGroup] = None,
        natural_spreading: Optional[RedNaturalSpreadingGroup] = None,
        target_mechanism: Optional[RedTargetMechanismGroup] = None,
    ) -> None:
        """
        Args:
            agent_attack: RedAgentAttackGroup 实例，表示与红方攻击相关的所有配置。
            action_set: RedActionSetGroup 实例，表示红方可以执行的所有动作的配置。
            natural_spreading: RedNaturalSpreadingGroup 实例，表示红方自然传播能力的配置。
            target_mechanism: RedTargetMechanismGroup 实例，表示红方目标选择机制的配置。
        """
        doc = 'The configuration of the red agent'
        self.agent_attack = (
            agent_attack if agent_attack else RedAgentAttackGroup(
                doc='All information related to the red agents attacks.'))
        self.action_set = (action_set if action_set else RedActionSetGroup(
            doc='All permissable actions the red agent can perform.'))
        self.natural_spreading = (
            natural_spreading
            if natural_spreading else RedNaturalSpreadingGroup(
                doc=
                'The information related to the red agents natural spreading ability.'
            ))
        self.target_mechanism = (
            target_mechanism if target_mechanism else RedTargetMechanismGroup(
                doc='all possible target mechanism the red agent can use.'))
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this
        :class: `~cyberattacksim.config.core.ConfigGroup`."""
        super().validate()

        try:
            if self.agent_attack.ignores_defences.value and (
                    self.target_mechanism.prioritise_vulnerable_nodes.value
                    or self.target_mechanism.prioritise_resilient_nodes.value):
                msg = 'If the red agent ignores defences then targeting based on this trait is impossible as it is ignored.'
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)

        return self.validation
