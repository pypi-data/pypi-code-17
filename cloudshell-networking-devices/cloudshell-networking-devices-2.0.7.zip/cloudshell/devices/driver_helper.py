#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading

from cloudshell.cli.cli import CLI
from cloudshell.cli.session_pool_manager import SessionPoolManager
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.shell.core.session.logging_session import LoggingSessionContext
from cloudshell.snmp.snmp_parameters import SNMPV2Parameters, SNMPV3Parameters
# from cloudshell.snmp.quali_snmp import QualiSnmp


def get_cli(session_pool_size, pool_timeout=100):
    session_pool = SessionPoolManager(max_pool_size=session_pool_size, pool_timeout=pool_timeout)
    return CLI(session_pool=session_pool)


def get_logger_with_thread_id(context):
    """
    Create QS Logger for command context AutoLoadCommandContext, ResourceCommandContext
    or ResourceRemoteCommandContext with thread name
    :param context:
    :return:
    """
    logger = LoggingSessionContext.get_logger_for_context(context)
    child = logger.getChild(threading.currentThread().name)
    for handler in logger.handlers:
        child.addHandler(handler)
    child.level = logger.level
    for log_filter in logger.filters:
        child.addFilter(log_filter)
    return child


def get_api(context):
    """

    :param context:
    :return:
    """

    return CloudShellSessionContext(context).get_api()


def get_snmp_parameters_from_command_context(resource_config, api):
    """
    :param ResourceCommandContext command_context: command context
    :return:
    """

    if '3' in resource_config.snmp_version:
        return SNMPV3Parameters(ip=resource_config.address,
                                snmp_user=resource_config.snmp_v3_user or '',
                                snmp_password=api.DecryptPassword(resource_config.snmp_v3_password).Value or '',
                                snmp_private_key=resource_config.snmp_v3_private_key or '')
    else:
        return SNMPV2Parameters(ip=resource_config.address,
                                snmp_community=api.DecryptPassword(resource_config.snmp_read_community).Value or '')
                                # snmp_community=resource_config.snmp_read_community or '')


# def get_snmp_handler(resource_config, logger, api):
#     snmp_handler_params = get_snmp_parameters_from_command_context(resource_config, api)
#     return QualiSnmp(snmp_parameters=snmp_handler_params, logger=logger)
