from __future__ import annotations

from typing import Optional

from cyberattacksim.config.core import ConfigGroup
from cyberattacksim.config.item_types.bool_item import BoolItem, BoolProperties

# --- Tier 0 groups


class Reset(ConfigGroup):
    """The modifications to network performed on reset.

    说明：该类定义了在网络重置时进行的各种修改设置。这些设置包括随机化节点漏洞、选择新高价值节点和选择新入口节点。
    """

    def __init__(
        self,
        randomise_vulnerabilities: Optional[bool] = False,
        choose_new_high_value_nodes: Optional[bool] = False,
        choose_new_entry_nodes: Optional[bool] = False,
    ) -> None:
        """
        Args:
            randomise_vulnerabilities: bool 类型（可选），指示是否在网络重置时随机化节点漏洞。
            choose_new_high_value_nodes: bool 类型（可选），指示是否在网络重置时选择新的高价值节点。
            choose_new_entry_nodes: bool 类型（可选），指示是否在网络重置时选择新的入口节点。
        """
        doc = 'The changes to the network made upon reset'
        self.randomise_vulnerabilities = BoolItem(
            value=randomise_vulnerabilities,
            doc='Randomise the node vulnerabilities when the network is reset',
            properties=BoolProperties(allow_null=True, default=False),
            alias='randomise_vulnerabilities_on_reset',
        )
        self.choose_new_high_value_nodes = BoolItem(
            value=choose_new_high_value_nodes,
            doc='Choose new high value nodes when the network is reset',
            properties=BoolProperties(allow_null=True, default=False),
            alias='choose_new_high_value_nodes_on_reset',
        )
        self.choose_new_entry_nodes = BoolItem(
            value=choose_new_entry_nodes,
            doc='Choose new entry nodes when the network is reset',
            properties=BoolProperties(allow_null=True, default=False),
            alias='choose_new_entry_nodes_on_reset',
        )
        super().__init__(doc)
