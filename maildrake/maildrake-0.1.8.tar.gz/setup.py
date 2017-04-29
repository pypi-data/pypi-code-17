# setup.py
# Part of Mail Drake, an email server for development and testing.
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Distribution setup for Mail Drake application. """

import distutils.command.build
import distutils.command.clean
import distutils.core
import os
import os.path
import pydoc
import sys
import unittest

from setuptools import (setup, find_packages)


if sys.version_info < (3,):
    print("Mail Drake requires Python 3 or later.")
    sys.exit(1)


main_module_name = 'maildrake'
main_module_fromlist = ['_metadata']
main_module = __import__(
        main_module_name,
        level=0, fromlist=main_module_fromlist)
metadata = main_module._metadata

version_file_path = os.path.join(os.path.dirname(__file__), "VERSION")
version_text = metadata.get_version_text(version_file_path)

(synopsis, long_description) = pydoc.splitdoc(pydoc.getdoc(main_module))


def test_suite():
    """ Make the test suite for this code base. """
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.curdir, pattern='test_*.py')
    return suite


class BuildVersionCommand(distutils.core.Command):
    """ Distutils command to build the version data file. """

    description = "Build the version data file for the package."

    version_data_file_path = os.path.join(
            os.path.dirname(main_module.__file__),
            "VERSION")

    def initialize_options(self):
        self.output_file_path = None

    def finalize_options(self):
        if self.output_file_path is None:
            self.output_file_path = self.version_data_file_path

    def run(self):
        with open(self.output_file_path, 'w') as outfile:
            outfile.write("{version}\n".format(version=version_text))


class BuildCommand(distutils.command.build.build):
    """ Custom ‘build’ command that also invokes ‘build_version’. """

    sub_commands = distutils.command.build.build.sub_commands
    sub_commands.insert(0, ('build_version', None))


class CleanVersionCommand(distutils.core.Command):
    """ Distutils command to clean the generated version data file. """

    description = "Clean the version data file for the package."

    def initialize_options(self):
        self.build_version_data_file_path = None

    def finalize_options(self):
        self.set_undefined_options(
                'build_version',
                ('output_file_path', 'build_version_data_file_path'),
                )

    def run(self):
        try:
            os.remove(self.build_version_data_file_path)
        except FileNotFoundError:
            # File already does not exist; we're done.
            pass


class CleanCommand(distutils.command.clean.clean):
    """ Custom ‘clean’ command that also cleans our generated files. """

    sub_commands = distutils.command.clean.clean.sub_commands
    sub_commands.insert(0, ('clean_version', None))

    def run(self):
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)
        super().run()


setup_args = dict(
        name=metadata.distribution_name,
        version=version_text,
        packages=find_packages(exclude=["test"]),
        package_data={
            main_module_name: [
                'VERSION'
                'web/static/css/*',
                'web/static/images/*',
                'web/templates/*',
                'store/*.sql',
                ],
            },
        cmdclass={
            "build": BuildCommand,
            "build_version": BuildVersionCommand,
            "clean": CleanCommand,
            "clean_version": CleanVersionCommand,
            },

        # Setuptools metadata.
        zip_safe=False,
        setup_requires=[
            "docutils",
            "semver",
            ],
        test_suite='setup.test_suite',
        tests_require=[
            "testtools",
            "testscenarios >=0.4",
            "Faker",
            "docutils",
            "semver",
            "sqlparse",
            "fasteners",
            "Flask",
            ],
        install_requires=[
            "setuptools",
            # Docutils is only required for building, but Setuptools
            # can't distinguish dependencies properly.
            # See <URL:https://github.com/pypa/setuptools/issues/457>.
            "docutils",
            "semver",
            "sqlparse",
            "fasteners",
            "Flask",
            ],
        entry_points={
            'console_scripts': [
                'maildrake-store = maildrake.store.manage:main',
                'maildrake-smtp = maildrake.smtp.service:main',
                'maildrake-web = maildrake.web.service:main',
                ],
            },

        # PyPI metadata.
        author=metadata.author_name,
        author_email=metadata.author_email,
        description=synopsis,
        license=metadata.license,
        keywords="email smtp queue debug".split(),
        url=metadata.url,
        long_description=long_description,
        classifiers=[
            # Reference: https://pypi.python.org/pypi?:action=list_classifiers
            "Development Status :: 4 - Beta",
            (
                "License :: OSI Approved ::"
                " GNU Affero General Public License v3 or later (AGPLv3+)"),
            "Operating System :: POSIX",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "Topic :: Communications :: Email :: Mail Transport Agents",
            "Topic :: Software Development :: Testing",
            ],
        )


if __name__ == '__main__':
    setup(**setup_args)


# Copyright © 2008–2017 Ben Finney <ben+python@benfinney.id.au>
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
