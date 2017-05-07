#
#  This is the git-remote-hg setuptools script.
#  Originally developed by Ryan Kelly, 2011.
#
#  This script is placed in the public domain.
#

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import versioneer

from git_remote_hg import __doc__

NAME = "git-remote-hg3"
DESCRIPTION = "access hg repositories as git remotes"
LONG_DESC = __doc__
AUTHOR = "Ryan Kelly"
AUTHOR_EMAIL = "ryan@rfk.id.au"
URL = "http://github.com/rfk/git-remote-hg"
LICENSE = "MIT"
KEYWORDS = "git hg mercurial"
INSTALL_REQUIRES = ["hg-git"]
CLASSIFIERS = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "License :: OSI Approved",
    "License :: OSI Approved :: MIT License",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
]

setup(
    name=NAME,
    version=versioneer.get_version(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description=DESCRIPTION,
    long_description=LONG_DESC,
    license=LICENSE,
    keywords=KEYWORDS,
    packages=["git_remote_hg"],
    entry_points={
        'console_scripts': [
            'git-remote-hg = git_remote_hg.__main__:main',
        ],
    },
    install_requires=INSTALL_REQUIRES,
    classifiers=CLASSIFIERS,
    cmdclass=versioneer.get_cmdclass())
