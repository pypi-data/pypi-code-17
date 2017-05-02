"""
mgtoolkit: metagraph implementation tool

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

Copyright 2017, dinesha ranathunga.
Licensed under MIT.
"""
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as test_command


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(test_command):
    # noinspection PyAttributeOutsideInit
    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))


version = "1.0.2"

# noinspection PyPep8,PyPep8,PyPep8,PyPep8,PyPep8,PyPep8
setup(name="mgtoolkit",
      version=version,
      description="metagraph implementation tool",

      # List of packages that this one depends upon:
      install_requires=[
          'configobj==4.7.0',
          'pytest==2.7.0',
          'numpy==1.10.2'
          ],

      classifiers=[
          'Development Status :: 1 - Planning',
          'Programming Language :: Python',
          'Intended Audience :: Science/Research',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Networking',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Programming Language :: Python :: 2.7',
        ],

      keywords="metagraph implementation, policy analysis",
      author="dinesha ranathunga",
      author_email="dinesha.ranathunga@adelaide.edu.au",
      url="",
      license="MIT",
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      download_url="",
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      
      entry_points={
          'console_scripts': [
             'mgtoolkit = mgtoolkit.console_script:console_entry',
        ],
      }
     )
