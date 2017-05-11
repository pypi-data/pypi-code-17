#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.runners.state_runner import StateRunner
from cloudshell.firewall.juniper.junos.cli.juniper_cli_handler import JuniperCliHandler
from cloudshell.firewall.juniper.junos.flows.juniper_shutdown_flow import JuniperShutdownFlow


class JuniperStateRunner(StateRunner):
    def __init__(self, cli, logger, api, resource_config):
        """
        :param cli:
        :param logger:
        :param api:
        :param resource_config:
        """

        super(JuniperStateRunner, self).__init__(logger, api, resource_config)
        self.cli = cli
        self.api = api

    @property
    def cli_handler(self):
        return JuniperCliHandler(self.cli, self.resource_config, self._logger, self.api)

    def shutdown(self):
        """ Shutdown device """

        juniper_shutdown_flow = JuniperShutdownFlow(self.cli_handler, self._logger)
        juniper_shutdown_flow.execute_flow()
