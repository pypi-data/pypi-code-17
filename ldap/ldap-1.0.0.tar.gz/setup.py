#!/usr/bin/env python
from setuptools import setup
import ldap as pkg

repo_url = 'https://github.com/andreif/ldap'
version = pkg.__version__

setup(
    name='ldap',
    version=version,
    author='Andrei Fokau',
    author_email='andrei@5monkeys.se',
    description=pkg.parser.description,
    url=repo_url,
    download_url='%s/tarball/%s' % (repo_url, version),
    keywords=['ldap', 'utils', 'mock', 'server'],
    license='BSD',
    zip_safe=False,
    packages=[
        pkg.__name__,
    ],
    install_requires=[
        'ldap3',
    ],
    entry_points={
        'console_scripts': [
            '{0} = {0}:main'.format(pkg.__name__),
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
