import os
import re
import importlib
import subprocess
from pkg_resources import get_distribution
from string import ascii_letters
from distutils.core import setup


file_path = os.path.abspath(os.path.dirname(__file__))

__project__ = 'zbsmsa'

# Get version from __init__.py
def get_version(project=__project__):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format('__version__'), open(project + '/__init__.py').read())
    return result.group(1)

__author__ = 'Ian Doarn'
__version__ = get_version()
__url__ = 'https://github.com/IanDoarn/zbsmsa'
__license__ = 'Apache-2.0'
__email__ = 'ian.doarn@zimmerbiomet.com'
__classifiers__ = [
    'Intended Audience :: Developers',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
]
__pkg_data__ = {__project__+'.utils.json': ['*.json']}
__packages__ = [__project__,
                __project__ + '.inventory',
                __project__ + '.utils',
                __project__ + '.utils.json']


# Descriptions
long_desc = """ZimmerBiomet Surgery Management System Automation"""
short_desc = "ZimmerBiomet Surgery Management System Automation"


# Get required packages by checking if
# the user has them first, then adding them
# to the list of required if they don't.

install_requires = []
modules_to_update = []
# Pull required modules from requirements.txt
with open(os.path.join(file_path, 'requirements.txt'), 'r')as req_file:
    req_modules = req_file.readlines()
req_file.close()

# Attempt to import each module
for mod in req_modules:
    _mod = mod.replace('\n', '').split('>=')
    try:
        print('Attempting to import {}'.format(_mod[0]))
        # Try to import
        module = importlib.import_module(_mod[0])
        # Check version of module
        mod_dist = get_distribution(_mod[0])

        if len(set(list(mod_dist.version)).intersection(list(ascii_letters))) > 0:
            # module version has letters in it, attempt to upgrade it
            print('Could not verify version of {}'.format(_mod[0]))
            modules_to_update.append(_mod[0])
        else:
            mod_version = int(''.join(mod_dist.version.split('.')))
            req_mod_version = int(''.join(_mod[1].split('.')))
            if  mod_version < req_mod_version:
                print("{} is installed but is not the required version:"
                      "Installed [{}] Required [{}]".format(_mod[0],
                                                            str(mod_version),
                                                            str(req_mod_version)))
                modules_to_update.append(_mod[0])
            else:
                print("{} is installed and is the correct version [>={}]".format(_mod[0],
                                                                               _mod[1]))
        # delete from memory if successful
        del module
    except ModuleNotFoundError as error:
        # could not import so add to install requires
        print('Could not import {}'.format(_mod[0]))
        install_requires.append(mod.replace('\n', ''))


# Attempt to update modules
def update_modules():
    if len(modules_to_update) != 0:
        for mod in modules_to_update:
            try:
                subprocess.call(['pip',
                                 'install',
                                 mod,
                                 '--upgrade'], shell=True)
            except Exception as error:
                print('Unable to update {} to the required / latest version. '
                      'Please resolve this issue to ensure stability. '
                      'Error: [{}]'.format(mod, str(error)))


# Actual setup process
setup_inf = dict(
    name=__project__,
    version=__version__,
    install_requires=install_requires,
    packages=__packages__,
    package_data=__pkg_data__,
    url=__url__,
    license=__license__,
    author=__author__,
    author_email=__email__,
    long_description=long_desc,
    description=short_desc,
    classifiers=__classifiers__,
    zip_safe=True
)

setup(**setup_inf)