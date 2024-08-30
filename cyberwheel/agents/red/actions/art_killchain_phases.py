import random

import cyberwheel.agents.red.art_techniques as art_techniques
from cyberwheel.agents.red.actions import ARTAction, RedActionResults
from cyberwheel.network import Host


class ARTKillChainPhase(ARTAction):
    """Base class for defining a KillChainPhase.

    Any new Killchain Phase (probably not needed) should inherit from this
    class.
    """

    validity_mapping = {
        # OS-based technique mapping (as shown in the original code)
    }

    def __init__(
        self,
        src_host: Host = None,
        target_host: Host = None,
        valid_techniques: list[str] = [],
    ) -> None:
        """Initialize with the source host, target host, and valid
        techniques."""
        super().__init__(src_host, target_host)
        self.valid_techniques = valid_techniques

    def sim_execute(self) -> RedActionResults:
        """Simulate the execution of a kill chain phase."""
        self.action_results.detector_alert.add_src_host(self.src_host)
        host = self.target_host
        host_os = host.os
        self.action_results.modify_alert(dst=host)

        if len(self.valid_techniques) > 0:
            self.action_results.add_successful_action()
            mitre_id = random.choice(self.valid_techniques)
            art_technique = art_techniques.technique_mapping[mitre_id]

            processes = []
            valid_tests = [
                at for at in art_technique.atomic_tests
                if host_os in at.supported_platforms
            ]
            chosen_test = random.choice(valid_tests)

            # Execute prerequisite commands, main commands, and cleanup commands
            for dep in chosen_test.dependencies:
                processes.extend(dep.get_prerequisite_command)
                processes.extend(dep.prerequisite_command)
            if chosen_test.executor is not None:
                processes.extend(chosen_test.executor.command)
                processes.extend(chosen_test.executor.cleanup_command)

            for p in processes:
                host.run_command(chosen_test.executor, p, 'root')

            self.action_results.add_metadata(
                host.name,
                {
                    'commands': processes,
                    'mitre_id': mitre_id,
                    'technique': art_technique.name,
                },
            )

        return self.action_results


class ARTPingSweep(ARTKillChainPhase):
    """PrivilegeEscalation Killchain Phase Attack. As described by MITRE:

    The adversary is trying to gain higher-level permissions.

    Privilege Escalation consists of techniques that adversaries use to gain higher-level permissions on a system or network.
    """

    name: str = 'pingsweep'

    def __init__(self, src_host: Host, target_host: Host) -> None:
        super().__init__(src_host, target_host)
        self.name = 'pingsweep'

    def sim_execute(self) -> RedActionResults:
        """Simulate the execution of a ping sweep attack."""
        self.action_results.detector_alert.add_src_host(self.src_host)
        host = self.target_host
        self.action_results.modify_alert(dst=host)

        host_os = host.os
        art_technique = art_techniques.technique_mapping['T1018']
        mitre_id = art_technique.mitre_id
        processes = []

        # Select a valid atomic test for the host's OS
        valid_tests = [
            at for at in art_technique.atomic_tests
            if host_os in at.supported_platforms
        ]
        chosen_test = random.choice(valid_tests)

        # Execute prerequisite commands, main commands, and cleanup commands
        for dep in chosen_test.dependencies:
            processes.extend(dep.get_prerequisite_command)
            processes.extend(dep.prerequisite_command)
        if chosen_test.executor is not None:
            processes.extend(chosen_test.executor.command)
            processes.extend(chosen_test.executor.cleanup_command)
        for p in processes:
            host.run_command(chosen_test.executor, p, 'user')

        self.action_results.add_successful_action()
        self.action_results.add_metadata(
            host.name,
            {
                'commands': processes,
                'mitre_id': mitre_id,
                'technique': art_technique.name,
            },
        )

        # Perform the ping sweep by discovering hosts in the same subnet
        subnet_hosts = host.subnet.connected_hosts
        interfaces = []
        self.action_results.add_metadata(host.subnet.name,
                                         {'subnet_scanned': host.subnet})
        for each_host in subnet_hosts:
            for h in each_host.interfaces:
                interfaces.append(h)
        for h in interfaces:
            self.action_results.add_metadata(h.name, {'ip_address': h})

        return self.action_results


