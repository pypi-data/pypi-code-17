from cloudshell.networking.arista.cli.arista_cli_handler import AristaCliHandler
from cloudshell.networking.devices.runners.firmware_runner import FirmwareRunner

from cloudshell.networking.arista.flows.arista_load_firmware_flow import AristaLoadFirmwareFlow


class AristaFirmwareRunner(FirmwareRunner):
    RELOAD_TIMEOUT = 500

    def __init__(self, cli, logger, api, context):
        """Handle firmware upgrade process

        :param CLI cli: Cli object
        :param qs_logger logger: logger
        :param CloudShellAPISession api: cloudshell api object
        :param ResourceCommandContext context: command context
        """

        super(AristaFirmwareRunner, self).__init__(logger)
        self._cli_handler =  AristaCliHandler(cli, context, logger, api)
        self._load_firmware_flow = AristaLoadFirmwareFlow(self._cli_handler, self._logger)
