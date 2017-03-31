import argparse
from os.path import isfile, abspath, join, dirname


class Arguments:

    def __init__(self):
        self.arguments = self.parse()

    def parse(self):
        parser = argparse.ArgumentParser(description='Perform back-ups from or to remote system(s).')
        parser.add_argument('--config', '-c', dest='config', help='Location of the configuration file (optional)')
        return parser.parse_args()

    @property
    def config_file(self):
        if self.arguments.config:
            if isfile(self.arguments.config):
                return self.arguments.config
        if isfile('/etc/serapeum/backup.ini'):
            return '/etc/serapeum/backup.ini'
        else:
            return abspath(join(dirname(abspath(__file__)), '../../..', 'config', 'config.ini'))
