import os
import sys
from setuptools import setup, find_packages

version = '0.1.0'

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


setup(name='android-strings-format',
      version=version,
      description=('Android Strings format'),
      long_description='\n\n'.join((read('README.md'), read('CHANGELOG'))),
      classifiers=[
          'License :: OSI Approved :: BSD License',
          'Intended Audience :: Developers',
          'Programming Language :: Python'],
      keywords='android localization strings format xml values',
      author='Jonathan Odul',
      author_email='contact@takohi.com',
      url='https://github.com/KonsomeJona/android-strings-format',
      download_url = 'https://github.com/KonsomeJona/android-strings-format/archive/0.1.0.tar.gz',
      license='MIT',
      py_modules=['android_strings_format'],
      namespace_packages=[],
      install_requires = [],
      entry_points={
          'console_scripts': [
              'android-strings-format = android_strings_format:main']
      },
      include_package_data = False)
