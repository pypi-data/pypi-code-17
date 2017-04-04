from cloudshell.networking.devices.runners.run_command_runner import RunCommandRunner

from cloudshell.networking.arista.cli.arista_cli_handler import AristaCliHandler


class AristaRunCommandRunner(RunCommandRunner):
    def __init__(self, cli, context, logger, api):
        """Create AristaRunCommandOperations

        :param context: command context
        :param api: cloudshell api object
        :param cli: CLI object
        :param logger: QsLogger object
        :return:
        """

        super(AristaRunCommandRunner, self).__init__(logger)
        self._cli_handler = AristaCliHandler(cli, context, logger, api)
