"""Setup file for Data Partitioner"""

from setuptools import setup

setup(
    name='data_partitioner',
    version='0.1',
    url='https://github.com/brahle/data_partitioner',
    license='GNU Lesser General Public License (LGPL), Version 3',
    author='brahle',
    author_email='brahle@gmail.com',
    description='Consistently partitions a dataset into a training set and a test set',
    long_description=open('README.rst', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['data_partitioner'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
