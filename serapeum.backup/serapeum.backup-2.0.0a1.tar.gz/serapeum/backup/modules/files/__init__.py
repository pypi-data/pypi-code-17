from serapeum.backup.modules.log import logger

from serapeum.backup.modules.backends import Backend


##
# TODO
# Make destination OK
# Use configuration file OK
# Implement delete-older-than OK
# Logger OK


class Files:

    def __init__(self, backend, host=None, delete_older_than=None):
        self.backend = Backend(backend, host=host, delete_older_than=delete_older_than).backend
        self.cmd_output = ''

    def run(self):
        return self.backend.run()
