"""
PyPI setup file
"""

from setuptools import setup


setup(
    name = 'pytmnd',
    packages = ['pytmnd'],
    version = '1.0.0-2',
    author='Matt Cotton',
    author_email='matthewcotton.cs@gmail.com',
    url='https://github.com/MattCCS/Pytmnd',

    description='YTMND site-opener',
    long_description=open("README.md").read(),
    classifiers=["Programming Language :: Python :: 3"],

    entry_points={
        'console_scripts': [
            'pytmnd=pytmnd.main:main',
        ],
    },
)