class ARTPortScan(ARTKillChainPhase):
    """PrivilegeEscalation Killchain Phase Attack. As described by MITRE:

    The adversary is trying to gain higher-level permissions.

    Privilege Escalation consists of techniques that adversaries use to gain higher-level permissions on a system or network.
    """

    name: str = 'portscan'

    def __init__(self, src_host: Host, target_host: Host) -> None:
        super().__init__(src_host, target_host)
        self.name = 'portscan'

    def sim_execute(self) -> RedActionResults:
        """Simulate the execution of a port scan attack."""
        self.action_results.detector_alert.add_src_host(self.src_host)
        host = self.target_host
        self.action_results.modify_alert(dst=host)

        host_os = host.os
        art_technique = art_techniques.technique_mapping['T1046']
        mitre_id = art_technique.mitre_id
        processes = []

        # Select a valid atomic test for the host's OS
        valid_tests = [
            at for at in art_technique.atomic_tests
            if host_os in at.supported_platforms
        ]
        chosen_test = random.choice(valid_tests)

        # Execute prerequisite commands, main commands, and cleanup commands
        for dep in chosen_test.dependencies:
            processes.extend(dep.get_prerequisite_command)
            processes.extend(dep.prerequisite_command)
        if chosen_test.executor is not None:
            processes.extend(chosen_test.executor.command)
            processes.extend(chosen_test.executor.cleanup_command)
        for p in processes:
            host.run_command(chosen_test.executor, p, 'user')

        self.action_results.add_successful_action()
        self.action_results.add_metadata(
            host.name,
            {
                'commands': processes,
                'mitre_id': mitre_id,
                'technique': art_technique.name,
            },
        )

        return self.action_results


class ARTPrivilegeEscalation(ARTKillChainPhase):
    """PrivilegeEscalation Killchain Phase Attack. As described by MITRE:

    The adversary is trying to gain higher-level permissions.

    Privilege Escalation consists of techniques that adversaries use to gain higher-level permissions on a system or network.
    Adversaries can often enter and explore a network with unprivileged access but require elevated permissions to follow
    through on their objectives. Common approaches are to take advantage of system weaknesses, misconfigurations, and
    vulnerabilities.
    """

    name: str = 'privilege-escalation'

    def __init__(self,
                 src_host: Host,
                 target_host: Host,
                 valid_techniques: list[str] = []) -> None:
        super().__init__(src_host,
                         target_host,
                         valid_techniques=valid_techniques)
        self.name = 'privilege-escalation'


class ARTDiscovery(ARTKillChainPhase):
    """Discovery Killchain Phase Attack. As described by MITRE:

    The adversary is trying to figure out your environment.

    Discovery consists of techniques an adversary may use to gain knowledge about the system and internal network.
    These techniques help adversaries observe the environment and orient themselves before deciding how to act.
    They also allow adversaries to explore what they can control and what's around their entry point in order to
    discover how it could benefit their current objective. Native operating system tools are often used toward
    this post-compromise information-gathering objective.
    """

    name: str = 'discovery'

    def __init__(self,
                 src_host: Host,
                 target_host: Host,
                 valid_techniques: list[str] = []) -> None:
        super().__init__(src_host,
                         target_host,
                         valid_techniques=valid_techniques)
        self.name = 'discovery'

    def sim_execute(self):
        super().sim_execute()
        if self.action_results.attack_success:
            self.action_results.add_metadata(
                self.target_host.name,
                {'type': self.target_host.host_type.name},
            )
        return self.action_results


class ARTLateralMovement(ARTKillChainPhase):
    """LateralMovement Killchain Phase Attack. As described by MITRE:

    The adversary is trying to move through your environment.

    Lateral Movement consists of techniques that adversaries use to enter and control remote systems on a network.
    Following through on their primary objective often requires exploring the network to find their target and
    subsequently gaining access to it. Reaching their objective often involves pivoting through multiple systems
    and accounts to gain. Adversaries might install their own remote access tools to accomplish Lateral Movement
    or use legitimate credentials with native network and operating system tools, which may be stealthier.
    """

    name: str = 'lateral-movement'

    def __init__(self,
                 src_host: Host,
                 target_host: Host,
                 valid_techniques: list[str] = []) -> None:
        super().__init__(src_host,
                         target_host,
                         valid_techniques=valid_techniques)
        self.name = 'lateral-movement'


class ARTImpact(ARTKillChainPhase):
    """Impact Killchain Phase Attack. As described by MITRE:

    The adversary is trying to manipulate, interrupt, or destroy your systems and data.

    Impact consists of techniques that adversaries use to disrupt availability or compromise integrity by manipulating business and
    operational processes. Techniques used for impact can include destroying or tampering with data. In some cases, business processes
    can look fine, but may have been altered to benefit the adversaries' goals. These techniques might be used by adversaries to follow
    through on their end goal or to provide cover for a confidentiality breach.
    """

    name: str = 'impact'

    def __init__(self,
                 src_host: Host,
                 target_host: Host,
                 valid_techniques: list[str] = []) -> None:
        super().__init__(src_host,
                         target_host,
                         valid_techniques=valid_techniques)
        self.name = 'impact'
