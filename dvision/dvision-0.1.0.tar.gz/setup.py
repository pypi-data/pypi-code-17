# !/usr/bin/env python

from distutils.core import setup


setup(
    name='dvision',
    packages=['dvision'],
    version='0.1.0',
    description='Pure python client for the DVID database',
    author='William Grisaitis',
    license='MIT',
    author_email='grisaitisw@janelia.hhmi.org',
    url='https://github.com/TuragaLab/dvision',
    keywords=['dvid', 'package', 'database', 'client', ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development',
    ],
)

