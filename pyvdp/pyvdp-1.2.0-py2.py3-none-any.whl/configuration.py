"""
Configuration management is done through reading configuration file. The location if configuration file is defined
with **PYVDP_CONFIG** environment variable, containing absolute path and file name of logfile, e.g.
/home/user/pyvdp/configuration.ini

Configuration file is a standard INI-file with sections, keys and their corresponding values.

If no configuration file found or configuration file is invalid, :func:`~pyvdp.configuration.PyvdpConfigurationError`
exception is raised.

**Usage:**

..  code-block:: ini
 
    [VISA]
    url = {Visa Developer Program API Enpoint URL, e.g. https://sandbox.api.visa.com}
    username = {your VDP app username}
    password = {your VDP app password}
    version = v1
    cert = {path and filename to certificate file, relative to configuration file directory}
    key = {path and filename to key file, relative to configuration file directory}
    loglevel = DEBUG
    logfile = pyvdp.log
"""
import os

try:
    import configparser as parser
except ImportError:
    import ConfigParser as parser

DEFAULT_CONFIG = {
    'url': 'https://sandbox.api.visa.com',
    'username': '',
    'password': '',
    'version': 'v1',
    'cert': '',
    'key': '',
    'loglevel': 'ERROR',
    'logfile': 'pyvdp.log',
    'shared_secret': '',
    'api_key': ''
}


def get_config(config_path=None):
    """Validates configuration file.

    :param config_path: **Optional**. Full path to configuration file including filename. Default is PYVDP_CONFIG env
        variable value or `configuration.ini` file in current directory. 
    :return: configuration
    """
    if os.getenv('PYVDP_TEST_MODE'):
        return DEFAULT_CONFIG

    if not config_path:
        config_path = os.getenv('PYVDP_CONFIG', os.path.join(os.path.dirname(__file__), 'configuration.ini'))

    # config file existence
    if not os.path.exists(config_path):
        message = "Could not find configuration file in %s. " \
                  "See \"Configuration\" chapter in docs for details." % config_path
        raise PyvdpConfigurationError(message)

    config = parser.ConfigParser()
    config.read(config_path)

    configuration = DEFAULT_CONFIG
    config_dict = dict(config.items('VISA'))

    configuration.update(config_dict)

    return configuration


class PyvdpConfigurationError(Exception):
    """Raised with invalid configuration"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
