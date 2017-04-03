from setuptools import setup, find_packages

setup(
    name="scallopstogo",
    version="0.3.0",
    author="Andrew Lee",
    author_email="andrewlee@indeed.com",
    license="Reserved",
    description='Python library of helper and connection functions for use with Google Calendar API',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'pytz',
        'httplib2',
        'oauth2client'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
