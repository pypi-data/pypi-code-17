# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from django.core.management.base import BaseCommand
from django.db import connection

from pgtools.decorators import graceful_db_errors
from pgtools.utils import (
    DJANGO_VERSION,
    check_database_engine,
    get_models,
    parse_username,
)


GRANT_SQL = "GRANT ALL ON %s TO %s;"
EXISTS_SQL = "SELECT 1 FROM pg_class WHERE relname='%s';"


class Command(BaseCommand):
    help = 'Grant access to user to all models.'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        if DJANGO_VERSION < (1, 8):
            self.args = "username"

    def add_arguments(self, parser):
        # positional arguments
        parser.add_argument(
            'username', metavar='username', nargs=1,
            help='Username for the new user.')

    @graceful_db_errors
    def handle(self, *args, **options):
        check_database_engine()

        self.username = parse_username(*args, **options)
        self.cursor = connection.cursor()

        for model in get_models():
            # grant access to model
            table = model._meta.db_table
            if self._check_exists(table):
                self._grant_one(table)
                if model._meta.has_auto_field:
                    sequence = "%s_%s_seq" % (table,
                                              model._meta.auto_field.column)
                    if self._check_exists(sequence):
                        self._grant_one(sequence)

            # grant access to model relations
            for f in model._meta.many_to_many:
                self._grant_many_to_many(f)

        if not getattr(connection.features, 'uses_autocommit', False):
            connection.connection.commit()

    def _check_exists(self, table_or_sequence):
        sql = EXISTS_SQL % table_or_sequence
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return bool(result)

    def _grant_one(self, table_or_sequence):
        print('Granting access to {}'.format(table_or_sequence))
        sql = GRANT_SQL % (table_or_sequence, self.username)
        self.cursor.execute(sql)

    def _grant_many_to_many(self, field):
        table = field.m2m_db_table()
        self.cursor.execute("select pg_get_serial_sequence('%s', 'id')" %
            table)
        sequence = self.cursor.fetchone()[0]
        self._grant_one(table)
        self._grant_one(sequence)

