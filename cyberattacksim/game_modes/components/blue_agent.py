from __future__ import annotations

from typing import Optional, Union

from cyberattacksim.config.core import ConfigGroup, ConfigGroupValidation
from cyberattacksim.config.groups.core import NodeChanceGroup, UseChancesGroup
from cyberattacksim.config.groups.validation import AnyUsedGroup
from cyberattacksim.config.item_types.bool_item import BoolItem, BoolProperties
from cyberattacksim.config.item_types.float_item import (FloatItem,
                                                         FloatProperties)
from cyberattacksim.config.item_types.int_item import IntItem, IntProperties
from cyberattacksim.exceptions import ConfigGroupValidationError

# --- Tier 1 groups ---
# 两个类 MakeNodeSafeGroup 和 DeceptiveNodeGroup 都是 ConfigGroup 的子类，
# 用于配置与蓝方（"Blue"）相关的网络安全模拟选项。这些类封装了一组配置项，
# 并且提供了一个验证方法 validate，用于确保配置的有效性。


class MakeNodeSafeGroup(ConfigGroup):
    """Group of values that collectively.

    这个类定义了蓝方在网络中修复节点时的配置选项。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        increases_vulnerability: Optional[bool] = False,
        gives_random_vulnerability: Optional[bool] = False,
        vulnerability_change: Optional[Union[float, int]] = None,
    ) -> None:
        """
        use: 一个布尔值，指示蓝方是否可以修复节点，但不恢复到初始状态。
        increases_vulnerability: 一个布尔值，指示修复节点时是否会增加节点的脆弱性。
        gives_random_vulnerability: 一个布尔值，指示修复节点时是否会随机设置节点的脆弱性。
        vulnerability_change: 一个浮点值，表示修复节点时节点的脆弱性变化量。
        """

        self.use: BoolItem = BoolItem(
            value=use,
            doc=
            'Blue fixes a node but does not restore it to its initial state.',
            alias='blue_uses_make_node_safe',
            properties=BoolProperties(allow_null=False, default=False),
        )
        self.increases_vulnerability: BoolItem = BoolItem(
            value=increases_vulnerability,
            doc=
            'If blue fixes a node then the vulnerability score of that node increases.',
            alias='making_node_safe_modifies_vulnerability',
            properties=BoolProperties(allow_null=False),
        )
        self.gives_random_vulnerability: BoolItem = BoolItem(
            value=gives_random_vulnerability,
            doc='making_node_safe_gives_random_vulnerability',
            alias='making_node_safe_gives_random_vulnerability',
            properties=BoolProperties(allow_null=False),
        )
        self.vulnerability_change: FloatItem = FloatItem(
            value=vulnerability_change,
            doc=
            'The amount that the vulnerability of a node changes when it is made safe.',
            alias='vulnerability_change_during_node_patch',
            properties=FloatProperties(
                allow_null=True,
                default=0,
                min_val=-1,
                max_val=1,
                inclusive_min=True,
                inclusive_max=True,
            ),
        )
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this
        :class: `~cyberattacksim.config.core.ConfigGroup`."""
        super().validate()
        try:
            if (self.increases_vulnerability.value
                    and self.gives_random_vulnerability.value):
                msg = 'Making a node safe cannot simultaneously increase the nodes vulnerability by a set amount and randomly set the vulnerability'
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


class DeceptiveNodeGroup(ConfigGroup):
    """The options related to the blue agents use of deceptive nodes.

    这个类定义了蓝方使用欺骗节点（deceptive nodes）时的配置选项。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        max_number: Optional[int] = 1,
        new_node_on_relocate: Optional[bool] = False,
    ) -> None:
        """
        use: 一个布尔值，指示蓝方是否可以放置欺骗节点。
        max_number: 一个整数，表示蓝方可以放置的最大欺骗节点数。
        new_node_on_relocate: 一个布尔值，指示当重新安置一个欺骗节点时，是否重新生成节点的属性。
        """
        self.use: BoolItem = BoolItem(
            value=use,
            doc=
            ('Blue agent can place down deceptive nodes. These nodes act as just another node '
             'in the network but have a different chance of spotting attacks and always show when they are compromised.'
             ),
            alias='blue_uses_deceptive_nodes',
            properties=BoolProperties(allow_null=False, default=False),
        )
        self.max_number: IntItem = IntItem(
            value=max_number,
            doc='The max number of deceptive nodes that blue can place.',
            alias='max_number_deceptive_nodes',
            properties=IntProperties(allow_null=True,
                                     default=1,
                                     min_val=0,
                                     inclusive_min=True),
        )
        self.new_node_on_relocate: BoolItem = BoolItem(
            value=new_node_on_relocate,
            doc="""
            When the blue agent places a deceptive node and it has none left in stock it will "pick up"
            the first deceptive node that it used and "relocate it" When relocating a node will the stats for the node
            (such as the vulnerability and compromised status)
            be re-generated as if adding a new node or will they carry over from the "old" node.""",
            alias='relocating_deceptive_nodes_generates_a_new_node',
            properties=BoolProperties(allow_null=True, default=False),
        )
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this
        :class: `~cyberattacksim.config.core.ConfigGroup`."""
        super().validate()
        try:
            if self.use.value and self.max_number.value == 0:
                msg = 'if the blue agent can use deceptive nodes then it must be able to create at least 1.'
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


