from distutils.core import setup

setup(
    name = 'servicenow_client',
    py_modules = ['servicenow_client'],
    url = 'http://pypi.python.org/pypi/servicenow_client',
    version = '0.1.0',
    author = 'Parul Neeraj',
    author_email = 'parulneeraj007@gmail.com',
    keywords = ['servicenow', 'rest', 'api', 'service', 'client', 'service now', 'servicenow_client'],
    description = 'A python module to access ServiceNow REST API',
    long_description = open('README.txt').read(),
    install_requires = ['requests'],
    license = 'GPLv2',
)
