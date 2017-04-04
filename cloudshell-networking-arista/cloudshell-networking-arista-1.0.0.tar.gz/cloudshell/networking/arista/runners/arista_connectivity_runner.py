from cloudshell.networking.devices.runners.connectivity_runner import ConnectivityRunner

from cloudshell.networking.arista.cli.arista_cli_handler import AristaCliHandler
from cloudshell.networking.arista.flows.cisco_add_vlan_flow import CiscoAddVlanFlow
from cloudshell.networking.arista.flows.cisco_remove_vlan_flow import CiscoRemoveVlanFlow


class AristaConnectivityRunner(ConnectivityRunner):
    def __init__(self, cli, logger, api, context):
        """
        Handle add/remove vlan flows

        :param cli:
        :param logger:
        :param api:
        :param context:
        """

        super(AristaConnectivityRunner, self).__init__(logger)
        self._cli_handler =  AristaCliHandler(cli, context, logger, api)
        self.add_vlan_flow = CiscoAddVlanFlow(cli_handler=self._cli_handler,
                                              logger=self._logger)
        self.remove_vlan_flow = CiscoRemoveVlanFlow(cli_handler=self._cli_handler,
                                                    logger=self._logger)
