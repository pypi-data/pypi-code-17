import os
from setuptools import setup


def filter_requirements(fn):
    with open(fn) as fh:
        filtered_requirements = []
        for line in fh.readlines():
            if line[0] in ['#', ' ', '-']:
                continue
            filtered_requirements.append(line)
    return filtered_requirements


def load_version():
    with open('VERSION') as fh:
        res = fh.read()
    return res


version = load_version()

required = filter_requirements('requirements.txt')

required_test = filter_requirements('requirements-test.txt')

long_description = 'Install, then run ``eelifx --help``. See `the repo<https://github.com/cgspeck/eelifx>`_ for more information.'

if os.path.exists('README.rst'):
    with open('README.rst') as fh:
        long_description = fh.read()

setup(
    name='eelifx',
    description='Use game state in EmptyEpsilon to control your Lifx globes.',
    long_description=long_description,
    version=version,
    author='Chris Speck',
    author_email='cgspeck@gmail.com',
    url='https://github.com/cgspeck/eelifx',
    packages=['eelifx'],
    install_requires=required,
    extras_require={
        'tests': required_test
    },
    entry_points='''
        [console_scripts]
        eelifx=eelifx.cli:root
    ''',
    keywords=['EmptyEpsilon', 'Lifx'],
    download_url=f'https://github.com/cgspeck/eelifx/archive/{version}.tar.gz'
)
