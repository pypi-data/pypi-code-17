"""Python CLI for Microsoft SQL."""
# Copyright (C) 2016 Russell Troxel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import io
import sys

from os import path

from mssqlcli import __version__

from setuptools import setup
from setuptools.command.test import test

here = path.abspath(path.dirname(__file__))


class Tox(test):
    """TestCommand to run ``tox`` via setup.py."""

    def finalize_options(self):
        """Finalize options from args."""
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Actually Run Tests."""
        # import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


def read(*filenames, **kwargs):
    """
    Read file contents into string.

    Used by setup.py to concatenate long_description.

    :param string filenames: Files to be read and concatenated.
    :rtype: string

    """
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        if path.splitext(filename)[1] == ".md":
            try:
                import pypandoc
                buf.append(pypandoc.convert_file(filename, 'rst'))
                continue
            except:
                with io.open(filename, encoding=encoding) as f:
                    buf.append(f.read())
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


setup(
    name='mssqlcli',
    version=__version__,
    description=('Python CLI for Microsoft SQL.'),
    long_description=read("README.md", "CONTRIBUTING.md", "CHANGELOG.rst"),

    # The project's main homepage.
    url='https://github.com/rtrox/mssqlcli',

    # Author details
    author='Russell Troxel',
    author_email='russelltroxel@gmail.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: System Administrators',

        'Topic :: Database :: Front-Ends',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'
    ],

    keywords=['microsoft', 'sql', 'mssql'],

    packages=['mssqlcli', 'mssqlcli.drivers'],
    package_dirs={
        'mssqlcli': 'mssqlcli',
        'mssqlcli.drivers': 'mssqlcli/drivers'
    },

    install_requires=[
        'pymssql',
        'PyYAML',
        'pygments',
        'click',
        'keyring',
        'prettytable',
        'jinja2'
    ],
    tests_require=['tox', 'virtualenv'],
    cmdclass={'test': Tox},

    entry_points={
        'console_scripts': [
            'mssqlcli=mssqlcli.cli:cli',
        ],
    },
)
