from __future__ import annotations

from typing import Optional

from cyberattacksim.config.core import ConfigGroup
from cyberattacksim.config.item_types.bool_item import BoolItem, BoolProperties
from cyberattacksim.config.item_types.int_item import IntItem, IntProperties

# --- Tier 0 groups


class Miscellaneous(ConfigGroup):
    """Miscellaneous settings."""

    def __init__(
        self,
        random_seed: Optional[int] = None,
        output_timestep_data_to_json: Optional[bool] = False,
    ) -> None:
        """
        Args:
            random_seed: int 类型（可选），用于设置随机数生成器的种子，使得游戏输出可以是确定性的。这对于测试和调试非常有用。
            output_timestep_data_to_json: bool 类型（可选），用于设置是否将每一步的状态数据输出到 JSON 文件中。包括节点之间的连接、节点状态以及蓝方在该回合中看到的攻击。
        """
        doc = 'Additional options'
        self.random_seed = IntItem(
            value=random_seed,
            doc=
            'Seed to inform the random number generation of python and numpy thereby creating deterministic game outputs',
            properties=IntProperties(allow_null=True),
            alias='random_seed',
        )
        self.output_timestep_data_to_json = BoolItem(
            value=output_timestep_data_to_json,
            doc=
            'Toggle to output a json file for each step that contains the connections between nodes, the states of the nodes and the attacks that blue saw in that turn',
            properties=BoolProperties(allow_null=True, default=False),
            alias='output_timestep_data_to_json',
        )

        super().__init__(doc)
