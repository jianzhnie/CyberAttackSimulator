from __future__ import annotations

from typing import Optional

from cyberattacksim.config.core import ConfigGroup
from cyberattacksim.config.item_types.bool_item import BoolItem, BoolProperties
from cyberattacksim.config.item_types.int_item import IntItem, IntProperties
from cyberattacksim.config.item_types.str_item import StrItem, StrProperties

# --- Tier 0 groups


class Rewards(ConfigGroup):
    """The rewards the blue agent receives based upon the final game state.

    说明：该类定义了蓝色代理在游戏结束时根据最终游戏状态获得的奖励。
    """

    def __init__(
        self,
        for_loss: Optional[int] = 0,
        for_reaching_max_steps: Optional[int] = 0,
        end_rewards_are_multiplied_by_end_state: Optional[bool] = False,
        reduce_negative_rewards_for_closer_fails: Optional[bool] = False,
        function: Optional[str] = 'standard_rewards',
    ) -> None:
        from cyberattacksim.envs.generic.core import reward_functions
        """
        Args:
            for_loss: int 类型（可选），指定蓝色代理在失败时的奖励。
            for_reaching_max_steps: int 类型（可选），指定蓝色代理在达到最大步骤时的奖励。
            end_rewards_are_multiplied_by_end_state: bool 类型（可选），指示游戏结束时的奖励是否乘以蓝色代理控制的百分比。
            reduce_negative_rewards_for_closer_fails: bool 类型（可选），指示如果蓝色代理离游戏结束更近时，是否减少失败的负面奖励。
            function: str 类型（可选），指定奖励计算使用的函数。可以选择内置的方法，也可以自定义方法。
        """

        doc = 'The rewards the blue agent gets for different game states'

        self.for_loss = IntItem(
            value=for_loss,
            doc='Rewards for the blue agent losing',
            properties=IntProperties(allow_null=True, default=0),
            alias='rewards_for_loss',
        )
        self.for_reaching_max_steps = IntItem(
            value=for_reaching_max_steps,
            doc=
            'Rewards for the blue agent winning by reaching the maximum number of steps',
            properties=IntProperties(allow_null=True, default=0),
            alias='rewards_for_reaching_max_steps',
        )
        self.end_rewards_are_multiplied_by_end_state = BoolItem(
            value=end_rewards_are_multiplied_by_end_state,
            doc=
            'How good the end state is (what % blue controls) is multiplied by the rewards that blue receives for winning',
            properties=BoolProperties(allow_null=False, default=False),
            alias='end_rewards_are_multiplied_by_end_state',
        )
        self.reduce_negative_rewards_for_closer_fails = BoolItem(
            value=reduce_negative_rewards_for_closer_fails,
            doc=
            'The negative rewards from the red agent winning are reduced the closer to the end the blue agent gets',
            properties=BoolProperties(allow_null=False, default=False),
            alias='reduce_negative_rewards_for_closer_fails',
        )
        self.function: StrItem = StrItem(
            value=function,
            doc=
            ('There are several built in example reward methods that you can choose from (shown below) '
             'You can also create your own reward method by copying one of the built in methods and calling it here '
             'built in reward methods: standard_rewards, one_per_timestep, safe_nodes_give_rewards, punish_bad_actions'
             ),
            properties=StrProperties(
                default='standard_rewards',
                options=list(reward_functions.__dict__.keys()),
            ),
            alias='reward_function',
        )
        super().__init__(doc)
