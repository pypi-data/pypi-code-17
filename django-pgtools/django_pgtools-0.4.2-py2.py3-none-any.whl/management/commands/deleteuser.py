# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from django.core.management.base import BaseCommand

from pgtools.dbrole import DatabaseRole
from pgtools.dbuser import DatabaseUser
from pgtools.decorators import graceful_db_errors
from pgtools.utils import (
    DJANGO_VERSION,
    check_database_engine,
    parse_username_and_rolename,
)


class Command(BaseCommand):
    help = 'Delete an existing database user based on given role.'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        if DJANGO_VERSION < (1, 8):
            self.args = "username [rolename]"

    def add_arguments(self, parser):
        # positional arguments
        parser.add_argument(
            'username', metavar='username', nargs=1,
            help='Username for the new user.')
        parser.add_argument(
            'rolename', metavar='rolename', nargs='?',
            help='Role to use for creating the new user.')

    @graceful_db_errors
    def handle(self, *args, **options):
        check_database_engine()
        username, rolename = parse_username_and_rolename(*args, **options)

        role = DatabaseRole(rolename)
        user = DatabaseUser(username, create=False)

        role.revoke(user)
        user.delete()

        print("User '{}' deleted successfully.".format(username))
