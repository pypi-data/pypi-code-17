from serapeum.backup import config
from serapeum.backup.modules.backends.generic import GenericRole


class DuplicityRole(GenericRole):
    def __init__(self, sources_file, scheme, user, host, port=None, password=None, path=None, encrypt_key=None,
                 passphrase=None, excludes_file=None, remote_role='backup', delete_older_than=None):
        self.c = config
        self.remote = self.url(scheme, user, password, host, port, path)
        self.encrypt_key = encrypt_key
        self.passphrase = passphrase

        self.sources = self.p__parse_sources_file(sources_file)

        self.excludes = []
        if excludes_file:
            self.excludes = self.p__parse_sources_file(excludes_file)

    @property
    def destination(self):
        return self.remote

    @property
    def source(self):
        return '/'

    @property
    def command(self):
        command = [
            self.c.config['SYSTEM']['duplicity_path'],
            '-v4'
        ]
        if self.encrypt_key:
            command += ['--encrypt-key', self.encrypt_key]

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

    def run(self):
        # Set the passphrase in the environment
        if self.passphrase:
            env = {
                'PASSPHRASE': self.passphrase
            }
        else:
            env = None
        self.p__run(self.command, env=env)
        return True

    def url(self, scheme, user, password, host, port, path):
        return '{scheme}://{user}{password}{host}{port}{path}'.format(
            scheme=scheme,
            user=user if user else '',
            password=':{0}'.format(password) if password else '',
            host='@{0}'.format(host) if host else '',
            port=':{0}'.format(port) if port else '',
            path='/{0}'.format(path) if path else ''
        )
