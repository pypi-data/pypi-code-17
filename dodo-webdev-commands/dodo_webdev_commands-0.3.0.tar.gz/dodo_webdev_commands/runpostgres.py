# noqa
from dodo_commands.extra.standard_commands import DodoCommand


class Command(DodoCommand):  # noqa
    help = ""
    decorators = ["docker"]
    docker_options = [
        '--name=pg',
    ]

    def _remove_option(self, key, option):
        options = self.config.get('DOCKER', {}).get(key, [])
        if option in options:
            options.remove(option)

    def handle_imp(self, **kwargs):  # noqa
        self._remove_option('extra_options', '--link=pg')
        self._remove_option('link_list', 'pg')

        self.docker_options.append(
            '--volumes-from=%s' % self.get_config("/DOCKER/database_volume")
        )

        self.runcmd(
            [
                "sudo", "-u", "postgres",
                "/usr/lib/postgresql/9.5/bin/postgres",
                "-D" "/var/lib/postgresql/9.5/main",
                "-c", "config_file=/etc/postgresql/9.5/main/postgresql.conf",
            ],
            cwd="/"
        )
