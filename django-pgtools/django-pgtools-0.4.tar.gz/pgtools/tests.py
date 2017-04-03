# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from __future__ import with_statement

import sys

try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO
from unittest import skipIf

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connection, models
from django.db.backends.postgresql_psycopg2.base import (
    DatabaseWrapper as PGDatabaseWrapper,
)
from django.db.utils import load_backend
from django.test import TransactionTestCase
from django.test.utils import override_settings
from mock import Mock, patch
from psycopg2 import ProgrammingError

from pgtools.dbrole import DatabaseRole
from pgtools.dbuser import DatabaseUser
from pgtools.decorators import graceful_db_errors
from pgtools.management.commands import grantuser
from pgtools.utils import (
    DJANGO_VERSION,
    check_database_engine,
    get_rolename_from_settings,
    parse_rolename,
    parse_username,
    parse_username_and_rolename,
)

EMPTY_ROLE_NAME = 'test_empty_role'
MASTER_ROLE_NAME = 'test_master_role'
TEST_USER_NAME1 = 'test_user1'
TEST_USER_NAME2 = 'test_user2'


class CommandBaseTestCase(TransactionTestCase):

    def setUp(self):
        test_settings = {
            'DATABASE_USER': 'postgres',
            'DATABASE_PASSWORD': '',
        }
        if hasattr(settings, 'DATABASES'):
            test_settings['DATABASES'] = settings.DATABASES.copy()
            test_settings['DATABASES']['default'].update({
                'USER': 'postgres',
                'PASSWORD': '',
            })
        overrides = self.settings(**test_settings)
        overrides.enable()
        self.addCleanup(overrides.disable)

        self._refresh_connection()
        self._capture_stdout_stderr()
        self._create_roles_and_users()

        # Make sure that dummy role doesn't exist before testing starts.
        if DatabaseRole.exists('dummy'):
            DatabaseRole('dummy', create=False).delete()

    def _refresh_connection(self):
        for attname in ['HOST', 'PORT', 'NAME', 'USER', 'PASSWORD']:
            if hasattr(settings, 'DATABASES'):
                attvalue = settings.DATABASES['default'].get(attname, '')
                # need to update the DatabaseWrapper cached settings_dict
                # to keep up to date with the new db setting
                connection.settings_dict[attname] = attvalue
            elif hasattr(connection, 'settings_dict'):
                setting_name = "DATABASE_%s" % attname
                attvalue = getattr(settings, setting_name, '')
                # need to update the DatabaseWrapper cached settings_dict
                # to keep up to date with the new db setting
                connection.settings_dict[setting_name] = attvalue
            else:
                # Django 1.0 doesn't have setting cache, so there's nothing to
                # refresh
                pass
        connection.close()

    def _capture_stdout_stderr(self):
        # patch stdout and stderr to avoid polluting the console
        sys.stdout = BytesIO()
        sys.stderr = BytesIO()

    def _create_roles_and_users(self):
        # Create master role
        if not DatabaseRole.exists(MASTER_ROLE_NAME):
            self.master_role = DatabaseRole(MASTER_ROLE_NAME, create=True)
        else:
            self.master_role = DatabaseRole(MASTER_ROLE_NAME, create=False)
        # Create standalone role (test1)
        if not DatabaseRole.exists(EMPTY_ROLE_NAME):
            self.empty_role = DatabaseRole(EMPTY_ROLE_NAME, create=True)
        else:
            self.empty_role = DatabaseRole(EMPTY_ROLE_NAME, create=False)
        # Create users based on master tole (test2 and test3)
        if not DatabaseUser.exists(TEST_USER_NAME1):
            self.test1 = DatabaseUser(TEST_USER_NAME1, 'testpass', create=True)
        else:
            self.test1 = DatabaseUser(TEST_USER_NAME1, 'testpass', create=False)
        self.master_role.grant(self.test1)

        if not DatabaseUser.exists(TEST_USER_NAME2):
            self.test2 = DatabaseUser(TEST_USER_NAME2, create=True)
        else:
            self.test2 = DatabaseUser(TEST_USER_NAME2, create=False)
        self.master_role.grant(self.test2)

    def tearDown(self):
        self._delete_roles_and_users()
        self._release_stdout_stderr()

    def _delete_roles_and_users(self):
        # clean up everything
        if DatabaseUser.exists(TEST_USER_NAME1):
            if DatabaseRole.exists(MASTER_ROLE_NAME):
                self.master_role.revoke(self.test1)
            self.test1.delete()
        if DatabaseUser.exists(TEST_USER_NAME2):
            if DatabaseRole.exists(MASTER_ROLE_NAME):
                self.master_role.revoke(self.test2)
            self.test2.delete()
        if DatabaseRole.exists(MASTER_ROLE_NAME):
            self.master_role.delete()
        if DatabaseRole.exists(EMPTY_ROLE_NAME):
            self.empty_role.delete()

        # make sure everything has been cleaned up
        self.assertFalse(DatabaseUser.exists(TEST_USER_NAME1))
        self.assertFalse(DatabaseUser.exists(TEST_USER_NAME2))
        self.assertFalse(DatabaseRole.exists(MASTER_ROLE_NAME))
        self.assertFalse(DatabaseRole.exists(EMPTY_ROLE_NAME))

    def _release_stdout_stderr(self):
        # reset stdout/stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


