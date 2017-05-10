import logging
import logging.config
import os
from os.path import expanduser
import yaml
import io
from jinja2 import Template


def configure_logging(app_name, custom_format=None):
    """
    Function for configuring logging, input parametar is application name, 
    log will be saved cwd/app_name.log or data/logs/app_name.log if service 
    is on server machine.
    :param app_name: Name of app(wanted name for logger, Buttercup etc)
    :param custom_format: Custom formatter for logger, see logging doc for 
    example
    """
    home = expanduser("~")
    production = os.path.join(home, "data/logs")
    if os.path.exists(production):
        app_path = os.path.join(production, '{}.log'.format(app_name))
    else:
        cwd = os.getcwd()
        app_path = os.path.join(cwd, '{}.log'.format(app_name))
    formatter = 'simple'
    if custom_format:
        formatter = 'custom'
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'log.yml')
    with io.open(conf_path, 'rt') as f:
        template = Template(f.read())
        dict_conf = yaml.safe_load(template.render(ppg_path=app_path,
                                                   formatter=formatter,
                                                   custom_format=custom_format))
    logging.config.dictConfig(dict_conf)
