from __future__ import annotations

from typing import Optional

from cyberattacksim.config.core import ConfigGroup, ConfigGroupValidation
from cyberattacksim.config.groups.core import RestrictRangeGroup, UseValueGroup
from cyberattacksim.config.groups.validation import AnyUsedGroup
from cyberattacksim.config.item_types.bool_item import BoolItem, BoolProperties
from cyberattacksim.config.item_types.int_item import IntItem, IntProperties
from cyberattacksim.exceptions import ConfigGroupValidationError

# --- Tier 0 groups


class NetworkCompatibilityGroup(ConfigGroup):
    """A set of optional restrictions that collectively constrain the types of
    network a game mode can be used upon.

    说明：这个类定义了一组可选的限制条件，用于约束游戏模式可以使用的网络类型。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        node_count: Optional[RestrictRangeGroup] = None,
        entry_node_count: Optional[RestrictRangeGroup] = None,
        high_value_node_count: Optional[RestrictRangeGroup] = None,
    ) -> None:
        """
        Args:
            - node_count: RestrictRangeGroup 实例，限制网络节点数量的范围。
            - entry_node_count: RestrictRangeGroup 实例，限制入口节点数量的范围。
            - high_value_node_count: RestrictRangeGroup 实例，限制高价值节点数量的范围。
        """
        self.node_count = (node_count if node_count else RestrictRangeGroup(
            doc=
            'Restrict the game mode to only work with network works within a range of node counts'
        ))
        self.entry_node_count = (
            entry_node_count if entry_node_count else RestrictRangeGroup(
                doc=
                'Restrict the game mode to only work with network works within a range of entry_node_count counts'
            ))
        self.high_value_node_count = (
            high_value_node_count
            if high_value_node_count else RestrictRangeGroup(
                doc=
                'Restrict the game mode to only work with network works within a range of high_value_node_count counts'
            ))

        self.node_count.min.alias = 'min_number_of_network_nodes'

        super().__init__(doc)


class BlueLossConditionGroup(AnyUsedGroup):
    """The state of the network that must be reached for the red agent to win
    the game.

    说明：该类定义了在网络达到某些条件时蓝方（防御方）输掉游戏的状态。这些条件是红方（攻击方）获胜的关键条件。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        all_nodes_lost: Optional[bool] = False,
        high_value_node_lost: Optional[bool] = False,
        target_node_lost: Optional[bool] = False,
        n_percent_nodes_lost: Optional[UseValueGroup] = None,
    ) -> None:
        """
        Args:
            - all_nodes_lost: bool 类型，若为 True，表示所有节点丢失时蓝方输掉游戏。
            - high_value_node_lost: bool 类型，若为 True，表示丢失一个特殊的高价值节点时蓝方输掉游戏。
            - target_node_lost: bool 类型，若为 True，表示目标节点丢失时蓝方输掉游戏。
            - n_percent_nodes_lost: UseValueGroup 类型，定义了蓝方输掉游戏所需丢失的节点百分比。如果不提供，使用默认的 UseValueGroup 实例。
        """
        self.all_nodes_lost: BoolItem = BoolItem(
            value=all_nodes_lost,
            doc='The blue agent loses if all the nodes become compromised',
            properties=BoolProperties(allow_null=True, default=False),
            alias='lose_when_all_nodes_lost',
        )
        self.high_value_node_lost: BoolItem = BoolItem(
            value=high_value_node_lost,
            doc=
            "Blue loses if a special node designated as 'high value' is lost",
            properties=BoolProperties(allow_null=True, default=False),
            alias='lose_when_high_value_node_lost',
        )
        self.target_node_lost: BoolItem = BoolItem(
            value=target_node_lost,
            doc='Blue loses if a target node it lost',
            properties=BoolProperties(allow_null=True, default=False),
            alias='lose_when_target_node_lost',
        )
        self.n_percent_nodes_lost: UseValueGroup = (
            n_percent_nodes_lost if n_percent_nodes_lost else UseValueGroup(
                doc=
                'The percentage of nodes that need to be lost for blue to lose',
            ))

        self.n_percent_nodes_lost.value.alias = (
            'percentage_of_nodes_compromised_equals_loss')

        self.n_percent_nodes_lost.use.alias = 'lose_when_n_percent_of_nodes_lost'

        super().__init__(doc)


# --- Tier 1 groups ---


class GameRules(ConfigGroup):
    """The overall rules of the game mode.

    说明：该类定义了游戏模式的整体规则，包括游戏的宽限期、最大步骤数、蓝方输掉条件和网络兼容性。
    """

    def __init__(
        self,
        grace_period_length: Optional[int] = 0,
        max_steps: Optional[int] = 0,
        blue_loss_condition: Optional[BlueLossConditionGroup] = None,
        network_compatibility: Optional[NetworkCompatibilityGroup] = None,
    ) -> None:
        """
        Args:
            self.grace_period_length: 使用 IntItem 管理游戏宽限期的长度，包括相关的文档和别名。
            self.max_steps: 使用 IntItem 管理游戏的最大步骤数，包括相关的文档和别名。
            self.blue_loss_condition: 使用 BlueLossConditionGroup 管理蓝方输掉游戏的条件，如果没有提供，则使用默认的 BlueLossConditionGroup 实例。
            self.network_compatibility: 使用 NetworkCompatibilityGroup 管理网络兼容性，如果没有提供，则使用默认的 NetworkCompatibilityGroup 实例。

        """
        doc = 'The rules of the overall game mode'
        self.grace_period_length = IntItem(
            value=grace_period_length,
            doc=
            ('The length of a grace period at the start of the game. During this time the red agent cannot act. '
             "This gives the blue agent a chance to 'prepare' (A length of 0 means that there is no grace period)"
             ),
            properties=IntProperties(
                allow_null=False,
                default=0,
                min_val=0,
                max_val=100,
                inclusive_min=True,
                inclusive_max=True,
            ),
            alias='grace_period_length',
        )
        self.max_steps = IntItem(
            value=max_steps,
            doc=
            'The max steps that a game can go on for. If the blue agent reaches this they win',
            properties=IntProperties(
                allow_null=False,
                default=1,
                min_val=1,
                max_val=10_000_000,
                inclusive_min=True,
                inclusive_max=True,
            ),
            alias='max_steps',
        )
        self.blue_loss_condition: BlueLossConditionGroup = (
            blue_loss_condition
            if blue_loss_condition else BlueLossConditionGroup(
                doc=
                'The state of the network that must be reached for the red agent to win the game.',
            ))
        self.network_compatibility: NetworkCompatibilityGroup = (
            network_compatibility
            if network_compatibility else NetworkCompatibilityGroup(
                doc='The range of networks the game mode can be played upon'))
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this
        :class: `~cyberattacksim.config.core.ConfigGroup`."""
        super().validate()
        try:
            if self.grace_period_length.value > self.max_steps.value:
                msg = 'The grace period cannot be the entire length of the game'
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation
