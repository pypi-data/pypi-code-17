# Ducker - search with DuckDuckGo from the command line

# Copyright (C) 2016-2017 Jorge Maldonado Ventura <jorgesumle@freakspot.net>

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

import os
import warnings

try:
    from setuptools import setup
    setuptools_available = True
except ImportError:
    from distutils.core import setup
    setuptools_available = False

if os.name == 'nt':
    data_files = []
else:
    texinfo_manual_path = 'docs/_build/texinfo/ducker.info'
    data_files = [
        ('/usr/share/man/man1', ['ducker.1']),
        ('/etc/bash_completion.d', ['autocompletion/bash/ducker.bash'])
    ]
    if os.path.exists('/etc/fish/completions'):
        data_files.append(('/etc/fish/completions', ['autocompletion/fish/ducker.fish']))
    if os.path.isfile(texinfo_manual_path):
        data_files.append(('/usr/share/info', [texinfo_manual_path]))
    else:
        warnings.warn('''The program should install correctly. But in order to
                      also install the info page, you should execute  make info
                      in the docs directory and then run the installation
                      again''')

if setuptools_available:
    setuptools_compatibility_options = {
        'entry_points': {'console_scripts': ['ducker=ducker:main', 'duck=ducker:main']}
    }
else:
    import shutil
    if not os.path.exists('build/_scripts'):
        os.makedirs('build/_scripts')
    shutil.copyfile('run_ducker.py', 'build/_scripts/ducker')
    setuptools_compatibility_options = {'scripts': ['build/_scripts/ducker']}

setup(
    name='ducker',
    version=__import__('ducker').__version__,
    author='Jorge Maldonado Ventura',
    author_email='jorgesumle@freakspot.net',
    description='''Program that lets you search with DuckDuckGo from the
                   command line.''',
    license='GNU General Public License v3 (GPLv3)',
    keywords='CLI DuckDuckGo search terminal',
    url='https://www.freakspot.net/programas/ducker/',
    packages=['ducker'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ],
    data_files=data_files,
    **setuptools_compatibility_options
)
