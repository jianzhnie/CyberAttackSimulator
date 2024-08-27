"""The DFS Impact strategy is to attack the current host until it's impacted,
move to another random unimpacted host, and repeat."""
import random

from cyberwheel.agents.red.strategies.red_strategy import RedStrategy


class DFSImpact(RedStrategy):

    @classmethod
    def select_target(cls, agent_obj):
        """
        If current host has been impacted: choose a random other unimpacted host
        Else: Continue attacking current host
        """
        if (agent_obj.history.hosts[agent_obj.current_host.name].last_step ==
                len(agent_obj.killchain) - 1):
            unimpacted_hosts = [
                h for h, info in agent_obj.history.hosts.items()
                if info.last_step < len(agent_obj.killchain) - 1
            ]
            if len(unimpacted_hosts) > 0:
                target_host_name = random.choice(unimpacted_hosts)
                target_host = agent_obj.history.mapping[target_host_name]
                return target_host
        return agent_obj.current_host

    @classmethod
    def get_reward_map(cls) -> dict[str, tuple[int, int]]:
        return {
            'pingsweep': (-1, 0),
            'portscan': (-1, 0),
            'discovery': (-2, 0),
            'lateral-movement': (-4, 0),
            'privilege-escalation': (-6, 0),
            'impact': (-8, -4),
        }
