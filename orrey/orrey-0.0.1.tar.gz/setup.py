from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='orrey',
    version='0.0.1',
    description='Utilities for daily GLM tasks',
    long_description=readme(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
    ],
    url='http://github.com/kastman/orrey',
    author='Erik Kastman',
    author_email='erik.kastman@gmail.com',
    license='GPL',
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            'modelCorr = orrey.cli:modelCorr',
        ]
    },
    scripts=[],
    install_requires=['pandas', 'seaborn', 'moss'],
    test_suite='nose.collector',
    tests_require=['nose'])
