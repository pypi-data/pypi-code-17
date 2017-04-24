# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from moven import __version__


try:
    with open('requirements.txt', 'r') as f:
        _install_requires = [line.rstrip('\n') for line in f]
except IOError:
    _install_requires = ['jip']  # TODO
    
setup(
    name="moven",
    version=__version__,
    url="https://bitbucket.org/ssix-project/moven",
    author="Sergio Fernández",
    author_email="sergio.fernandez@redlink.co",
    description="NLP models distribution relying on Maven infrastructure",
    packages=['moven'],
    platforms=['any'],
    install_requires=_install_requires,
    entry_points={
        'console_scripts': [
            'moven = moven.moven:main'
        ]
    },
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Build Tools',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Java',
                 'Environment :: Console'],
    keywords='python nlp ml dl models maven ssix',
    use_2to3=True
)
