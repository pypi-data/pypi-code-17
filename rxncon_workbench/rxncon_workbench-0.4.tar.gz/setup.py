import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='rxncon_workbench',
    scripts=[
        'runserver.py'
    ],
    version='0.4',
    packages=find_packages(),
    include_package_data=True,
    license='LGPL License', 
    description='A browser based interface for the rxncon framework.',
    long_description=README,
    url='https://www.rxncon.org/',
    author='Mathias Wajnberg',
    author_email='mathias.wajnberg@hu-berlin.de',
    keywords=['sysbio', 'signalling', 'systems biology'],
    install_requires=[
        'django',
	'rxncon',
	'typecheck-decorator',
        'typing',
    ]
)
