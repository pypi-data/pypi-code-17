from os import mkdir
from os.path import isdir

from serapeum.backup import config
from serapeum.backup.modules.backends.generic import GenericRole


class RdiffRole(GenericRole):
    def __init__(self, remote_role, sources_file, path, remote_user, host, remote_ssh, excludes_file=None,
                 delete_older_than=None):
        self.c = config
        self.__remote_role = remote_role
        self.__destination_path = path
        if self.__remote_role == 'source':
            self.__destination_path = '{0}/{1}'.format(host, path)
        self.__remote_user = remote_user
        self.__remote_host = host
        self.sources = self.p__parse_sources_file(sources_file)
        self.excludes = []
        if excludes_file:
            self.excludes = self.p__parse_sources_file(excludes_file)
        self.ssh_key = remote_ssh
        self.delete_older_than = delete_older_than
        self.__cmd_output = ''

    @property
    def destination(self):
        if self.__remote_role == 'source':
            self.create_local_destination()
            return self.__destination_path
        elif self.__remote_role == 'backup':
            self.create_remote_destination()
            return '{user}@{host}::{path}'.format(user=self.__remote_user, host=self.__remote_host,
                                                  path=self.__destination_path)
        else:
            raise Exception('Illegal remote_role specified!')

    @property
    def source(self):
        if self.__remote_role == 'source':
            return '{user}@{host}::/'.format(user=self.__remote_user, host=self.__remote_host)
        elif self.__remote_role == 'backup':
            return '/'
        else:
            raise Exception('Illegal remote_role specified!')

    @property
    def command(self):
        """
            Build the command we will make rdiff-backup run
            :return:
            """
        command = [
            self.c.config['SYSTEM']['rdiff_path'],
            '-v0',
            '--print-statistics',
            '--exclude-special-files',
            '--remote-schema',
            '/usr/bin/ssh -i "{ssh_key}" -C %s "sudo /usr/bin/rdiff-backup --server"'
                .format(ssh_key=self.ssh_key)
        ]
        for d in self.excludes:
            command += ['--exclude', d]
        for d in self.sources:
            command += ['--include', d]
        command += [
            '--exclude',
            '**',
            self.source,
            self.destination
        ]
        return command

    def __delete_older(self, delete_older_than):
        command = [
            self.c.config['SYSTEM']['rdiff_path'],
            '-v0',
            '--print-statistics',
            '--remove-older-than',
            delete_older_than
        ]
        if self.__remote_role == 'backup':
            command += [
                '--remote-schema',
                '/usr/bin/ssh -i "{ssh_key}" -C %s "sudo /usr/bin/rdiff-backup --server"'
                    .format(ssh_key=self.ssh_key)
            ]

        command += [
            self.destination
        ]
        return self.p__run(command)

    def create_remote_destination(self):
        command = [
            '/usr/bin/ssh',
            '-i',
            self.ssh_key,
            '{user}@{host}'.format(user=self.__remote_user, host=self.__remote_host),
            '/bin/mkdir -p "{path}"'.format(path=self.__destination_path)
        ]
        self.p__run(command)

    def create_local_destination(self):
        if not isdir(self.__destination_path):
            mkdir(self.__destination_path)

    def run(self):
        self.p__run(self.command)
        if self.delete_older_than is not None:
            # Delete older increments
            self.__delete_older(self.delete_older_than)
        return True
