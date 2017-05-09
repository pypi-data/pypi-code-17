from setuptools import setup, find_packages

setup(
    name = 'servermonitor',
    url = 'http://pypi.python.org/pypi/servermonitor',
    version = '1.0.0',
    author = 'chandresh soni',
    author_email = 'chndsoni00@gmail.com',
    keywords = ['serverMonitor', 'Monitor', 'api', 'excel', 'servers', 'diskusage', 'housekeeping'],
    description = 'A python module to moniter the servers and preform housekeeping',
    long_description = open('README.txt').read(),
    license = 'ACN',
    include_package_data=True,
)
