#!/usr/bin/env python

name = 'noauthsftp'
path = 'noauthsftp.py'


## Automatically determine project version ##
from setuptools import setup, find_packages
try:
    from hgdistver import get_version
except ImportError:
    def get_version():
        import os
        
        d = {'__name__':name}

        # handle single file modules
        if os.path.isdir(path):
            module_path = os.path.join(path, '__init__.py')
        else:
            module_path = path
                                                
        with open(module_path) as f:
            try:
                exec(f.read(), None, d)
            except:
                pass

        return d.get("__version__", 0.1)

## Use py.test for "setup.py test" command ##
from setuptools.command.test import test as TestCommand
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)

## Try and extract a long description ##
for readme_name in ("README", "README.rst", "README.md"):
    try:
        readme = open(readme_name).read()
    except (OSError, IOError):
        continue
    else:
        break
else:
    readme = ""

try:
    changelog = open("CHANGELOG").read()
except (OSError, IOError):
    changelog = ""

readme = readme + "\n\n" + changelog


## Finally call setup ##
setup(
    name = name,
    version = get_version(),
    py_modules = [name],
    author = "Da_Blitz",
    author_email = "code@pocketnix.org",
    maintainer=None,
    maintainer_email=None,
    description = "Simple SFTP server that allows all logins (anon sftp)",
    long_description = readme,
    license = "ISC",
    keywords = "ssh asyncio sftp server",
    download_url=None,
    classifiers=[

    ],
    platforms=None,
    url = "http://blitz.works/noauthsftp",
    #test_loader = "epicworld.tests:EpicTests",
    #test_suite = "all",

    entry_points = {"console_scripts":["noauthsftp = noauthsftp:main"],
                   },

    # include any extra files found in the package dir
    include_package_data = True,
    
    # fine for pure python modules otherwise disable this unless you know what you are doing
    # if you need package_data/resources and you are not using the helpers but open() instead
    # (as well as some fancy autopath detection) then disable this option
    zip_safe = True,
    
    # needed if you are using distutils extensions for the build process
    setup_requires = ['hgdistver'],

    # optinal packages needed to install/run this app
    install_requires = ['asyncssh'],

    # extra packages needed for the test suite
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},
)
