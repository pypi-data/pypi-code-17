from os.path import isfile
from .exception import ConfigFileNotFoundExcetion
import ruamel.yaml
from ruamel.yaml import RoundTripLoader
import logging


config = None


def override(_):
    """ marker method """
    return _


def make_config(name, dirs):
    global config
    for file in ('%s/%s' % (dir, name) for dir in dirs):
        if isfile(file):
            config = ruamel.yaml.load(open(file, 'rt').read(), RoundTripLoader)
            return config, file

    raise ConfigFileNotFoundExcetion(dirs)


def print_meta(config_file_url):
    log = logging.getLogger("contactcenter.configuration")
    log.info(f"load configuration from {config_file_url}")
