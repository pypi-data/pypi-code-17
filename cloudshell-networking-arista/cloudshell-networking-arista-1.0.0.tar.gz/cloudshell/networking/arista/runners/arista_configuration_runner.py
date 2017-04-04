from cloudshell.networking.devices.runners.configuration_runner import ConfigurationRunner

from cloudshell.networking.arista.cli.arista_cli_handler import AristaCliHandler
from cloudshell.networking.arista.flows.cisco_restore_flow import CiscoRestoreFlow
from cloudshell.networking.arista.flows.cisco_save_flow import CiscoSaveFlow


class AristaConfigurationRunner(ConfigurationRunner):
    def __init__(self, cli, logger, context, api):
        super(AristaConfigurationRunner, self).__init__(logger, context, api)
        self._cli_handler = AristaCliHandler(cli, context, logger, api)
        self._save_flow = CiscoSaveFlow(cli_handler=self._cli_handler,
                                        logger=self._logger)
        self._restore_flow = CiscoRestoreFlow(cli_handler=self._cli_handler,
                                              logger=self._logger)
        self.file_system = 'flash:'
