from setuptools import setup, find_packages

setup(
    name = 'osimis_timer',
    packages = find_packages(),
    version_format='{tag}',
    setup_requires=['setuptools-git-version', 'twine', 'wheel'],
    description = 'Timer/TimeOut helpers',
    author = 'Alain Mazy',
    author_email = 'am@osimis.io',
    url = 'https://bitbucket.org/osimis/python-osimis-timer',
    keywords = ['timer', 'timeout'],
    classifiers = [],
)
