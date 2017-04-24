#! /usr/bin/env python

''' Setup script for cmsplugin-blurp
'''

import os
import subprocess

from setuptools import setup, find_packages
from setuptools.command.install_lib import install_lib as _install_lib
from setuptools.command.sdist import sdist
from distutils.command.build import build as _build
from distutils.cmd import Command

class compile_translations(Command):
    description = 'compile message catalogs to MO files via django compilemessages'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os
        import sys
        try:
            from django.core.management import call_command
            for path in ['src/cmsplugin_blurp/']:
                curdir = os.getcwd()
                os.chdir(os.path.realpath(path))
                call_command('compilemessages')
                os.chdir(curdir)
        except ImportError:
            print
            sys.stderr.write('!!! Please install Django >= 1.7 to build translations')
            print

class build(_build):
    sub_commands = [('compile_translations', None)] + _build.sub_commands

class eo_sdist(sdist):
    sub_commands = [('compile_translations', None)] + sdist.sub_commands

    def run(self):
        if os.path.exists('VERSION'):
            os.remove('VERSION')
        version = get_version()
        version_file = open('VERSION', 'w')
        version_file.write(version)
        version_file.close()
        sdist.run(self)
        if os.path.exists('VERSION'):
            os.remove('VERSION')


class install_lib(_install_lib):
    def run(self):
        self.run_command('compile_translations')
        _install_lib.run(self)

def get_version():
    if os.path.exists('VERSION'):
        version_file = open('VERSION', 'r')
        version = version_file.read()
        version_file.close()
        return version
    if os.path.exists('.git'):
        p = subprocess.Popen(['git', 'describe', '--dirty', '--match=v*'], stdout=subprocess.PIPE)
        result = p.communicate()[0]
        if p.returncode == 0:
            version = result.split()[0][1:]
            version = version.replace('-', '.')
            return version
    return '0'

setup(name="django-cmsplugin-blurp",
      version=get_version(),
      license="AGPLv3 or later",
      description="",
      long_description=file('README').read(),
      url="http://dev.entrouvert.org/projects/django-cmsplugin-blurp/",
      author="Entr'ouvert",
      author_email="info@entrouvert.org",
      maintainer="Benjamin Dauvergne",
      maintainer_email="bdauvergne@entrouvert.com",
      packages=find_packages('src'),
      install_requires=[
          'django>=1.7,<1.8',
          'django-classy-tags',
      ],
      package_dir={
          '': 'src',
      },
      package_data={
          'cmsplugin_blurp': [
              'locale/fr/LC_MESSAGES/*.po',
              'templates/cmsplugin_blurp/*',
              'tests_data/*'
          ],
      },
      tests_require=[
          'nose>=0.11.4',
      ],
      dependency_links=[],
      cmdclass={
          'build': build,
          'install_lib': install_lib,
          'compile_translations': compile_translations,
          'sdist': eo_sdist,
      },
)