# --- Tier 2 groups ---
# 这是三组用于网络安全模拟中“蓝方”代理行为和检测机制的配置类。
# 每个类都继承自 ConfigGroup，并提供了一些与“蓝方”代理行为相关的配置选项。


class BlueActionSetGroup(AnyUsedGroup):
    """The options related to the actions that the blue agent can perform.

    该类定义了蓝方代理可以执行的一系列操作，如降低节点脆弱性、隔离节点、重新连接节点等。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        reduce_vulnerability: Optional[bool] = False,
        restore_node: Optional[bool] = False,
        scan: Optional[bool] = False,
        isolate_node: Optional[bool] = False,
        reconnect_node: Optional[bool] = False,
        do_nothing: Optional[bool] = False,
        make_node_safe: Optional[MakeNodeSafeGroup] = None,
        deceptive_nodes: Optional[DeceptiveNodeGroup] = None,
    ) -> None:
        """
        - reduce_vulnerability: 布尔值，表示蓝方是否可以降低节点的脆弱性。
        - restore_node: 布尔值，表示蓝方是否可以将节点恢复到初始状态。
        - scan: 布尔值，表示蓝方是否可以扫描节点以检测红方入侵。
        - isolate_node: 布尔值，表示蓝方是否可以隔离节点。
        - reconnect_node: 布尔值，表示蓝方是否可以重新连接节点。
        - do_nothing: 布尔值，表示蓝方是否可以选择在某一轮中不执行任何操作。
        - make_node_safe: MakeNodeSafeGroup 实例，定义蓝方修复节点的行为。
        - deceptive_nodes: DeceptiveNodeGroup 实例，定义蓝方使用欺骗节点的行为。
        """
        self.reduce_vulnerability: BoolItem = BoolItem(
            value=reduce_vulnerability,
            doc='Blue picks a node and reduces the vulnerability score.',
            alias='blue_uses_reduce_vulnerability',
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.restore_node: BoolItem = BoolItem(
            value=restore_node,
            doc=
            'Blue picks a node and restores everything about the node to its starting state.',
            alias='blue_uses_restore_node',
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.scan: BoolItem = BoolItem(
            value=scan,
            doc=
            'Blue scans all the nodes to try and detect any red intrusions.',
            alias='blue_uses_scan',
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.isolate_node: BoolItem = BoolItem(
            value=isolate_node,
            doc='Blue disables all the connections to and from a node.',
            alias='blue_uses_isolate_node',
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.reconnect_node: BoolItem = BoolItem(
            value=reconnect_node,
            doc='Blue re-connects all the connections to and from a node.',
            alias='blue_uses_reconnect_node',
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.do_nothing: BoolItem = BoolItem(
            value=do_nothing,
            doc='The blue agent is able to perform no attack for a given turn.',
            alias='blue_uses_do_nothing',
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.make_node_safe: MakeNodeSafeGroup = (
            make_node_safe if make_node_safe else MakeNodeSafeGroup(
                doc=
                'all information relating to the process of the blue fixing a node but not restoring it to its initial state.',
            ))
        self.deceptive_nodes: DeceptiveNodeGroup = (
            deceptive_nodes if deceptive_nodes else DeceptiveNodeGroup(doc=(
                'all information relating to the blue agent placing down deceptive nodes.'
                'These nodes act as just another node in the network but have a '
                'different chance of spotting attacks and always show when they '
                'are compromised.')))
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this
        :class: `~cyberattacksim.config.core.ConfigGroup`.
        验证确保当蓝方能够隔离或重新连接节点时，这两个操作的可用性是一致的。
        """
        super().validate()

        pair = [self.isolate_node.value, self.reconnect_node.value]
        try:
            if any(v is True for v in pair) and not all(v is True
                                                        for v in pair):
                msg = 'Blue should be able to reconnect or isolate nodes if the other is true.'
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