class CommandTestCase(CommandBaseTestCase):

    def test_command_createuser_no_args(self):
        # No argument
        try:
            call_command('createuser')
            self.fail('Calling createuser with no arguments should fail.')
        except (CommandError, SystemExit):
            pass

    def test_command_createuser_existing_user(self):
        # Create an already existing user
        try:
            call_command('createuser', TEST_USER_NAME1, MASTER_ROLE_NAME,
                password='testpass')
            self.fail('Calling createuser with an existing user as an '
                'argument should fail.')
        except (CommandError, SystemExit):
            pass

    @patch('pgtools.management.commands.createuser.getpass')
    def test_command_createuser_passwords_not_match(self, mock_getpass):
        passwords = ['bar', 'foo']
        def get_password(*args):
            return passwords.pop()
        mock_getpass.side_effect = get_password

        # Test the password entry with pexpect - passwords don't match
        try:
            call_command('createuser', 'dummy', MASTER_ROLE_NAME)
        except IndexError:
            # capture end of passwords
            pass
        sys.stderr.seek(0)
        stderr = sys.stderr.read()

        self.assertEqual(stderr,
            "Error: Your passwords didn't match.\n")

    @patch('pgtools.management.commands.createuser.getpass')
    def test_command_createuser_passwords_match(self, mock_getpass):
        mock_getpass.return_value = 'foobar'

        # Matching passwords
        call_command('createuser', 'dummy', MASTER_ROLE_NAME)
        sys.stdout.seek(0)
        stdout = sys.stdout.read()

        self.assertEqual(stdout,
            "User 'dummy' created successfully based on role '%s'.\n" %
            MASTER_ROLE_NAME)

        # Delete the created user
        call_command('deleteuser', 'dummy', MASTER_ROLE_NAME)

    @patch('pgtools.management.commands.createuser.getpass')
    def test_command_createuser_empty_password(self, mock_getpass):
        passwords = [' ', ' ']
        def get_password(*args):
            return passwords.pop()
        mock_getpass.side_effect = get_password

        try:
            call_command('createuser', 'dummy', MASTER_ROLE_NAME)
        except IndexError:
            # capture end of passwords
            pass
        sys.stderr.seek(0)
        stderr = sys.stderr.read()

        self.assertEqual(stderr, "Error: Blank passwords aren't allowed.\n")

    @patch('pgtools.management.commands.createuser.getpass')
    def test_command_createuser_keyboard_interrupt(self, mock_getpass):
        def interrupt(*args):
            raise KeyboardInterrupt()
        mock_getpass.side_effect = interrupt

        try:
            call_command('createuser', 'dummy', MASTER_ROLE_NAME)
            self.fail('Calling createuser should capture '
                      'KeyboardInterrupt exceptions.')
        except SystemExit as err:
            self.assertEqual(str(err), '1')

            sys.stderr.seek(0)
            stderr = sys.stderr.read()

            self.assertTrue('Error: Cancelled.' in stderr)
        except CommandError as err:
            self.assertEqual(str(err), 'Cancelled.')

    @patch('pgtools.management.commands.createuser.getpass')
    def test_command_createuser_repeat_password_input(self, mock_getpass):
        passwords = ['foobar', 'foobar', 'bar', 'foo']
        def get_password(*args):
            return passwords.pop()
        mock_getpass.side_effect = get_password

        # Test repeated password input
        call_command('createuser', 'dummy', MASTER_ROLE_NAME)
        sys.stdout.seek(0)
        stdout = sys.stdout.read()
        sys.stderr.seek(0)
        stderr = sys.stderr.read()

        self.assertEqual(stderr,
            "Error: Your passwords didn't match.\n")
        self.assertEqual(stdout,
            "User 'dummy' created successfully based on "
            "role '%s'.\n" % MASTER_ROLE_NAME)

        # Delete the created user
        call_command('deleteuser', 'dummy', MASTER_ROLE_NAME)

    @patch('pgtools.management.commands.createuser.getpass')
    def test_command_createuser_enter_password(self, mock_getpass):
        mock_getpass.return_value = 'password'
        call_command('createuser', 'dummy', MASTER_ROLE_NAME)
        call_command('deleteuser', 'dummy', MASTER_ROLE_NAME)

    def test_command_listusers(self):
        # No argument, no predefined role
        try:
            call_command('listusers')
            self.fail('Calling listusers with no arguments should fail.')
        except (CommandError, SystemExit):
            pass
        # Role passed as an argument, existing role
        call_command('listusers', MASTER_ROLE_NAME)
        # Role passed as an argument, non-existing role
        try:
            call_command('listusers', 'somefunkynonexistingrole')
            self.fail('Calling listusers with a non-existing role should fail.')
        except (CommandError, SystemExit):
            pass
        # No argument, but existing role predefined
        with self.settings(PG_BASE_ROLE=MASTER_ROLE_NAME):
            call_command('listusers')
        # No argument, non-existing role predefined
        with self.settings(PG_BASE_ROLE='somefunkynonexistingrole'):
            try:
                call_command('listusers')
                self.fail(
                    'Calling listusers without arguments and non-existing role '
                    'predefined should fail.')
            except (CommandError, SystemExit):
                pass
        # Too many arguments
        try:
            call_command('listusers', 'foo', 'bar')
            self.fail(
                'Calling listusers with more than one argument should fail.')
        except (CommandError, SystemExit):
            pass
        # No users exist for the role
        call_command('listusers', EMPTY_ROLE_NAME)

    def test_graceful_db_errors_permission_denied(self):
        @graceful_db_errors
        def test_func():
            err = ProgrammingError()
            err.pgcode = '42501'
            raise err
        try:
            test_func()
            self.fail('No errors raised.')
        except CommandError as err:
            self.assertEqual(str(err),
                'Permission denied: please check DATABASE_* settings.')

    def test_graceful_db_errors_other(self):
        @graceful_db_errors
        def test_func():
            err = ProgrammingError()
            err.pgcode = 100
            raise err
        try:
            test_func()
            self.fail('No errors raised.')
        except Exception as err:
            self.assertEqual(err.pgcode, 100)

    def test_dbrole_create_existing_role(self):
        try:
            DatabaseRole(MASTER_ROLE_NAME, create=True)
            self.fail('Creating an existing role was successful.')
        except CommandError:
            pass

    @patch('pgtools.dbrole.DatabaseRole.exists')
    def test_dbrole_create_fail(self, mock_exists):
        mock_exists.return_value = False
        try:
            DatabaseRole('dummy', create=True)
            self.fail('Creating a role was successful.')
        except CommandError as err:
            self.assertEqual(str(err), "Role couldn't be created: dummy")

    def test_dbrole_get_users(self):
        if not hasattr(self, 'master_role') or not hasattr(self, 'empty_role'):
            self.fail("At least one of 'master_role' or 'empty_role' "
                      "are missing.")
        master_users = self.master_role.get_users()
        empty_users = self.empty_role.get_users()
        self.assertEqual(master_users, [TEST_USER_NAME1, TEST_USER_NAME2])
        self.assertEqual(empty_users, [])

    def test_dbrole_query_missing_role(self):
        try:
            DatabaseRole('somefunkynonexistingrole')
            self.fail("Role shouldn't exist.")
        except CommandError:
            pass

    @patch('pgtools.dbrole.DatabaseRole.exists')
    def test_dbrole_delete_fail(self, mock_exists):
        mock_exists.return_value = True
        try:
            role = DatabaseRole(MASTER_ROLE_NAME)
            role.delete()
            self.fail('Deleting a role was successful.')
        except CommandError as err:
            self.assertEqual(str(err),
                "Role cannot be deleted: %s" % MASTER_ROLE_NAME)

    def test_dbrole_revoke_fail(self):
        try:
            user = Mock()
            user.username = TEST_USER_NAME1
            user.has_role.return_value = True
            role = DatabaseRole(MASTER_ROLE_NAME)
            role.revoke(user)
            self.fail('Revoking a role was successful.')
        except CommandError as err:
            self.assertEqual(str(err),
                "Role cannot be revoked: %s" % MASTER_ROLE_NAME)

    def test_dbuser_create_existing_user(self):
        try:
            DatabaseUser(TEST_USER_NAME1)
            self.fail('Creating an existing user was successful.')
        except CommandError:
            pass

    @patch('pgtools.dbuser.DatabaseUser.exists')
    def test_dbuser_create_fail(self, mock_exists):
        mock_exists.return_value = False
        try:
            DatabaseUser('dummy')
            self.fail('Creating an user was successful.')
        except CommandError as err:
            self.assertEqual(str(err), "User couldn't be created: dummy")

    def test_dbuser_query_missing_user(self):
        try:
            user = DatabaseUser('somefunkynonexistinguser', create=False)
            # Remove the user, so it doesn't get stuck in the DB
            user.delete()
            self.fail("User shouldn't exist.")
        except CommandError:
            pass

    @patch('pgtools.dbuser.DatabaseUser.exists')
    def test_dbuser_delete_fail(self, mock_exists):
        mock_exists.return_value = True
        try:
            user = DatabaseUser(TEST_USER_NAME1, create=False)
            user.delete()
            self.fail('Deleting an user was successful.')
        except CommandError as err:
            self.assertEqual(str(err),
                "User cannot be deleted: %s" % TEST_USER_NAME1)

    def get_backends(self):
        backends = ['django.db.backends.postgresql_psycopg2']
        if DJANGO_VERSION < (1,4):
            backends.insert(0, 'postgresql_psycopg2')
        return backends

    @patch('pgtools.utils.settings')
    def test_utils_check_database_engine_13_style(self, mock_settings):
        dbconfig = {'default': {'NAME': 'mydatabase'}}
        mock_settings.DATABASES = dbconfig
        for engine in self.get_backends():
            dbconfig['default']['ENGINE'] = engine
            mock_settings.DATABASE_ENGINE = 'django.db.backends.sqlite3'
            check_database_engine()
        # Test an unsupported engine
        dbconfig['default']['ENGINE'] = 'django.db.backends.sqlite3'
        mock_settings.DATABASE_ENGINE = 'django.db.backends.postgresql_psycopg2'
        self.assertRaises(CommandError, check_database_engine)

    @patch('pgtools.utils.settings')
    def test_utils_check_database_engine_using_alias(self, mock_settings):
        dbconfig = {
            'default': {'NAME': 'mydatabase',
                        'ENGINE': 'custom_backend'},
            'other': {'NAME': 'myotherdb'},
        }
        mock_settings.DATABASES = dbconfig
        for engine in self.get_backends():
            dbconfig['other']['ENGINE'] = engine
            check_database_engine(alias='other')
        # Test an unsupported engine
        dbconfig['other']['ENGINE'] = 'django.db.backends.sqlite3'
        self.assertRaises(CommandError, check_database_engine, alias='other')

    @patch('pgtools.utils.settings')
    def test_utils_check_database_engine_subclass_13_style(self,
                                                           mock_settings):
        class CustomDatabaseWrapper(PGDatabaseWrapper):
            pass

        dbconfig = {'default': {'NAME': 'mydatabase',
                                'ENGINE': 'custom_backend'}}
        mock_settings.DATABASE_ENGINE = 'custom_backend'
        mock_settings.DATABASES = dbconfig
        def mock_load_backend(name):
            if name == 'custom_backend':
                backend = Mock()
                backend.DatabaseWrapper = CustomDatabaseWrapper
                return backend
            return load_backend(name)

        with patch('pgtools.utils.load_backend', mock_load_backend):
            check_database_engine()

    def test_utils_get_rolename_from_settings(self):
        # Test with default (nothing set)
        self.assertRaises(CommandError, get_rolename_from_settings)
        # Test with the master role
        with self.settings(PG_BASE_ROLE=MASTER_ROLE_NAME):
            master_role_name = get_rolename_from_settings()
            self.assertEqual(master_role_name, MASTER_ROLE_NAME)


