from setuptools import setup
from setuptools import find_packages
import os
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
setup(
    name='pnc-cli',
    packages=find_packages(exclude=['test*']),
    version='1.0.3',
    description='CLI wrapper for PNC REST calls',
    author = 'Tom Hauser',
    author_email = 'thauser@redhat.com',
    url = 'https://github.com/project-ncl/pnc-cli',
    download_url='https://github.com/project-ncl/pnc-cli/tarball/pypi-1.0.3',
    keywords = ['PNC','REST'],
    long_description=README,
    install_requires=[
	"argh >= 0.26.1",
        "requests >= 2.4.3",
        "certifi >= 2015.04.28",
	"urllib3 >= 1.12",
	"six >= 1.9.0",
        "validators >=0.10",
        "tzlocal >= 1.0",
        "pytest >= 2.0"
    ],
    classifiers=[
	'Development Status :: 3 - Alpha',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3'
    ],
    entry_points={'console_scripts': ['pnc = pnc_cli.pnc:main']}
)
