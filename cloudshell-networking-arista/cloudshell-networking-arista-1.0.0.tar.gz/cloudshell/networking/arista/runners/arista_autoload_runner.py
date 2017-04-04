from cloudshell.networking.arista.flows.arista_autoload_flow import AristaAutoloadFlow
from cloudshell.networking.devices.runners.autoload_runner_new import AutoloadRunner

from cloudshell.networking.arista.snmp.arista_snmp_handler import AristaSnmpHandler


class AristaAutoloadRunner(AutoloadRunner):
    def __init__(self, cli, logger, context, api, supported_os):
        super(AristaAutoloadRunner, self).__init__(context, supported_os)
        self._cli = cli
        self._api = api
        self._logger = logger

    @property
    def snmp_handler(self):
        return AristaSnmpHandler(self._cli, self._context, self._logger, self._api)

    def create_autoload_flow(self):
        return AristaAutoloadFlow(self.snmp_handler, self._logger)
