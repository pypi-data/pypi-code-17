# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

import sys
from getpass import getpass
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from pgtools.dbrole import DatabaseRole
from pgtools.dbuser import DatabaseUser
from pgtools.decorators import graceful_db_errors
from pgtools.utils import (
    DJANGO_VERSION,
    check_database_engine,
    parse_username_and_rolename,
)


class Command(BaseCommand):
    help = 'Create a new database user based on an existing role.'
    OPTIONS = [
        (('-p', '--password'),
         dict(default=None, dest='password',
              help='Password of the user to be created.')),
        (('-P', '--no-password'),
         dict(default=False, dest='no_password',
              help='If given, then no password is set up for the user.')),
    ]

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        if DJANGO_VERSION < (1, 8):
            self.args = "username [rolename]"
            self.option_list = BaseCommand.option_list + tuple(
                make_option(*a, **kw) for (a, kw) in self.OPTIONS
            )

    def add_arguments(self, parser):
        # positional arguments
        parser.add_argument(
            'username', metavar='username', nargs=1,
            help='Username for the new user.')
        parser.add_argument(
            'rolename', metavar='rolename', nargs='?',
            help='Role to use for creating the new user.')

        # named arguments
        for (args, kwargs) in self.OPTIONS:
            parser.add_argument(*args, **kwargs)

    def _ask_password(self):
        password = None
        try:
            while True:
                if password is None:
                    password = getpass('Password: ')
                    password2 = getpass('Password (again): ')
                    if password != password2:
                        sys.stderr.write(
                            "Error: Your passwords didn't match.\n")
                        password = None
                        continue
                if password.strip() == '':
                    sys.stderr.write("Error: Blank passwords aren't allowed.\n")
                    password = None
                    continue
                break
        except KeyboardInterrupt:
            raise CommandError('Cancelled.')

        return password

    @graceful_db_errors
    def handle(self, *args, **options):
        check_database_engine()
        username, rolename = parse_username_and_rolename(*args, **options)

        password = options.get('password')
        no_password = options.get('no_password')
        if not no_password and password is None:
            self._ask_password()

        role = DatabaseRole(rolename)
        user = DatabaseUser(username, password)
        role.grant(user)

        print("User '{}' created successfully based on role '{}'.".format(
            username, rolename))
