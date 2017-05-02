from setuptools import setup, find_packages

INSTALL_DEPS = [
  'python-dateutil >= 2.6.0',
  'pytz >= 2016.10',
  'requests >= 2.13.0',
  'requests-toolbelt >= 0.7.1',
]

TEST_DEPS = [
  'mock',
  'pytest',
]

setup(
  name='bitfusion',
  version='0.0.17',
  description='Python SDK for developing against the Bitfusion Platform',
  packages=find_packages(),
  author='Brian Schultz',
  author_email='brian@bitfusion.io',
  url='http://www.bitfusion.io',
  install_requires=INSTALL_DEPS,
  tests_require=TEST_DEPS,
  extras_require={'test': TEST_DEPS},
  setup_requires=['pytest-runner'],
)
