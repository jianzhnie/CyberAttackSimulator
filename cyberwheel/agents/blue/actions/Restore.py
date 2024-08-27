from typing import Dict

import BlueActionReturn
import HostAction

from cyberwheel.agents.blue.blue_action import HostAction
from cyberwheel.network.host import Host
from cyberwheel.network.network_base import Network


class Restore(HostAction):

    def __init__(self, network: Network, configs: Dict[str, any],
                 **kwargs) -> None:
        super().__init__(network, configs)

    def execute(self, host: Host, **kwargs) -> BlueActionReturn:
        if host.restored:
            return BlueActionReturn("", False)

        host.remove_process("malware.exe")
        host.restored = True

        return BlueActionReturn("", True)
