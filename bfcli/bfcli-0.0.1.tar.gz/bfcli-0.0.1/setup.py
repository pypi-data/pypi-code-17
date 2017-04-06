from setuptools import setup

setup(
  name='bfcli',
  version='0.0.1',
  description='CLI for interactive with the Bitfusion Platform',
  author = "Brian Schultz",
  author_email='brian@bitfusion.io',
  url='http://www.bitfusion.io',
  py_modules=['bfcli'],
  install_requires=[
    'bitfusion',
    'click',
    'jsonschema',
    'python-dateutil',
    'pytz',
    'requests',
    'pyyaml'
  ],
  setup_requires=['pytest-runner'],
  tests_require=[
    'pytest',
    'docker'
  ],
  entry_points='''
    [console_scripts]
    bfcli=bfcli.cli:cli
  ''',
)
