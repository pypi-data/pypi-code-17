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
    version='7',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots. JSON backend, MIT license.",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=[],
    scripts=["bot", "bot-udp", "bot-local", "bot-do"],
    packages=['botlib'],
    long_description='''
    
BOTLIB is a python3 framework to use if you want to program IRC or XMPP bots.

provides:

| CLI, IRC and XMPP bots.
| Object class  - save/load to/from a JSON file.
| ReST server - serve saved object's over HTTP.
| RSS fetcher - echo rss feeds to IRC channels.
| UDP server -  udp to bot to IRC channel.
| watcher server - run tail -f and have output send to IRC channel.
| email scanning - scan mbox format to searchable BOTLIB objects.
| modular structure, you can add funcionality yourself.

email:

| Bart Thate
| botfather on #dunkbot irc.freenode.net
| bthate@dds.nl, thatebart@gmail.com
|
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
