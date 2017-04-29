#!/usr/bin/env python

import glob
import os
from distutils.core import setup

VERSION = '0.4.0'

# On dos-alike platforms, put data files in package dir.
# Otherwise make ptml subdirectory in share.
# XXX this solution is quite ugly, but i cannot think of
#   anything more intelligent right now.
if os.name in ('nt', 'os2', 'ce'):
    data_dir = os.path.join('lib', 'site-packages', 'ptml')
else:
    data_dir = os.path.join('share', 'ptml-' + VERSION)

data_files = [(os.path.join(data_dir, 'doc'), ['README', 'TODO'])]
for dir in ('benchmark', 'contrib', 'doc', 'testsuite'):
    data_files.append((os.path.join(data_dir, dir),
        [fn for fn in glob.glob(os.path.join(dir, '*')) if os.path.isfile(fn)]
    ))

setup(name="ptml",
    version=VERSION,
    description="PTML - Embed Python in text documents",
    author="Niall Smart",
    license="BSD License",
    author_email="niall@pobox.com",
    maintainer_email="ptml-users@lists.sourceforge.net",
    url="http://ptml.sourceforge.net/",
    download_url="http://sourceforge.net/project/showfiles.php?group_id=5811",
    long_description="""\
PTML is a Python module which lets you embed Python code in text
documents.  Its most common application is dynamic content generation
on web servers, however it can be used anywhere you need to generate
text files on-the-fly.""",
    platforms=["OS Independent"],
    # Note: we use Trove classifiers from PyPI list
    # (http://www.python.org/pypi?%3Aaction=list_classifiers),
    # not from SF Trove Categorization
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: No Input/Output (Daemon)',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Markup',
    ],
    packages=['ptml'],
    data_files=data_files,
)

# vim: set et sts=4 sw=4 :
