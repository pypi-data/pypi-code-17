# maildrake/store/tests/test_manage.py
# Part of Mail Drake, an email server for development and testing.
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Unit tests for `manage` module. """

import argparse
import io
import os
import sys
import types
import unittest
import unittest.mock

import faker
import testscenarios

import maildrake
import maildrake.store
import maildrake.store.manage


fake_factory = faker.Faker()


class ArgumentParser_TestCase(unittest.TestCase):
    """ Test cases for class `ArgumentParser`. """

    def setUp(self):
        """ Set up test fixtures. """
        self.instance = maildrake.store.manage.ArgumentParser()
        super().setUp()

    def test_instantiate(self):
        """ New `ArgumentParser` instance should be created. """
        self.assertIsNotNone(self.instance)

    def test_has_default_description(self):
        """ Should have default descripion value. """
        expected_description = "Mail Drake message store management tool"
        self.assertEqual(self.instance.description, expected_description)

    def test_has_specified_description(self):
        """ Should have default descripion value. """
        test_description = fake_factory.paragraph()
        self.instance = maildrake.store.manage.ArgumentParser(
                description=test_description)
        expected_description = test_description
        self.assertEqual(self.instance.description, expected_description)

    def test_has_expected_argument_definitions(self):
        """ Should have expected argument definitions. """
        expected_argument_dests = [
                'command',
                'database_file_path',
                ]
        argument_dests = [
                arg.dest for arg in self.instance._actions]
        for dest in expected_argument_dests:
            with self.subTest(argument_dest=dest):
                self.assertIn(dest, argument_dests)


class ArgumentParser_parse_args_TestCase(unittest.TestCase):
    """ Test cases for method `ArgumentParser.parse_args`. """

    def setUp(self):
        """ Set up test fixtures. """
        super().setUp()
        self.patch_program_name()
        self.instance = maildrake.store.manage.ArgumentParser(
            prog=self.test_program_name)

    def patch_program_name(self):
        """ Patch the program command name in the command-line arguments. """
        self.test_program_name = fake_factory.word()
        fake_argv = list(sys.argv)
        fake_argv[0] = self.test_program_name

        attribute_patcher = unittest.mock.patch.object(
            sys, 'argv', new=fake_argv)
        attribute_patcher.start()
        self.addCleanup(attribute_patcher.stop)

    @unittest.mock.patch.object(sys, 'stdout', new_callable=io.StringIO)
    def test_help_option_emits_help_text(
            self,
            fake_stdout,
            ):
        """ Should emit help text when ‘--help’ option. """
        expected_output = "usage: {program}".format(
                program=self.test_program_name)
        for option in ["-h", "--help"]:
            with self.subTest(option=option):
                test_command_args = [option]
                with self.assertRaises(SystemExit):
                    self.instance.parse_args(test_command_args)
                self.assertIn(expected_output, fake_stdout.getvalue())

    @unittest.mock.patch.object(sys, 'stdout', new_callable=io.StringIO)
    def test_help_option_raises_systemexit(
            self,
            fake_stdout,
            ):
        """ Should raise SystemExit when ‘--help’ option. """
        for option in ["-h", "--help"]:
            with self.subTest(option=option):
                test_command_args = [option]
                with self.assertRaises(SystemExit):
                    self.instance.parse_args(test_command_args)

    @unittest.mock.patch.object(sys, 'stdout', new_callable=io.StringIO)
    def test_version_option_emits_program_version(
            self,
            fake_stdout,
            ):
        """ Should emit help text when ‘--version’ option. """
        test_command_args = ["--version"]
        with self.assertRaises(SystemExit):
            self.instance.parse_args(test_command_args)
        expected_output = "{program} {version}\n".format(
                program=self.test_program_name,
                version=maildrake._metadata.version_text)
        self.assertEqual(expected_output, fake_stdout.getvalue())

    @unittest.mock.patch.object(sys, 'stdout', new_callable=io.StringIO)
    def test_version_option_raises_systemexit(
            self,
            fake_stdout,
            ):
        """ Should raise SystemExit when ‘--version’ option. """
        test_command_args = ["--version"]
        with self.assertRaises(SystemExit):
            self.instance.parse_args(test_command_args)


def setup_MessageStoreManager_fixture(testcase):
    """ Set up a test fixture for `MessageStoreManager`.

        :param testcase:
            Instance of `TestCase` to which the fixture should be
            added. Must have a `test_app_class` attribute which will
            be used to instantiate the test fixture.
        :return: ``None``.

        """
    testcase.test_app = testcase.test_app_class()


class MessageStoreManager_TestCase(unittest.TestCase):
    """ Test cases for class `MessageStoreManager`. """

    test_command_name = fake_factory.word()

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        self.test_app_class = maildrake.store.manage.MessageStoreManager
        setup_MessageStoreManager_fixture(self)

    def test_instantiate(self):
        """ Should create a `MessageStoreManager` instance. """
        self.assertIsNotNone(self.test_app)


class MessageStoreManager_parse_commandline_TestCase(unittest.TestCase):
    """ Test cases for class `MessageStoreManager.parse_commandline`. """

    test_command_name = fake_factory.word()

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        self.test_app_class = maildrake.store.manage.MessageStoreManager
        setup_MessageStoreManager_fixture(self)

        self.test_args = {
                'argv': [self.test_command_name],
                }

    def test_requires_argv(self):
        """ Should require commandline args list. """
        self.test_args = dict()
        with self.assertRaises(TypeError):
            self.test_app.parse_commandline(**self.test_args)

    def test_init_parses_args(self):
        """ MessageStoreManager should parse commandline args list. """
        argv = self.test_args['argv']
        args_return = argv[1:]

        mock_parser = unittest.mock.Mock(name='ArgumentParser')
        fake_args = types.SimpleNamespace(
                database_file_path=fake_factory.file_name(),
                command=fake_factory.word(),
                )
        mock_parser.parse_args.return_value = fake_args

        with unittest.mock.patch.object(
                maildrake.store.manage, 'ArgumentParser'
                ) as mock_ArgumentParser_class:
            mock_ArgumentParser_class.return_value = mock_parser
            self.test_app.parse_commandline(**self.test_args)
        mock_parser.parse_args.assert_called_once_with(args_return)

    def test_init_sets_specified_args(self):
        """
        MessageStoreManager should set the specified commandline arguments.
        """
        test_database_file_path = fake_factory.file_name()
        test_command = fake_factory.word()
        test_argv = [
                "progname",
                "--database", test_database_file_path,
                test_command,
                ]
        self.test_args.update(argv=test_argv)
        self.test_app.parse_commandline(**self.test_args)
        expected_args = argparse.Namespace(
                database_file_path=test_database_file_path,
                command=test_command,
                )
        self.assertEqual(self.test_app.args, expected_args)


class MessageStoreManager_parse_commandline_ErrorTestCase(
        testscenarios.WithScenarios,
        unittest.TestCase):
    """ Error test cases for class `MessageStoreManager.parse_commandline`. """

    test_command_name = fake_factory.word()

    scenarios = [
            ('args-zero', {
                'test_argv': [],
                'expected_error': IndexError,
                }),
            ('args-three', {
                'test_argv': [test_command_name, "foo", "bar"],
                'expected_error': SystemExit,
                }),
            ]

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        self.test_app_class = maildrake.store.manage.MessageStoreManager
        setup_MessageStoreManager_fixture(self)

        self.test_args = {
                'argv': self.test_argv,
                }

    def test_init_rejects_incorrect_commandline_args_count(self):
        """ Should reject incorrect count of commandline args. """
        with unittest.mock.patch.object(sys, 'stderr'):
            with self.assertRaises(self.expected_error):
                self.test_app.parse_commandline(**self.test_args)


class MessageStoreManager_run_TestCase(unittest.TestCase):
    """ Test cases for method `MessageStoreManager.run`. """

    test_command_name = fake_factory.word()

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        self.test_app_class = maildrake.store.manage.MessageStoreManager
        setup_MessageStoreManager_fixture(self)

        self.test_app.args = argparse.Namespace(
                command=self.test_command_name,
                )

    def test_run_performs_required_steps(self):
        """ Should invoke the specified command. """
        self.test_app.args.command = "init"

        func_patcher = unittest.mock.patch.object(self.test_app, 'do_init')
        with func_patcher as mock_func:
            self.test_app.run()
        mock_func.assert_called_once_with()


@unittest.mock.patch.object(maildrake.store.manage, 'sqlite')
class MessageStoreManager_do_init_TestCase(unittest.TestCase):
    """ Test cases for method `MessageStoreManager.do_init`. """

    test_command_name = "init"

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        self.test_app_class = maildrake.store.manage.MessageStoreManager
        setup_MessageStoreManager_fixture(self)

        self.test_app.args = argparse.Namespace(
                command=self.test_command_name,
                database_file_path=fake_factory.file_name(),
                )

    def test_calls_sqlite_connect_with_expected_args(
            self,
            mock_sqlite_module,
    ):
        """ Should call `sqlite.connect` with expected arguments. """
        self.test_app.do_init()
        expected_database_file_path = self.test_app.args.database_file_path
        mock_sqlite_module.connect.assert_called_with(
                expected_database_file_path)

    def test_calls_sqlite_get_schema_with_expected_args(
            self,
            mock_sqlite_module,
    ):
        """
        Should call `sqlite.get_schema` with expected arguments.
        """
        self.test_app.do_init()
        mock_sqlite_module.get_schema.assert_called_with()

    def test_calls_sqlite_init_with_expected_args(
            self,
            mock_sqlite_module,
    ):
        """ Should call `sqlite.init` with expected arguments. """
        self.test_app.do_init()
        expected_connection = mock_sqlite_module.connect.return_value
        expected_schema = mock_sqlite_module.get_schema.return_value
        mock_sqlite_module.init.assert_called_with(
                expected_connection, expected_schema)


@unittest.mock.patch.object(maildrake.store.manage, 'MessageStoreManager')
class main_TestCase(unittest.TestCase):
    """ Test cases for function `main`. """

    test_command_name = fake_factory.word()

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()
        self.test_args = {
                'argv': [self.test_command_name],
                }

    def test_calls_app_parse_commandline_with_specified_argv(
            self,
            mock_app_class,
    ):
        """ Should call app's `parse_commandline` method with `argv`. """
        maildrake.store.manage.main(**self.test_args)
        expected_app = mock_app_class.return_value
        expected_argv = self.test_args['argv']
        expected_app.parse_commandline.assert_called_with(expected_argv)

    def test_calls_app_parse_commandline_with_commandline_argv(
            self,
            mock_app_class,
    ):
        """ Should call app's `parse_commandline` method with `sys.argv`. """
        del self.test_args['argv']
        with unittest.mock.patch.object(sys, 'argv') as mock_sys_argv:
            maildrake.store.manage.main(**self.test_args)
            expected_argv = mock_sys_argv
        expected_app = mock_app_class.return_value
        expected_app.parse_commandline.assert_called_with(expected_argv)

    def test_calls_app_run(
            self,
            mock_app_class,
    ):
        """ Should call app's `run` method. """
        maildrake.store.manage.main(**self.test_args)
        expected_app = mock_app_class.return_value
        expected_app.run.assert_called_with()

    def test_returns_status_okay_when_no_error(
            self,
            mock_app_class,
    ):
        """ Should return “okay” exit status when no error. """
        result = maildrake.store.manage.main(**self.test_args)
        expected_result = os.EX_OK
        self.assertEqual(result, expected_result)

    def test_returns_exit_status_when_parse_commandline_systemexit(
            self,
            mock_app_class,
    ):
        """ Should return exit status from `parse_commandline` SystemExit. """
        expected_app = mock_app_class.return_value
        test_exit_status = fake_factory.pyint()
        test_exception = SystemExit(test_exit_status)
        with unittest.mock.patch.object(
                expected_app, 'parse_commandline',
                side_effect=test_exception):
            result = maildrake.store.manage.main(**self.test_args)
        expected_result = test_exit_status
        self.assertEqual(result, expected_result)

    def test_returns_exit_status_when_run_systemexit(
            self,
            mock_app_class,
    ):
        """ Should return exit status from `run` SystemExit. """
        expected_app = mock_app_class.return_value
        test_exit_status = fake_factory.pyint()
        test_exception = SystemExit(test_exit_status)
        with unittest.mock.patch.object(
                expected_app, 'run',
                side_effect=test_exception):
            result = maildrake.store.manage.main(**self.test_args)
        expected_result = test_exit_status
        self.assertEqual(result, expected_result)


# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation; version 3 of that license or any later version.
# No warranty expressed or implied. See the file ‘LICENSE.AGPL-3’ for details.


# Local variables:
# coding: utf-8
# mode: python
# End:
# vim: fileencoding=utf-8 filetype=python :
