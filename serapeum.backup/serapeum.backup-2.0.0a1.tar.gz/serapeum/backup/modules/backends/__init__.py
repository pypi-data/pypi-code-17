from serapeum.backup.modules.backends.duplicity import DuplicityRole as Duplicity
from serapeum.backup.modules.backends.rdiff import RdiffRole as Rdiff
from serapeum.backup.modules.log import logger
from serapeum.backup import config


class Backend:

    def __init__(self, backend, **kwargs):
        self.__backend = backend
        o_backend = eval(self.__backend)
        self.backend = o_backend(**self.options, **kwargs)
        self.cmd_output = ''

    @property
    def options(self):
        options = {
            'remote_role': config.config['BACKUP']['remote_role'],
            'sources_file': config.config['BACKUP']['sources_file'],
            'excludes_file': config.config['BACKUP']['excludes_file']
        }
        backend_header = 'BACKEND_{0}'.format(self.__backend.upper())

        for key, value in config.config.items(backend_header):
            options[key] = value

        return options

    def run(self):
        if self.options['remote_role'] == 'backup':
            logger.info('Performing backup to {0}::{1}.'.format(self.options['host'],
                                                                self.options['path']))
        elif self.options['remote_role'] == 'source':
            logger.info('Performing backup of {0} to {1}.'.format(self.options['host'],
                                                                self.options['path']))
        try:
            self.backend.run()
        except Exception as e:
            self.cmd_output = self.backend.cmd_output
            raise e
        self.cmd_output = self.backend.cmd_output
        return True