class BlueIntrusionDiscoveryGroup(ConfigGroup):
    """The options related to the ability for the blue agent to discover the
    red agents intrusions into the network.

    该类定义了蓝方发现红方入侵的概率。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        immediate_standard_node: Optional[Union[int, float]] = None,
        immediate_deceptive_node: Optional[Union[int, float]] = None,
        on_scan_standard_node: Optional[Union[int, float]] = None,
        on_scan_deceptive_node: Optional[Union[int, float]] = None,
    ) -> None:
        # immediate: NodeChanceGroup 实例，定义红方一旦入侵节点，蓝方立即发现入侵的概率。
        self.immediate = NodeChanceGroup(
            standard_node=immediate_standard_node,
            deceptive_node=immediate_deceptive_node,
        )

        self.immediate.standard_node.alias = 'chance_to_immediately_discover_intrusion'
        self.immediate.standard_node.doc = 'Chance for blue to discover a node that red has compromised the instant red compromises the node.'

        self.immediate.deceptive_node.alias = (
            'chance_to_immediately_discover_intrusion_deceptive_node')
        self.immediate.deceptive_node.doc = 'Chance for blue to discover a deceptive node that red has compromised the instant it is compromised.'

        # on_scan: NodeChanceGroup 实例，定义蓝方扫描节点时发现入侵的概率。
        self.on_scan = NodeChanceGroup(standard_node=on_scan_standard_node,
                                       deceptive_node=on_scan_deceptive_node)

        self.on_scan.standard_node.alias = 'chance_to_discover_intrusion_on_scan'
        self.on_scan.standard_node.doc = 'When blue performs the scan action this is the chance that a red intrusion is discovered.'

        self.on_scan.deceptive_node.alias = (
            'chance_to_discover_intrusion_on_scan_deceptive_node')
        self.on_scan.deceptive_node.doc = 'When blue uses the scan action what is the chance that blue will detect an intrusion in a deceptive node.'

        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this
        :class: `~cyberattacksim.config.core.ConfigGroup`."""
        super().validate()
        try:
            if (self.on_scan.deceptive_node.value <=
                    self.on_scan.standard_node.value) and (
                        self.on_scan.deceptive_node.value != 1):
                msg = 'there should be a higher chance at detecting intrusions on deceptive nodes than standard nodes.'
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation


class BlueAttackDiscoveryGroup(ConfigGroup):
    """The options related to the blue agents ability to discover the attacks
    the red agent makes to nodes within the network.

    该类定义了蓝方发现红方攻击的概率。
    """

    def __init__(
        self,
        doc: Optional[str] = None,
        failed_attacks: Optional[UseChancesGroup] = None,
        succeeded_attacks_known_compromise: Optional[UseChancesGroup] = None,
        succeeded_attacks_unknown_compromise: Optional[UseChancesGroup] = None,
    ) -> None:
        # - failed_attacks: UseChancesGroup
        # 实例，定义蓝方发现红方攻击失败的概率。
        self.failed_attacks: UseChancesGroup = (
            failed_attacks if failed_attacks else UseChancesGroup(
                doc=
                'Whether the blue can discover failed attacks and the associated chance of discovery.'
            ))
        self.failed_attacks.use.alias = 'can_discover_failed_attacks'

        self.failed_attacks.chance.standard_node.alias = (
            'chance_to_discover_failed_attack')

        self.failed_attacks.chance.deceptive_node.alias = (
            'chance_to_discover_failed_attack_deceptive_node')

        # - succeeded_attacks_known_compromise: UseChancesGroup
        # 实例，定义蓝方在已知节点被攻陷的情况下，发现红方成功攻击的概率。
        self.succeeded_attacks_known_compromise: UseChancesGroup = (
            succeeded_attacks_known_compromise
            if succeeded_attacks_known_compromise else UseChancesGroup(
                doc=
                'Whether the blue can discover succeeded attacks where the nature '
                'of the compromise is known and the associated chance of discovery.'
            ))
        self.succeeded_attacks_known_compromise.use.alias = (
            'can_discover_succeeded_attacks_if_compromise_is_discovered')

        self.succeeded_attacks_known_compromise.chance.standard_node.alias = (
            'chance_to_discover_succeeded_attack_compromise_known')

        self.succeeded_attacks_known_compromise.chance.deceptive_node.alias = (
            'chance_to_discover_succeeded_attack_deceptive_node')

        # succeeded_attacks_unknown_compromise: UseChancesGroup
        # 实例，定义蓝方在未知节点被攻陷的情况下，发现红方成功攻击的概率。
        self.succeeded_attacks_unknown_compromise: UseChancesGroup = (
            succeeded_attacks_unknown_compromise
            if succeeded_attacks_unknown_compromise else UseChancesGroup(
                doc=
                'Whether the blue can discover succeeded attacks where the nature '
                'of the compromise is unknown and the associated chance of discovery.'
            ))
        self.succeeded_attacks_unknown_compromise.use.alias = (
            'can_discover_succeeded_attacks_if_compromise_is_not_discovered')

        self.succeeded_attacks_unknown_compromise.chance.standard_node.alias = (
            'chance_to_discover_succeeded_attack_compromise_not_known')

        # Set the deceptive node chances to both reference same config item
        self.succeeded_attacks_unknown_compromise.chance.deceptive_node = (
            self.succeeded_attacks_known_compromise.chance.deceptive_node)

        super().__init__(doc)


