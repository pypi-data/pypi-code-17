from setuptools import setup, find_packages

# Try to convert markdown README to rst format for PyPI.
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='tangocard-raasv2',
    version='1.0.0b2',
    description='With this RESTful API you can integrate a global reward or incentive program into your app or platform. If you have any questions or if you\'d like to receive your own credentials, please contact us at devsupport@tangocard.com.',
    long_description=long_description,
    author='Tango Card, Inc.',
    author_email='devsupport@tangocard.com',
    url='https://github.com/tangocard/raas-v2-sdk-python',
    download_url='https://github.com/tangocard/raas-v2-sdk-python/archive/1.0.0b2.tar.gz',
    packages=find_packages(),
    install_requires=[
        'requests>=2.9.1, <3.0',
        'jsonpickle>=0.7.1, <1.0',
        'cachecontrol>=0.11.7, <1.0',
        'python-dateutil>=2.5.3, <3.0'
    ],
    tests_require=[
        'nose>=1.3.7'
    ],
    test_suite = 'nose.collector'
)
