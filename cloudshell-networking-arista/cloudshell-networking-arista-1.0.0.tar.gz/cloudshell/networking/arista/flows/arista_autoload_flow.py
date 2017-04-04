from cloudshell.networking.devices.flows.snmp_action_flows import AutoloadFlow

from cloudshell.networking.arista.autoload.arista_snmp_autoload import AristaSNMPAutoload


class AristaAutoloadFlow(AutoloadFlow):
    def execute_flow(self, supported_os, resource_name):
        with self._snmp_handler.get_snmp_service() as snmp_service:
            arista_snmp_autoload = AristaSNMPAutoload(snmp_handler=snmp_service,
                                                      logger=self._logger,
                                                      resource_name=resource_name)
            return arista_snmp_autoload.discover(supported_os)
