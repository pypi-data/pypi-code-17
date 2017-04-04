import re

from cloudshell.cli.cli_service_impl import CliServiceImpl as CliService
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor

from cloudshell.networking.arista.command_templates.arista_configuration_templates import ENABLE_SNMP, SHOW_SNMP_COMMUNITY, DISABLE_SNMP


class EnableDisableSnmpActions(object):
    def __init__(self, cli_service, logger):
        """
        Reboot actions
        :param cli_service: config mode cli service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """
        self._cli_service = cli_service
        self._logger = logger

    def configured(self, snmp_community):
        """
        Check snmp community configured
        :param snmp_community:
        :return:
        """
        s = CommandTemplateExecutor(self._cli_service, SHOW_SNMP_COMMUNITY).execute_command()
        return 'Community name: %s' % snmp_community in s

    def enable_snmp(self, snmp_community):
        """
        Enable snmp on the device
        :return:
        """

        return CommandTemplateExecutor(self._cli_service, ENABLE_SNMP).execute_command(snmp_community=snmp_community)

    def disable_snmp(self):
        """
        Disable SNMP
        :return:
        """
        output = ''
        show = CommandTemplateExecutor(self._cli_service, SHOW_SNMP_COMMUNITY).execute_command()
        output += show
        m = re.search(r'Community name: (\S+)', show)
        if m:
            snmp_community = m.groups()[0]
            output += CommandTemplateExecutor(self._cli_service, DISABLE_SNMP).execute_command(snmp_community=snmp_community)
        else:
            s = '(SNMP was already disabled)'
            self._logger.warn(s)
            output += s
        return output
