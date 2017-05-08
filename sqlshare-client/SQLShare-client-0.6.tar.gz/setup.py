import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/sqlshare-client>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = 'sqlshare_client/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/sqlshare-client/wiki/Client-documentation"
setup(
    name='SQLShare-client',
    version=VERSION,
    packages=['sqlshare_client'],
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'setuptools',
        'sanction',
        'tabulate',
        'tqdm',
    ],
    license='Apache License, Version 2.0',
    scripts=['sqlshare_client/scripts/sqlshare_show_dataset',
             'sqlshare_client/scripts/sqlshare_all_datasets',
             'sqlshare_client/scripts/sqlshare_my_datasets',
             'sqlshare_client/scripts/sqlshare_shared_datasets',
             'sqlshare_client/scripts/sqlshare_whoami',
             'sqlshare_client/scripts/sqlshare_run_query',
             'sqlshare_client/scripts/sqlshare_list_queries',
             'sqlshare_client/scripts/sqlshare_permissions',
             'sqlshare_client/scripts/sqlshare_upload_file',
             'sqlshare_client/scripts/sqlshare_create_from_sql'],
    description='A library for accessing SQLShare REST Services',
    long_description=README,
    url=url,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)
