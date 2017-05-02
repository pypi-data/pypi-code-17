# -*- coding: utf-8 -*-

"""
   raas_v2.configuration

   This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
import sys
import logging

from .api_helper import APIHelper

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class Configuration(object):

    """A class used for configuring the SDK by a user.

    This class need not be instantiated and all properties and methods
	are accessible without instance creation.

    """

    # An enum for SDK environments
    class Environment(object):
        # Sandbox (Fake) Environment
        SANDBOX = 0
        # Production (Live) Environment
        PRODUCTION = 1
        # Tango Card Internal Use Only
        QA = 2
        # Tango Card Internal Use Only
        GAMMA = 3
        # Tango Card Internal Use Only
        LOCAL = 4

    # An enum for API servers
    class Server(object):
        DEFAULT = 0

    # The environment in which the SDK is running
    environment = Environment.SANDBOX

    # RaaS v2 API Platform Name
    platform_name = 'QAPlatform2'

    # RaaS v2 API Platform Key
    platform_key = 'apYPfT6HNONpDRUj3CLGWYt7gvIHONpDRUYPfT6Hj'

    # All the environments the SDK can run in
    environments = {
        Environment.SANDBOX: {
            Server.DEFAULT: 'https://integration-api.tangocard.com/raas/v2',
        },
        Environment.PRODUCTION: {
            Server.DEFAULT: 'https://api.tangocard.com/raas/v2',
        },
        Environment.QA: {
            Server.DEFAULT: 'https://qa-api.tangocard.com/raas/v2',
        },
        Environment.GAMMA: {
            Server.DEFAULT: 'https://gamma-api.tangocard.com/raas/v2',
        },
        Environment.LOCAL: {
            Server.DEFAULT: 'http://raastango.cc:8080/v2',
        },
    }

    @classmethod
    def get_base_uri(cls, server=Server.DEFAULT):
        """Generates the appropriate base URI for the environment and the server.

        Args:
            server (Configuration.Server): The server enum for which the base URI is required.

        Returns:
            String: The base URI.

        """
        parameters = {
        }
        return APIHelper.append_url_with_template_parameters(cls.environments[cls.environment][server], parameters)
