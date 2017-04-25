import os
from setuptools import setup, find_packages


def long_desc(root_path):
    FILES = ['README.rst', 'CHANGES.rst']
    for filename in FILES:
        filepath = os.path.realpath(os.path.join(root_path, filename))
        if os.path.isfile(filepath):
            with open(filepath, mode='r') as f:
                yield f.read()


HERE = os.path.abspath(os.path.dirname(__file__))
long_description = "\n\n".join(long_desc(HERE))


def get_version(root_path):
    with open(os.path.join(root_path, 'emtex_common_utils', '__init__.py')) as f:
        for line in f:
            if line.startswith('__version__ ='):
                return line.split('=')[1].strip().strip('"\'')

setup(
    name='emtex_common_utils',
    version=get_version(HERE),
    license="BSD",
    description='Contains common application for Emtex',
    long_description=long_description,
    author='Amit Yadav',
    author_email='amityadav@amityadav.in',
    maintainer='am1tyadava',
    url='https://github.com/am1tyadava/emtex_common_utils',
    packages=find_packages(exclude=['tests*']),
    install_requires=['Django>=1.6'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
    ],
    zip_safe=False,
    tests_require=['Django>=1.6'],
)