@skipIf(DJANGO_VERSION >= (1, 8), 'Django 1.8 and later uses argparse')
class Django17ParserTestCase(CommandBaseTestCase):

    def test_parse_username_and_rolename_no_args(self):
        # Test with no args
        args = []
        self.assertRaises(CommandError, parse_username_and_rolename, args)

    def test_parse_username_and_rolename_two_args(self):
        # Test with two arguments
        args = ['username', 'rolename']
        username, rolename = parse_username_and_rolename(*args)
        self.assertEqual(username, 'username')
        self.assertEqual(rolename, 'rolename')

    def test_parse_username_and_rolename_username_no_role(self):
        # One argument, no predefined base role
        args = ['username']
        self.assertRaises(CommandError, parse_username_and_rolename, *args)

    @override_settings(PG_BASE_ROLE=MASTER_ROLE_NAME)
    def test_parse_username_and_rolename_username_with_role(self):
        # One argument, predefined base role
        args = ['username', 'rolename']
        username, rolename = parse_username_and_rolename(*args)
        self.assertEqual(username, 'username')
        self.assertEqual(rolename, 'rolename')

    def test_parse_username_and_rolename_too_many_args(self):
        args = ['username', 'rolename', 'foo']
        self.assertRaises(CommandError, parse_username_and_rolename, *args)

    def test_parse_username_no_args(self):
        self.assertRaises(CommandError, parse_username)

    def test_parse_username_too_many_args(self):
        args = ['username', 'rolename']
        self.assertRaises(CommandError, parse_username, *args)

    def test_parse_username_from_args(self):
        args = ['username']
        username = parse_username(*args)
        self.assertEqual(username, 'username')

    @override_settings(PG_BASE_ROLE=MASTER_ROLE_NAME)
    def test_parse_rolename_no_args(self):
        rolename = parse_rolename()
        self.assertEqual(rolename, MASTER_ROLE_NAME)

    def test_parse_rolename_too_many_args(self):
        args = ['username', 'rolename']
        self.assertRaises(CommandError, parse_rolename, *args)

    def test_parse_rolename_from_args(self):
        args = ['rolename']
        rolename = parse_rolename(*args)
        self.assertEqual(rolename, 'rolename')