# --- Tier 3 groups ---


class Blue(ConfigGroup):
    """All options relating to the behavior of the blue agent. Blue
    类用于配置蓝方代理在网络安全模拟中的行为及其相关选项。 这个类将蓝方的行动集、入侵检测概率和攻击发现配置组合在一起，
    并添加了特定的验证逻辑，以确保这些配置的一致性和合理性。

    - action_set：蓝方代理可执行的操作集合，由 BlueActionSetGroup 定义。
    - intrusion_discovery_chance：蓝方发现红方入侵的概率，由 BlueIntrusionDiscoveryGroup 定义。
    - attack_discovery：蓝方发现红方攻击的概率，由 BlueAttackDiscoveryGroup 定义。
    """

    def __init__(
        self,
        action_set: Optional[BlueActionSetGroup] = None,
        intrusion_discovery_chance: Optional[
            BlueIntrusionDiscoveryGroup] = None,
        attack_discovery: Optional[BlueAttackDiscoveryGroup] = None,
    ) -> None:
        """
        - action_set：BlueActionSetGroup 的实例，包含蓝方的行动集。 \
            如果未提供，则使用默认的 BlueActionSetGroup 实例。
        - intrusion_discovery_chance：BlueIntrusionDiscoveryGroup 的实例，包含蓝方入侵发现概率的配置。 \
            如果未提供，则使用默认的 BlueIntrusionDiscoveryGroup 实例。
        - attack_discovery：BlueAttackDiscoveryGroup 的实例，包含蓝方攻击发现概率的配置。 \
            如果未提供，则使用默认的 BlueAttackDiscoveryGroup 实例。
        """
        doc = 'The configuration of the blue agent'
        self.action_set: BlueActionSetGroup = (
            action_set if action_set else BlueActionSetGroup(
                doc=
                'The set of actions the blue agent can perform and their associated information.'
            ))
        self.intrusion_discovery_chance: BlueIntrusionDiscoveryGroup = (
            intrusion_discovery_chance
            if intrusion_discovery_chance else BlueIntrusionDiscoveryGroup(
                doc=
                'The chances of blue discovering intrusions for different node types.'
            ))
        self.attack_discovery: BlueAttackDiscoveryGroup = (
            attack_discovery if attack_discovery else BlueAttackDiscoveryGroup(
                doc=
                'Which of reds attacks can the blue agent discover together with their associated discovery chances for different node types.'
            ))
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this
        :class: `~cyberattacksim.config.core.ConfigGroup`."""
        super().validate()
        try:
            if (self.action_set.scan.value and self.intrusion_discovery_chance.
                    immediate.standard_node.value == 1):
                msg = (
                    'The scan action is selected yet blue has 100% chance to spot '
                    'detections. There is no need for the blue to have the scan '
                    'action in this case.')
                raise ConfigGroupValidationError(msg)
            elif (not self.action_set.scan.value and
                  self.intrusion_discovery_chance.immediate.standard_node.value
                  != 1):
                msg = (
                    'If the blue agent cannot scan nodes then it should be able to '
                    'automatically detect the intrusions.')
                raise ConfigGroupValidationError(msg)
        except ConfigGroupValidationError as e:
            self.validation.add_validation(msg, e)
        return self.validation
