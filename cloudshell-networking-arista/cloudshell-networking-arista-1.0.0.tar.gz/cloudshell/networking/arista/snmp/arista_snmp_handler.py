from cloudshell.networking.arista.cli.arista_cli_handler import AristaCliHandler
from cloudshell.networking.arista.flows.arista_disable_snmp_flow import AristaDisableSnmpFlow
from cloudshell.networking.snmp_handler import SnmpHandler

from cloudshell.networking.arista.flows.arista_enable_snmp_flow import AristaEnableSnmpFlow


class AristaSnmpHandler(SnmpHandler):
    def __init__(self, cli, context, logger, api):
        super(AristaSnmpHandler, self).__init__(context, logger)
        self._cli = cli
        self._api = api

    @property
    def arista_cli_handler(self):
        return AristaCliHandler(self._cli, self._context, self._logger, self._api)

    def _create_enable_flow(self):
        return AristaEnableSnmpFlow(self.arista_cli_handler, self._logger)

    def _create_disable_flow(self):
        return AristaDisableSnmpFlow(self.arista_cli_handler, self._logger)
