import os, sys

HOME_DIR = os.path.dirname(__file__)

# ----
# find the version number (can't use import as there are dependenacies that
# setup.py may not have installed)
import re

pattern = re.compile("""
\s*              # skip whitespace
__version__      # look for variable name
\s*
=
\s*
\'(.*)\'         # look for whatever is assigned to __version__
""", re.VERBOSE)

with open('eenum.py', 'r') as f:
    data = f.read()
    match = pattern.search(data)
    __version__ = match.group(1)

# ----
# get the description

readme = os.path.join(HOME_DIR, 'README.rst')
long_description = open(readme).read()

# ---
# specified dependencies

install_requires = [
    'six>=1.10',
]

if sys.version_info[:2] < (3,4):
    install_requires.append('enum34>=1.0.4')

# ---
# create the parms for setup()

SETUP_ARGS = dict(
    name='eenum',
    version=__version__,
    description=('Extension to the python enum and Enum3.4 libraries'),
    long_description=long_description,
    url='https://github.com/cltrudeau/eenum',
    author='Christopher Trudeau',
    author_email='ctrudeau+pypi@arsensa.com',
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='tools,enum',
    test_suite='load_tests.get_suite',
    py_modules = ['eenum',],
    install_requires=install_requires,
    tests_require=[
        'waelstow==0.10.0',
    ],
)

if __name__ == '__main__':
    from setuptools import setup
    setup(**SETUP_ARGS)
