import ipaddress as ipa
from typing import Dict, List, Optional, Union

from .network_object import NetworkObject


class Router(NetworkObject):

    def __init__(
        self,
        name: str,
        firewall_rules: Optional[List[Dict[str, Union[str, int]]]] = None,
        **kwargs,
    ):
        """Initializes a Router object.

        :param str name: The name of the router.
        :param Optional[List[Dict[str, Union[str, int]]]] firewall_rules: List of firewall rules.
            If no rules are provided, the default behavior is to allow all traffic.
            Example:
                [
                    {
                        'name': 'https',
                        'src': 'some_subnet',
                        'port': 443,
                        'proto': 'tcp',
                        'desc': 'Allow all src to all dest on dest port 443'
                    },
                    {
                        'name': 'foo',
                        'src': 'some_host',
                        'port': 3128,
                        'proto': 'tcp',
                        'desc': 'Allow some_host to use foo service'
                    }
                ]
        """
        super().__init__(name,
                         firewall_rules if firewall_rules is not None else [])
        self.default_route: Optional[Union[ipa.IPv4Address,
                                           ipa.IPv6Address]] = None
        self.interfaces: Dict[str, Union[ipa.IPv4Address,
                                         ipa.IPv6Address]] = {}

    def __str__(self) -> str:
        return (
            f'Router(name="{self.name}", default_route="{self.default_route}", '
            f'routes="{self.routes}")')

    def __repr__(self) -> str:
        return (
            f'Router(name={self.name!r}, default_route={self.default_route!r}, '
            f'routes={self.routes!r}, firewall_rules={self.firewall_rules!r})')

    def get_default_route(
            self) -> Optional[Union[ipa.IPv4Address, ipa.IPv6Address]]:
        """Returns the default route of the router.

        :return: The default route IP address or None if not set.
        """
        return self.default_route

    def set_interface_ip(self, interface_name: str,
                         ip: Union[ipa.IPv4Address, ipa.IPv6Address]) -> None:
        """Sets the IP address for a given interface.

        :param str interface_name: The name of the interface.
        :param Union[ipa.IPv4Address, ipa.IPv6Address] ip: The IP address to be assigned to the interface.
        """
        self.interfaces.update({interface_name: ip})

    def get_interface_ip(
        self, interface_name: str
    ) -> Optional[Union[ipa.IPv4Address, ipa.IPv6Address]]:
        """Retrieves the IP address of a given interface.

        :param str interface_name: The name of the interface.
        :return: The IP address associated with the interface, or None if not set.
        """
        return self.interfaces.get(interface_name)

    def add_subnet_interface(self, subnet) -> None:
        """Adds a subnet interface to the router and assigns an IP address to
        it.

        :param subnet: The subnet object from which to obtain an available IP address.
        """
        if hasattr(subnet, 'available_ips') and subnet.available_ips:
            ip = subnet.available_ips.pop(0)
            self.set_interface_ip(subnet.name, ip)
        else:
            raise ValueError(
                'The subnet does not have available IPs or the attribute is missing.'
            )
