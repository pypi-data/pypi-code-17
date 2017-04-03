"""Parse sections from the configuration file."""

from __future__ import print_function

from configparser import ConfigParser
import sys

EMAIL_SECTION_NAME = 'Email'
AWS_SECTION_NAME = 'AWS '


class ConfigLine(object):
    """Configuration line item class."""

    def __init__(self, name, required=True, default=None):
        """Initialize a configuration line item.

        Args:
            name (str): The name of the configuration item.
            required (Optional bool): Whether the configuration is required or
                not.
            default (Optional): If the configuration is not required, the
                default value.
        """
        self.name = name
        self.required = required
        self.default = default


def parse_aws_config(section, config_parser):
    """Parse AWS account configurations.

    Args:
        section (str): The AWS account section from the config file.
        config_parser (ConfigParser): The ConfigParser object with the config
            file loaded.

    Returns:
        aws_config (dict): A dict of an AWS account configuration loaded from
            the config file.
    """
    allowed_aws_options = [
        ConfigLine('aws_access_key_id', True),
        ConfigLine('aws_secret_access_key', True),
        ConfigLine('region', False, 'us-east-1'),
        ConfigLine('rds', False, True),
        ConfigLine('elasticache', False, True)
    ]

    aws_config = {
        'name': section
    }

    for option in allowed_aws_options:
        if option.required and not config_parser.has_option(
                section, option.name):
            print('Required configuration option for an AWS account ({}) '
                  'in section "{}" is not configured!'.format(
                      option.name, section))
            sys.exit(-1)

        if config_parser.has_option(section, option.name):
            aws_config[option.name] = config_parser.get(section, option.name)
        else:
            aws_config[option.name] = option.default

    return aws_config


def parse_config(filename):
    """Parse the configuration file.

    Args:
        filename (str): A filesystem location to the config file.

    Returns:
        config (dict): A dictionary containing the loaded configurations from
            file.
    """
    config_parser = ConfigParser()
    config = {}
    config_parser.read_file(open(filename))

    if config_parser.has_section(EMAIL_SECTION_NAME):
        config['Email'] = parse_email_config(config_parser)

    config_sections = config_parser.sections()
    if config_sections:
        aws_sections = []
        for section in config_sections:
            if AWS_SECTION_NAME in section:
                aws_config = parse_aws_config(section, config_parser)
                aws_sections.append(aws_config)
                config['Accounts'] = aws_sections

        if aws_sections:
            return config

    print('Please specify at least one [AWS ] section in the configuration '
          'file!')
    sys.exit(-1)


def parse_email_config(config_parser):
    """Parse email configuration for sending the report via email.

    Args:
        config_parser (ConfigParser): The ConfigParser object with the config
            file loaded.

    Returns:
        email_config (dict): A dict containing the email configuration.
    """
    email_config = {}

    allowed_email_options = [
        ConfigLine('smtp_host', True),
        ConfigLine('smtp_port', False, 25),
        ConfigLine('smtp_user', False, None),
        ConfigLine('smtp_password', False, None),
        ConfigLine('smtp_recipients', True),
        ConfigLine('smtp_sendas', False, 'root@localhost'),
        ConfigLine('smtp_tls', False, False)
    ]

    for option in allowed_email_options:
        if option.required and not config_parser.has_option(
                EMAIL_SECTION_NAME, option.name):
            print('Required configuration option for email ({}) is not '
                  'configured!'.format(option.name))
            sys.exit(-1)

        if config_parser.has_option(EMAIL_SECTION_NAME, option.name):
            email_config[option.name] = config_parser.get(
                EMAIL_SECTION_NAME, option.name)
        else:
            email_config[option.name] = option.default

    return email_config