@skipIf(DJANGO_VERSION < (1, 8), 'Django 1.7 and earlier uses optparse')
class Django18ParserTestCase(CommandBaseTestCase):

    def test_parse_username_and_rolename_from_options(self):
        args = ['foo', 'bar']
        options = {'username': 'username', 'rolename': 'rolename'}
        username, rolename = parse_username_and_rolename(*args, **options)
        self.assertEqual(username, 'username')
        self.assertEqual(rolename, 'rolename')

    @override_settings(PG_BASE_ROLE=MASTER_ROLE_NAME)
    def test_parse_username_and_rolename_from_options_with_default_role(self):
        args = ['foo', 'bar']
        options = {'username': 'username'}
        username, rolename = parse_username_and_rolename(*args, **options)
        self.assertEqual(username, 'username')
        self.assertEqual(rolename, MASTER_ROLE_NAME)

    def test_parse_username_from_options(self):
        args = ['foo']
        options = {'username': 'username'}
        username = parse_username(*args, **options)
        self.assertEqual(username, 'username')

    def test_parse_rolename_from_options(self):
        args = ['foo']
        options = {'rolename': 'rolename'}
        rolename = parse_rolename(*args, **options)
        self.assertEqual(rolename, 'rolename')


@skipIf(DJANGO_VERSION < (1, 7), "django.apps not available in Django 1.6")
class GrantUserCommandTestCase(CommandBaseTestCase):

    def get_models(self, app_label):
        from django.apps import apps
        return apps.get_app_config(app_label).get_models()

    def test_command_grantuser_no_args(self):
        try:
            call_command('grantuser')
            self.fail('Calling grantuser with no arguments should fail.')
        except (CommandError, SystemExit):
            pass

    @patch('pgtools.management.commands.grantuser.get_models')
    def test_command_grantuser(self, mock_get_models):
        mock_get_models.return_value = self.get_models('admin')
        command = grantuser.Command
        with patch.object(command, '_grant_one') as mock_grant_one:
            # force the cache to reload the apps
            try:
                call_command('grantuser', 'payments')
            except:
                self.fail('Error while calling grantuser command')

        # assert the grant table method was called on all model tables
        self.assertEqual(mock_grant_one.call_args_list[0],
            (('django_admin_log',), {}))
        # assert the grant sequence method was called on all model
        # sequences
        self.assertEqual(mock_grant_one.call_args_list[1],
            (('django_admin_log_id_seq',), {}))

    @patch('pgtools.management.commands.grantuser.get_models')
    def test_command_grantuser_missing_relations(self, mock_get_models):
        # create table without sequence
        sql = "CREATE TABLE pgtools_foo (id integer PRIMARY KEY);"
        cursor = connection.cursor()
        cursor.execute(sql)

        class Foo(models.Model):
            foo = models.IntegerField()

        mock_get_models.return_value = [Foo]
        command = grantuser.Command
        with patch.object(command, '_grant_one') as mock_grant_one:
            # force the cache to reload the apps
            try:
                call_command('grantuser', 'payments')
            except:
                self.fail('Error while calling grantuser command')

        # assert the grant table method was called on all model tables
        self.assertEqual(mock_grant_one.call_args_list[0],
            (('pgtools_foo',), {}))
        # assert nothing else was processed
        self.assertEqual(len(mock_grant_one.call_args_list), 1)

    @patch('pgtools.management.commands.grantuser.get_models')
    @patch('pgtools.management.commands.grantuser.connection')
    def test__grant_many_to_many(self, mock_connection, mock_get_models):
        mock_connection.cursor.return_value.fetchone.return_value = ['foo']
        mock_get_models.return_value = self.get_models('auth')

        call_command('grantuser', 'payments')

        args_list = mock_connection.cursor.return_value.execute.call_args_list
        calls = [x[0][0] for x in args_list]
        for expected in [
                "select pg_get_serial_sequence('auth_user_groups', 'id')",
                'GRANT ALL ON foo TO payments;'
            ]:
            self.assertTrue(expected in calls)


@skipIf(DJANGO_VERSION > (1, 6), "Django 1.7 and later use django.apps for getting models")
class Django16GrantUserCommandTestCase(GrantUserCommandTestCase):

    def get_models(self, app_label):
        import django.contrib.admin.models
        import django.contrib.auth.models
        from django.db.models.loading import get_models

        if app_label == 'admin':
            models = django.contrib.admin.models
        elif app_label == 'auth':
            models = django.contrib.auth.models
        return get_models(models)
