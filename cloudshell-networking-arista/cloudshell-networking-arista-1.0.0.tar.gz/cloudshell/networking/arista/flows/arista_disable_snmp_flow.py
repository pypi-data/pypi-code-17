from cloudshell.networking.devices.flows.cli_action_flows import DisableSnmpFlow

from cloudshell.networking.arista.command_actions.enable_disable_snmp_actions import EnableDisableSnmpActions


class AristaDisableSnmpFlow(DisableSnmpFlow):
    def __init__(self, cli_handler, logger):
        """
          Enable snmp flow
          :param cli_handler:
          :type cli_handler: JuniperCliHandler
          :param logger:
          :return:
          """
        super(AristaDisableSnmpFlow, self).__init__(cli_handler, logger)
        self._cli_handler = cli_handler

    def execute_flow(self):
        with self._cli_handler.config_mode_service() as cli_service:
            snmp_actions = EnableDisableSnmpActions(cli_service, self._logger)
            self._logger.debug('Disable SNMP')
            snmp_actions.disable_snmp()
