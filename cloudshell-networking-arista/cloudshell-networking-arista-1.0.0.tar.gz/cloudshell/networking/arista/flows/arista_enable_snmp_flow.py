from cloudshell.networking.devices.flows.cli_action_flows import EnableSnmpFlow
from cloudshell.snmp.snmp_parameters import SNMPV2Parameters

from cloudshell.networking.arista.command_actions.enable_disable_snmp_actions import EnableDisableSnmpActions


class AristaEnableSnmpFlow(EnableSnmpFlow):
    def __init__(self, cli_handler, logger):
        """
        Enable snmp flow
        :param cli_handler:
        :type cli_handler: JuniperCliHandler
        :param logger:
        :return:
        """
        super(AristaEnableSnmpFlow, self).__init__(cli_handler, logger)
        self._cli_handler = cli_handler

    def execute_flow(self, snmp_parameters):
        if not isinstance(snmp_parameters, SNMPV2Parameters):
            message = 'Unsupported SNMP version'
            self._logger.error(message)
            raise Exception(self.__class__.__name__, message)

        if not snmp_parameters.snmp_community:
            message = 'SNMP community cannot be empty'
            self._logger.error(message)
            raise Exception(self.__class__.__name__, message)

        snmp_community = snmp_parameters.snmp_community
        with self._cli_handler.config_mode_service() as cli_service:
            snmp_actions = EnableDisableSnmpActions(cli_service, self._logger)
            if not snmp_actions.configured(snmp_community):
                self._logger.debug('Configuring SNMP with community {}'.format(snmp_community))
                return snmp_actions.enable_snmp(snmp_community)
