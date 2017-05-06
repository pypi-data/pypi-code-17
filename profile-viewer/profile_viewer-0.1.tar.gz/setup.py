#!/usr/bin/env python
"""Installs profile_viewer using distutils

Run:
    python setup.py install
to install the package from the source archive.
"""
import os, sys
import versioneer
try:
    from setuptools import setup
    setuptools = True
except ImportError:
    from distutils.core import setup
    setuptools = False

version = [(line.split('=')[1]).strip().strip('"').strip("'")
           for line in open(os.path.join('profile_viewer', '__init__.py'))
           if line.startswith('__version__')][0]

if __name__ == "__main__":
    extraArguments = {
        'classifiers': [
            """License :: OSI Approved :: BSD License""",
            """Programming Language :: Python""",
            """Topic :: Software Development :: Libraries :: Python Modules""",
            """Intended Audience :: Developers""",
        ],
        'keywords':
        'profile,gui,wxPython,squaremap',
        'long_description':
        """GUI Viewer for Python profiling runs

Provides explorability and overall visualization of the call tree
and package/module structures.""",
        'platforms': ['Any'],
    }
    if setuptools:
        extraArguments['install_package_data'] = True
    ### Now the actual set up call
    if sys.platform == 'darwin':
        gui_commands = [
            'runsnake=profile_viewer.macshim:macshim',
            'runsnake32=profile_viewer.runsnake:main',
            'runsnakemem=profile_viewer.runsnake:meliaemain',
        ]
    else:
        gui_commands = [
            'runsnake=profile_viewer.runsnake:main',
            'runsnakemem=profile_viewer.runsnake:meliaemain',
        ]
    setup(
        name="profile_viewer",
        version=versioneer.get_version(),
        url="http://www.vrplumber.com/programming/profile_viewer/",
        download_url="http://www.vrplumber.com/programming/profile_viewer/",
        description="GUI Viewer for Python profiling runs",
        author="Mike C. Fletcher",
        author_email="mcfletch@vrplumber.com",
        install_requires=[
            'SquareMap3 >= 1.0.3',
        ],
        license="BSD",
        package_dir={
            'profile_viewer': 'profile_viewer',
        },
        packages=[
            'profile_viewer',
        ],
        options={
            'sdist': {
                'force_manifest': 1,
                'formats': ['gztar', 'zip'],
            },
        },
        zip_safe=False,
        entry_points={
            'gui_scripts': gui_commands,
        },
        use_2to3=True,
        cmdclass=versioneer.get_cmdclass(),
        **extraArguments)
