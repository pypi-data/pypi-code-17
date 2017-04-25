#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3:
    print("you need to run madbot with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

setup(
    name='botlib',
    version='2',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots. JSON backend, MIT license.",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=[],
    scripts=["bot"],
    packages=['botlib'],
    long_description='''BOTLIB is a python3 framework to use if you want to program IRC or XMPP bots.

PROVIDES

| CLI, IRC and XMPP bots.
| Object that can be saved/loaded to/from JSON file.
| ReST server.
| RSS fetcher.
| UDP to channel forwarding.
| Scan email into objects.
| easy programmable. 

CONTACT

| Bart Thate
| botfather on #dunkbot irc.freenode.net
| bthate@dds.nl, thatebart@gmail.com
|
| BOTLIB is code released onder een MIT compatible license.


''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
