from __future__ import unicode_literals

"""
This is literally forked from djangos own loaddata, expect it saves the
object not the serialisation.
It also uses a modified fixture finder that loads everything in the 'aristotle_help_files' directory
"""

import os
import warnings
from itertools import product

from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.db import (
    DEFAULT_DB_ALIAS, DatabaseError, IntegrityError, connections, router,
    transaction,
)
from django.forms.models import model_to_dict
from django.utils._os import upath
from django.utils.encoding import force_text
from django.utils.functional import cached_property

from django.core.management.commands.loaddata import humanize

from django.utils import lru_cache


class Command(BaseCommand):
    help = 'Installs the named help fixture(s) in the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a specific database to load '
            'fixtures into. Defaults to the "default" database.'
        )
        parser.add_argument(
            '--app', action='store', dest='app_label',
            default=None, help='Only look for fixtures in the specified app.'
        )
        parser.add_argument(
            '--ignorenonexistent', '-i', action='store_true',
            dest='ignore', default=False,
            help='Ignores entries in the serialized data for fields that do not '
            'currently exist on the model.'
        )
        parser.add_argument(
            '--update', '-U', action='store_true',
            dest='update', default=False,
            help='Updates existing helps files if they exist.'
        )

    def loadhelp(self, fixture_labels=['aristotle_help_files']):
        connection = connections[self.using]

        # Keep a count of the installed objects and fixtures
        self.fixture_count = 0
        self.loaded_object_count = 0
        self.fixture_object_count = 0
        self.models = set()

        self.serialization_formats = serializers.get_public_serializer_formats()

        # Django's test suite repeatedly tries to load initial_data fixtures
        # from apps that don't have any fixtures. Because disabling constraint
        # checks can be expensive on some database (especially MSSQL), bail
        # out early if no fixtures are found.
        if not self.find_fixtures():
            return

        with connection.constraint_checks_disabled():
            self.load_label()

        # Since we disabled constraint checks, we must manually check for
        # any invalid keys that might have been added
        table_names = [model._meta.db_table for model in self.models]
        try:
            connection.check_constraints(table_names=table_names)
        except Exception as e:
            e.args = ("Problem installing fixtures: %s" % e,)
            raise

        # If we found even one object in a fixture, we need to reset the
        # database sequences.
        if self.loaded_object_count > 0:
            sequence_sql = connection.ops.sequence_reset_sql(no_style(), self.models)
            if sequence_sql:
                if self.verbosity >= 2:
                    self.stdout.write("Resetting sequences\n")
                with connection.cursor() as cursor:
                    for line in sequence_sql:
                        cursor.execute(line)

        if self.verbosity >= 1:
            if self.fixture_count == 0 and self.hide_empty:
                pass
            elif self.fixture_object_count == self.loaded_object_count:
                self.stdout.write("Installed %d object(s) from %d fixture(s)" % (
                    self.loaded_object_count, self.fixture_count)
                )
            else:
                self.stdout.write("Installed %d object(s) (of %d) from %d fixture(s)" % (
                    self.loaded_object_count, self.fixture_object_count, self.fixture_count)
                )

    def handle(self, *fixture_labels, **options):

        self.ignore = options.get('ignore')
        self.using = options.get('database')
        self.app_label = options.get('app_label')
        self.hide_empty = options.get('hide_empty', False)
        self.verbosity = options.get('verbosity')
        self.update = options.get('update')

        with transaction.atomic(using=self.using):
            self.loadhelp()

        # Close the DB connection -- unless we're still in a transaction. This
        # is required as a workaround for an  edge case in MySQL: if the same
        # connection is used to create tables, load data, and query, the query
        # can return incorrect results. See Django #7572, MySQL #37735.
        if transaction.get_autocommit(self.using):
            connections[self.using].close()

    def load_label(self):
        """
        Loads fixtures files for a given label.
        """
        show_progress = self.verbosity >= 3
        for fixture_file, fixture_dir, fixture_name in self.find_fixtures():
            _, ser_fmt = self.parse_name(os.path.basename(fixture_file))
            fixture = open(fixture_file, 'rb')
            try:
                self.fixture_count += 1
                objects_in_fixture = 0
                loaded_objects_in_fixture = 0
                if self.verbosity >= 2:
                    self.stdout.write(
                        "Installing %s fixture '%s' from %s." %
                        (ser_fmt, fixture_name, humanize(fixture_dir))
                    )

                objects = serializers.deserialize(
                    ser_fmt, fixture,
                    using=self.using, ignorenonexistent=self.ignore
                )

                for obj in objects:
                    objects_in_fixture += 1
                    if router.allow_migrate_model(self.using, obj.object.__class__):
                        loaded_objects_in_fixture += 1
                        self.models.add(obj.object.__class__)
                        try:
                            keys = dict([
                                (key, getattr(obj.object, key))
                                for key in obj.object.unique_together
                            ])
                            if self.update:
                                vals = dict([
                                    (k, v)
                                    for k, v in model_to_dict(obj.object).items()
                                    if v is not None
                                    ])

                                item, created = obj.object.__class__.objects.get_or_create(
                                    defaults=vals,
                                    **keys
                                )
                                if not created:
                                    if show_progress:
                                        self.stdout.write(
                                            'Updated an object(s).',
                                            ending=''
                                        )
                                    for k, v in vals.items():
                                        setattr(item, k, v)
                                    item.save()
                            else:
                                if not obj.object.__class__.objects.filter(**keys).exists():
                                    obj.object.save()
                            if show_progress:
                                self.stdout.write(
                                    '\rProcessed %i object(s).' % loaded_objects_in_fixture,
                                    ending=''
                                )
                        except (DatabaseError, IntegrityError) as e:
                            e.args = ("Could not load %(app_label)s.%(object_name)s(pk=%(pk)s): %(error_msg)s" % {
                                'app_label': obj.object._meta.app_label,
                                'object_name': obj.object._meta.object_name,
                                'pk': obj.object.pk,
                                'error_msg': force_text(e)
                            },)
                            raise
                if objects and show_progress:
                    self.stdout.write('')  # add a newline after progress indicator
                self.loaded_object_count += loaded_objects_in_fixture
                self.fixture_object_count += objects_in_fixture
            except Exception as e:
                if not isinstance(e, CommandError):
                    e.args = ("Problem installing fixture '%s': %s" % (fixture_file, e),)
                raise
            finally:
                fixture.close()

            # Warn if the fixture we loaded contains 0 objects.
            if objects_in_fixture == 0:
                warnings.warn(
                    "No fixture data found for '%s'. (File format may be "
                    "invalid.)" % fixture_name,
                    RuntimeWarning
                )

    @lru_cache.lru_cache(maxsize=None)
    def find_fixtures(self, fixture_label='aristotle_help_files'):
        """
        Finds fixture files for a given label.
        """

        fixture_name, ser_fmt = self.parse_name(fixture_label)
        databases = [self.using, None]
        ser_fmts = serializers.get_public_serializer_formats() if ser_fmt is None else [ser_fmt]

        if self.verbosity >= 2:
            self.stdout.write("Loading '%s' fixtures..." % fixture_name)

        if os.path.isabs(fixture_name):
            fixture_dirs = [os.path.dirname(fixture_name)]
        else:
            fixture_dirs = self.fixture_dirs
            if os.path.sep in os.path.normpath(fixture_name):
                fixture_dirs = [os.path.join(dir_, os.path.dirname(fixture_name))
                                for dir_ in fixture_dirs]

        suffixes = (
            '.'.join(ext for ext in combo if ext)
            for combo in product(databases, ser_fmts)
        )

        fixture_name = "*"
        search_name = ""
        targets = set('.'.join((search_name, suffix)) for suffix in suffixes)

        fixture_files = []

        for fixture_dir in fixture_dirs:
            if self.verbosity >= 2:
                self.stdout.write("Checking %s for fixtures..." % humanize(fixture_dir))
            fixture_files_in_dir = []
            for dir_name, sub, candidates in os.walk(fixture_dir):  # , search_name + '*')):
                for candidate in candidates:
                    candidate = os.path.join(dir_name, candidate)
                    if any([os.path.basename(candidate).endswith(t) for t in targets]):
                        # Save the fixture_dir and fixture_name for future error messages.
                        fixture_files_in_dir.append((candidate, fixture_dir, candidate.split('/')[-1]))

            dest_static_dir = os.path.join(settings.STATIC_ROOT, "aristotle_help")
            src = os.path.join(fixture_dir, 'static')
            if not os.path.exists(dest_static_dir):
                os.makedirs(dest_static_dir)
            if os.path.exists(src):
                from distutils import dir_util
                dir_util.copy_tree(src, dest_static_dir)

            # Check kept for backwards-compatibility; it isn't clear why
            # duplicates are only allowed in different directories.
            # Commented out from django
            # if len(fixture_files_in_dir) > 1:
            #    raise CommandError(
            #        "Multiple fixtures named '%s' in %s. Aborting." %
            #        (fixture_name, humanize(fixture_dir)))
            fixture_files.extend(fixture_files_in_dir)

        return fixture_files

    @cached_property
    def fixture_dirs(self):
        """
        Return a list of fixture directories.
        The list contains the 'fixtures' subdirectory of each installed
        application, if it exists, the directories in FIXTURE_DIRS, and the
        current directory.
        """
        dirs = []
        fixture_dirs = settings.FIXTURE_DIRS
        if len(fixture_dirs) != len(set(fixture_dirs)):
            raise ImproperlyConfigured("settings.FIXTURE_DIRS contains duplicates.")
        for app_config in apps.get_app_configs():
            app_label = app_config.label
            app_dir = os.path.join(app_config.path, 'aristotle_help_files')
            if app_dir in fixture_dirs:
                raise ImproperlyConfigured(
                    "'%s' is a default fixture directory for the '%s' app "
                    "and cannot be listed in settings.FIXTURE_DIRS." % (app_dir, app_label)
                )

            if self.app_label and app_label != self.app_label:
                continue
            if os.path.isdir(app_dir):
                dirs.append(app_dir)
        dirs.extend(list(fixture_dirs))
        dirs.append('aristotle_help_files')
        dirs = [upath(os.path.abspath(os.path.realpath(d))) for d in dirs]
        return dirs

    def parse_name(self, fixture_name):
        """
        Splits fixture name in name, serialization format.
        """
        parts = fixture_name.rsplit('.', 1)

        if len(parts) > 1:
            if parts[-1] in self.serialization_formats:
                ser_fmt = parts[-1]
                parts = parts[:-1]
            else:
                raise CommandError(
                    "Problem installing fixture '%s': %s is not a known "
                    "serialization format." % (''.join(parts[:-1]), parts[-1]))
        else:
            ser_fmt = None

        name = '.'.join(parts)

        return name, ser_fmt
