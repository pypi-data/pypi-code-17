from cloudshell.networking.devices.runners.state_runner import StateRunner

from cloudshell.networking.arista.cli.arista_cli_handler import AristaCliHandler


class AristaStateRunner(StateRunner):
    def __init__(self, cli, logger, api, context):
        """

        :param cli:
        :param logger:
        :param api:
        :param context:
        """

        super(AristaStateRunner, self).__init__(logger, api, context)
        self._cli_handler = AristaCliHandler(cli, context, logger, api)
