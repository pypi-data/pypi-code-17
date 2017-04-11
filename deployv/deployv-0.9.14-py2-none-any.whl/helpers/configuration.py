import os
import logging
import ConfigParser

_logger = logging.getLogger(__name__)


class DeployvConfig(object):

    def __init__(self, config=None):
        self.config = self.parse_config(config)

    def parse_config(self, additional_config_file=None):
        """Loads and returns the parsed config files in a ConfigParser object.

        The config files are loaded in this order:

        1. /etc/deployv/deployv.conf
        2. /etc/deployv/conf.d/*.conf
        3. ~/.config/deployv/deployv.conf
        4. ~/.config/deployv/conf.d/*.conf
        5. All files received in additional_config_files.

        :param additional_config_file: Additional .conf file to load.
        :type additional_config_files: String

        :returns: The parsed config files.
        :rtype: ConfigParser.ConfigParser
        """
        config_files = []
        main_dirs = ['/etc/deployv', os.path.expanduser('~/.config/deployv')]
        for main_dir in main_dirs:
            main_config_file = os.path.join(main_dir, 'deployv.conf')
            if os.access(main_config_file, os.F_OK):
                config_files.append(main_config_file)
            addons_dir = os.path.join(main_dir, 'conf.d')
            if os.path.isdir(addons_dir):
                for filename in os.listdir(addons_dir):
                    filepath = os.path.join(addons_dir, filename)
                    if os.path.isfile(filepath) and filename.endswith('.conf'):
                        config_files.append(filepath)
        if additional_config_file:
            config_files.append(additional_config_file)
        if config_files:
            _logger.info("Loading config files: %s", ", ".join(config_files))
            config = ConfigParser.ConfigParser()
            loaded_files = config.read(config_files)
            if len(config_files) != len(loaded_files):
                _logger.warn("Error loading config files: %s",
                             ", ".join(set(config_files) - set(loaded_files)))
        return config
