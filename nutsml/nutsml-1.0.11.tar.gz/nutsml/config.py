"""
.. module:: config
   :synopsis: Handling of configuration files.
"""

import os
import yaml


class ConfigDict(dict):
    """
    Dictionary that allows access via keys or attributes.

    Used to store and access configuration data.
    """

    def __init__(self, *args, **kwargs):
        """
        Create dictionary.

        >>> contact = ConfigDict({'age':13, 'name':'stefan'})
        >>> contact['age']
        13

        >>> contact.name
        'stefan'

        :param args: See dict
        :param kwargs: See dict
        """
        super(ConfigDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def load_config(filename):
    """
    Load configuration file in YAML format.

    The search order for the config file is:
    1) user home dir
    2) current dir
    3) full path
    
    |  Example file: 'tests/data/config.yaml'
    |  filepath : c:/Maet
    |  imagesize : [100, 200]

    >>> cfg = load_config('tests/data/config.yaml')
    >>> cfg.filepath
    'c:/Maet'

    >>> cfg['imagesize']
    [100, 200]

    :param filename: Name or full path of configuration file.
    :return: dictionary with config data. Note that config data can be
             accessed by key or attribute, e.g. cfg.filepath or cfg.['filepath']
    :rtype: ConfigDict
    """
    filepaths = []
    for dirpath in os.path.expanduser('~'), os.curdir, '':
        try:
            filepath = os.path.join(dirpath, filename)
            filepaths.append(filepath)
            with open(filepath, 'r') as f:
                return ConfigDict(yaml.load(f))
        except IOError:
            pass
    raise IOError('Configuration file not found: ' + ', '.join(filepaths))
