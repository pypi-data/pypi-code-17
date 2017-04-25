from setuptools import setup

setup(
    name='tetpyclient',
    packages=['tetpyclient'],  # this must be the same as the name above
    version='1.0',

    install_requires=['six', 'requests', 'requests_toolbelt'],

    description='Python API Client for Tetration Analytics',
    author='Cisco Tetration Analytics',
    author_email='openapi-dev@tetrationanalytics.com',
    url='https://github.com/TetrationAnalytics/tetpyclient',
    download_url='https://github.com/TetrationAnalytics/tetpyclient/tarball/1.0',
    license='Cisco API License'
)
